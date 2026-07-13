"""DBLP conference proceedings source for recommender-systems research."""

import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

import requests
from tenacity import before_sleep_log, retry, stop_after_attempt, wait_exponential

from .base_source import BasePaperSource, PaperMetadata

logger = logging.getLogger(__name__)


class DblpSource(BasePaperSource):
    API_URL = "https://dblp.org/search/publ/api"

    def __init__(
        self,
        history_dir: Path,
        venues: List[str],
        title_terms: List[str],
        max_results: int = 120,
    ):
        super().__init__("dblp", history_dir)
        self.venues = [venue.lower() for venue in venues]
        self.title_terms = title_terms
        self.max_results = max_results
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "ArxivDailyResearcher/3.2 "
                    "(https://github.com/peipeijiang/arxiv-daily-researcher)"
                )
            }
        )

    @property
    def display_name(self) -> str:
        return "DBLP Conferences"

    def can_download_pdf(self) -> bool:
        return False

    def _request(self, query: str) -> Dict:
        from config import settings

        @retry(
            stop=stop_after_attempt(settings.RETRY_MAX_ATTEMPTS),
            wait=wait_exponential(min=settings.RETRY_MIN_WAIT, max=settings.RETRY_MAX_WAIT),
            before_sleep=before_sleep_log(logger, logging.WARNING),
            reraise=True,
        )
        def do_request():
            response = self.session.get(
                self.API_URL,
                params={"q": query, "h": 500, "format": "json"},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()

        return do_request()

    def _matches_title(self, title: str) -> bool:
        normalized = re.sub(r"[^a-z0-9]+", " ", title.lower())
        return any(term.lower() in normalized for term in self.title_terms)

    @staticmethod
    def _authors(info: Dict) -> List[str]:
        raw = (info.get("authors") or {}).get("author", [])
        if isinstance(raw, (str, dict)):
            raw = [raw]
        authors = []
        for author in raw:
            if isinstance(author, str):
                authors.append(author)
            elif isinstance(author, dict):
                name = author.get("text") or author.get("#text")
                if name:
                    authors.append(name)
        return authors

    def fetch_papers(self, days: int, **kwargs) -> List[PaperMetadata]:
        del days  # DBLP exposes publication year, while history tracks daily ingestion.
        current_year = datetime.now(timezone.utc).year
        papers: Dict[str, PaperMetadata] = {}
        per_venue_limit = max(1, self.max_results // max(1, len(self.venues)))

        logger.info(f"[DBLP] 开始抓取会议论文: {self.venues}")
        for venue in self.venues:
            venue_selected = 0
            for year in (current_year, current_year - 1):
                if venue_selected >= per_venue_limit:
                    break
                query = f"stream:streams/conf/{venue}: year:{year}"
                try:
                    data = self._request(query)
                except Exception as exc:
                    logger.warning(f"[DBLP] {venue.upper()} {year} 抓取失败: {exc}")
                    continue

                hits = (data.get("result") or {}).get("hits", {}).get("hit", [])
                if isinstance(hits, dict):
                    hits = [hits]
                matched = 0
                for hit in hits:
                    info = hit.get("info") or {}
                    title = re.sub(r"\s+", " ", info.get("title") or "").strip().rstrip(".")
                    if not title or not self._matches_title(title):
                        continue
                    doi = info.get("doi")
                    dblp_key = info.get("key")
                    paper_id = f"https://doi.org/{doi}" if doi else f"dblp:{dblp_key}"
                    if not paper_id or self.is_processed(paper_id):
                        continue
                    if paper_id in papers:
                        continue
                    papers[paper_id] = PaperMetadata(
                        paper_id=paper_id,
                        title=title,
                        authors=self._authors(info),
                        abstract="",
                        published_date=datetime(int(info.get("year") or year), 1, 1),
                        url=info.get("url") or f"https://dblp.org/rec/{dblp_key}",
                        source=venue,
                        doi=f"https://doi.org/{doi}" if doi else None,
                        journal=info.get("venue") or venue.upper(),
                        publication_type=info.get("type") or "Conference and Workshop Papers",
                    )
                    matched += 1
                    venue_selected += 1
                    if venue_selected >= per_venue_limit:
                        break
                logger.info(f"  {venue.upper()} {year}: 标题预筛命中 {matched} 篇")

        logger.info(f"[DBLP] 去重后共发现 {len(papers)} 篇会议候选")
        return list(papers.values())
