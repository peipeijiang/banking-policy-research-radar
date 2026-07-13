"""Free working-paper discovery from configured IDEAS/RePEc series."""

import html
import logging
import re
from datetime import datetime, timedelta
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urljoin

import requests

from .base_source import BasePaperSource, PaperMetadata

logger = logging.getLogger(__name__)


class _HtmlMetadataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta: Dict[str, str] = {}
        self.links: List[str] = []
        self.download_urls: List[str] = []
        self.current_year_links: List[str] = []
        self._heading_parts: List[str] = []
        self._inside_heading = False
        self._inside_current_year = False

    def handle_starttag(self, tag: str, attrs) -> None:
        values = {str(key).lower(): value for key, value in attrs if value is not None}
        if tag.lower() == "h3":
            self._inside_heading = True
            self._heading_parts = []
        if tag.lower() == "meta":
            name = (values.get("name") or values.get("property") or "").lower()
            if name and values.get("content"):
                self.meta[name] = html.unescape(values["content"]).strip()
        elif tag.lower() == "a" and values.get("href"):
            href = html.unescape(values["href"]).strip()
            self.links.append(href)
            if self._inside_current_year:
                self.current_year_links.append(href)
        elif (
            tag.lower() == "input"
            and values.get("name", "").lower() == "url"
            and values.get("value")
        ):
            self.download_urls.append(html.unescape(values["value"]).strip())

    def handle_data(self, data: str) -> None:
        if self._inside_heading:
            self._heading_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() != "h3":
            return
        heading = " ".join(self._heading_parts).strip()
        self._inside_current_year = heading == str(datetime.now().year)
        self._inside_heading = False


class RepecSeriesSource(BasePaperSource):
    """Read recent free papers from economic working-paper series catalogs."""

    def __init__(
        self,
        history_dir: Path,
        series: List[Dict[str, str]],
        max_results: int = 50,
    ):
        super().__init__("repec", history_dir)
        self.series = series
        self.max_results = max_results
        self.session = requests.Session()
        self.session.headers["User-Agent"] = (
            "ArxivDailyResearcher/3.2 "
            "(https://github.com/peipeijiang/arxiv-daily-researcher)"
        )

    @property
    def display_name(self) -> str:
        return "Free Economic Working Paper Series"

    def can_download_pdf(self) -> bool:
        return True

    @staticmethod
    def _parser(content: str) -> _HtmlMetadataParser:
        parser = _HtmlMetadataParser()
        parser.feed(content)
        return parser

    @staticmethod
    def _published(meta: Dict[str, str]) -> tuple[datetime, str]:
        raw = meta.get("citation_publication_date") or meta.get("date") or ""
        for fmt in ("%Y/%m/%d", "%Y-%m-%d", "%Y/%m", "%Y-%m"):
            try:
                precision = "day" if fmt in ("%Y/%m/%d", "%Y-%m-%d") else "month"
                return datetime.strptime(raw, fmt), precision
            except ValueError:
                pass
        year = meta.get("citation_year") or raw[:4]
        if year.isdigit() and len(year) == 4:
            return datetime(int(year), 1, 1), "year"
        return datetime.now(), "unknown"

    @staticmethod
    def _authors(meta: Dict[str, str]) -> List[str]:
        raw = meta.get("citation_authors") or meta.get("author") or ""
        separator = ";" if ";" in raw else "&"
        return [part.strip() for part in raw.split(separator) if part.strip()]

    @staticmethod
    def _doi(meta: Dict[str, str]) -> Optional[str]:
        return meta.get("doi") or meta.get("citation_doi") or None

    @staticmethod
    def _direct_pdf(urls: List[str]) -> Optional[str]:
        for url in urls:
            if re.search(r"\.pdf(?:$|[?#])", url, re.I):
                return url.replace("http://", "https://", 1)
        return None

    def _item_links(self, series_url: str, limit: int) -> List[str]:
        response = self.session.get(series_url, timeout=30)
        response.raise_for_status()
        parser = self._parser(response.text)
        links: List[str] = []
        candidates = parser.current_year_links or parser.links
        for href in candidates:
            absolute = urljoin(response.url, href)
            if not re.search(r"ideas\.repec\.org/p/.+\.html(?:$|[?#])", absolute, re.I):
                continue
            if absolute not in links:
                links.append(absolute)
            if len(links) >= limit:
                break
        return links

    def _paper(self, item_url: str, config: Dict[str, str], cutoff: datetime) -> Optional[PaperMetadata]:
        response = self.session.get(item_url, timeout=30)
        response.raise_for_status()
        parser = self._parser(response.text)
        meta = parser.meta
        if meta.get("freedownload") != "1":
            return None

        handle = meta.get("handle") or item_url
        paper_id = f"repec:{handle}"
        if self.is_processed(paper_id):
            return None
        title = meta.get("citation_title") or meta.get("title") or ""
        if not title:
            return None
        published, date_precision = self._published(meta)
        if date_precision == "day" and published < cutoff:
            return None
        if date_precision == "month" and published < cutoff.replace(day=1):
            return None
        if date_precision == "year" and published.year != datetime.now().year:
            return None

        source = config.get("name") or "repec"
        display_name = config.get("display_name") or source.upper()
        abstract = meta.get("citation_abstract") or meta.get("description") or ""
        abstract = re.sub(r"^Downloadable!\s*", "", abstract).strip()
        direct_pdf = self._direct_pdf(parser.download_urls)
        landing = next((url for url in parser.download_urls if url), item_url)
        candidate = {
            "landing_page_url": landing,
            "pdf_url": direct_pdf,
            "source": display_name,
            "source_type": "repository",
            "license": None,
        }
        return PaperMetadata(
            paper_id=paper_id,
            title=title,
            authors=self._authors(meta),
            abstract=abstract,
            published_date=published,
            url=item_url,
            source=source,
            pdf_url=direct_pdf,
            doi=self._doi(meta),
            journal=meta.get("citation_journal_title") or display_name,
            publication_type="working-paper",
            open_access_candidates=[candidate],
            fulltext_provenance=(
                {
                    "provider": "repec_free_fulltext",
                    "source": source,
                    "pdf_url": direct_pdf,
                }
                if direct_pdf
                else {}
            ),
            discovery={
                "provider": "IDEAS/RePEc",
                "series_url": config.get("url"),
                "free_download": True,
                "date_precision": date_precision,
            },
        )

    def fetch_papers(self, days: int, **kwargs) -> List[PaperMetadata]:
        del kwargs
        cutoff = datetime.now() - timedelta(days=days)
        per_series = max(1, self.max_results // max(1, len(self.series)))
        papers: Dict[str, PaperMetadata] = {}

        for config in self.series:
            name = config.get("name") or "repec"
            url = config.get("url") or ""
            if not url:
                continue
            selected = 0
            try:
                item_links = self._item_links(url, max(per_series * 4, 8))
                for item_url in item_links:
                    paper = self._paper(item_url, config, cutoff)
                    if not paper or paper.paper_id in papers:
                        continue
                    papers[paper.paper_id] = paper
                    selected += 1
                    if selected >= per_series or len(papers) >= self.max_results:
                        break
            except requests.RequestException as exc:
                logger.warning(f"[{name}] RePEc 系列抓取失败: {exc}")
            logger.info(f"[{name}] RePEc 免费全文命中 {selected} 篇")
            if len(papers) >= self.max_results:
                break

        return list(papers.values())
