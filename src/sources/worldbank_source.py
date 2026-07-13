"""World Bank Policy Research Working Papers via the official Documents API."""

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

import requests

from .base_source import BasePaperSource, PaperMetadata

logger = logging.getLogger(__name__)


class WorldBankSource(BasePaperSource):
    API_URL = "https://search.worldbank.org/api/v3/wds"

    def __init__(
        self,
        history_dir: Path,
        search_terms: List[str],
        max_results: int = 40,
    ):
        super().__init__("worldbank", history_dir)
        self.search_terms = search_terms
        self.max_results = max_results
        self.session = requests.Session()
        self.session.headers["User-Agent"] = (
            "ArxivDailyResearcher/3.2 "
            "(https://github.com/peipeijiang/arxiv-daily-researcher)"
        )

    @property
    def display_name(self) -> str:
        return "World Bank Policy Research Working Papers"

    def can_download_pdf(self) -> bool:
        return True

    @staticmethod
    def _authors(value) -> List[str]:
        if isinstance(value, dict):
            value = value.get("author") or value.get("cdata!") or []
        if isinstance(value, str):
            return [item.strip() for item in value.split(";") if item.strip()]
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        return []

    def fetch_papers(self, days: int, **kwargs) -> List[PaperMetadata]:
        del kwargs
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        per_term = max(1, self.max_results // max(1, len(self.search_terms)))
        papers: Dict[str, PaperMetadata] = {}

        for term in self.search_terms:
            try:
                response = self.session.get(
                    self.API_URL,
                    params={
                        "format": "json",
                        "qterm": term,
                        "strdate": start_date,
                        "docty_exact": "Policy Research Working Paper",
                        "rows": per_term,
                        "srt": "docdt",
                        "order": "desc",
                        "fl": "docdt,abstracts,authors,pdfurl,docty,display_title",
                    },
                    timeout=30,
                )
                response.raise_for_status()
                documents = response.json().get("documents") or {}
            except (requests.RequestException, ValueError) as exc:
                logger.warning(f"[World Bank] 检索失败 ({term}): {exc}")
                continue

            for item in documents.values():
                if not isinstance(item, dict) or not item.get("id"):
                    continue
                paper_id = f"worldbank:{item['id']}"
                if paper_id in papers or self.is_processed(paper_id):
                    continue
                title = item.get("display_title") or ""
                if not title:
                    continue
                raw_date = item.get("docdt") or ""
                try:
                    published = datetime.fromisoformat(raw_date.replace("Z", "+00:00")).replace(
                        tzinfo=None
                    )
                except ValueError:
                    published = datetime.now()
                abstract_data = item.get("abstracts") or {}
                abstract = (
                    abstract_data.get("cdata!", "")
                    if isinstance(abstract_data, dict)
                    else str(abstract_data)
                )
                pdf_url = (item.get("pdfurl") or "").replace("http://", "https://", 1)
                landing_url = (item.get("url") or "").replace("http://", "https://", 1)
                papers[paper_id] = PaperMetadata(
                    paper_id=paper_id,
                    title=title,
                    authors=self._authors(item.get("authors")),
                    abstract=abstract,
                    published_date=published,
                    url=landing_url or pdf_url,
                    source="worldbank",
                    pdf_url=pdf_url or None,
                    journal="World Bank Policy Research Working Paper",
                    publication_type="working-paper",
                    fulltext_provenance=(
                        {
                            "provider": "worldbank_documents_api",
                            "pdf_url": pdf_url,
                        }
                        if pdf_url
                        else {}
                    ),
                )
                if len(papers) >= self.max_results:
                    break
            if len(papers) >= self.max_results:
                break

        logger.info(f"[World Bank] 去重后命中 {len(papers)} 篇近期政策研究工作论文")
        return list(papers.values())
