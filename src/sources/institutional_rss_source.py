"""Official central-bank and institution research RSS feeds."""

import calendar
import html
import logging
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional

import feedparser
import requests

from .base_source import BasePaperSource, PaperMetadata

logger = logging.getLogger(__name__)


class InstitutionalRssSource(BasePaperSource):
    def __init__(
        self,
        history_dir: Path,
        feeds: List[Dict[str, str]],
        max_results: int = 60,
    ):
        super().__init__("institutional", history_dir)
        self.feeds = feeds
        self.max_results = max_results
        self.session = requests.Session()
        self.session.headers["User-Agent"] = (
            "ArxivDailyResearcher/3.2 "
            "(https://github.com/peipeijiang/arxiv-daily-researcher)"
        )

    @property
    def display_name(self) -> str:
        return "Official Institution Working Papers"

    def can_download_pdf(self) -> bool:
        return True

    @staticmethod
    def _plain_text(value: str) -> str:
        value = re.sub(r"<[^>]+>", " ", value or "")
        return re.sub(r"\s+", " ", html.unescape(value)).strip()

    @staticmethod
    def _published(entry) -> Optional[datetime]:
        parsed = entry.get("published_parsed") or entry.get("updated_parsed")
        if not parsed:
            return None
        return datetime.fromtimestamp(calendar.timegm(parsed), tz=timezone.utc).replace(
            tzinfo=None
        )

    @staticmethod
    def _pdf_url(entry) -> Optional[str]:
        candidates = [entry.get("cb_link"), entry.get("link")]
        candidates.extend(link.get("href") for link in entry.get("links", []))
        for candidate in candidates:
            if candidate and re.search(r"\.pdf(?:$|[?#])", candidate, re.I):
                return candidate.replace("http://", "https://", 1)
        return None

    def fetch_papers(self, days: int, **kwargs) -> List[PaperMetadata]:
        del kwargs
        cutoff = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=days)
        per_feed = max(1, self.max_results // max(1, len(self.feeds)))
        papers: Dict[str, PaperMetadata] = {}

        for feed in self.feeds:
            name = feed.get("name") or "institutional"
            url = feed.get("url") or ""
            if not url:
                continue
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                parsed_feed = feedparser.parse(response.content)
            except requests.RequestException as exc:
                logger.warning(f"[{name}] RSS 抓取失败: {exc}")
                continue

            selected = 0
            for entry in parsed_feed.entries:
                published = self._published(entry)
                if published and published < cutoff:
                    continue
                title = self._plain_text(entry.get("title"))
                landing_url = entry.get("link") or entry.get("id") or ""
                if not title or not landing_url:
                    continue
                paper_id = f"{name}:{entry.get('id') or landing_url}"
                if paper_id in papers or self.is_processed(paper_id):
                    continue
                authors = [
                    author.get("name")
                    for author in entry.get("authors", [])
                    if author.get("name")
                ]
                abstract = self._plain_text(
                    entry.get("dcterms_abstract") or entry.get("summary") or ""
                )
                pdf_url = self._pdf_url(entry)
                paper = PaperMetadata(
                    paper_id=paper_id,
                    title=title,
                    authors=authors,
                    abstract=abstract,
                    published_date=published or datetime.now(),
                    url=landing_url,
                    source=name,
                    pdf_url=pdf_url,
                    journal=feed.get("display_name") or name.upper(),
                    publication_type="working-paper",
                    open_access_candidates=[
                        {
                            "landing_page_url": landing_url,
                            "pdf_url": pdf_url,
                            "source": feed.get("display_name") or name.upper(),
                            "source_type": "repository",
                            "license": None,
                        }
                    ],
                    fulltext_provenance=(
                        {
                            "provider": "official_institution_rss",
                            "source": name,
                            "pdf_url": pdf_url,
                        }
                        if pdf_url
                        else {}
                    ),
                )
                papers[paper_id] = paper
                selected += 1
                if selected >= per_feed:
                    break
            logger.info(f"[{name}] RSS 命中 {selected} 篇近期工作论文")

        return list(papers.values())[: self.max_results]
