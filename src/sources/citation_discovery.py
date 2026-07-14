"""Bounded discovery of papers connected to strong historical seeds."""

import json
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List

from .base_source import PaperMetadata


class CitationDiscovery:
    def __init__(
        self,
        openalex,
        index_path: Path = Path("knowledge/index.jsonl"),
        max_age_days: int = 365,
        include_seed_references: bool = True,
    ):
        self.openalex = openalex
        self.index_path = index_path
        self.max_age_days = max(1, max_age_days)
        self.include_seed_references = include_seed_references

    def _is_recent(self, paper: PaperMetadata) -> bool:
        published = paper.published_date
        if not published:
            return False
        published_date = published.date() if isinstance(published, datetime) else published
        return published_date >= date.today() - timedelta(days=self.max_age_days)

    def _seeds(self, limit: int = 5) -> List[Dict]:
        if not self.index_path.exists():
            return []
        seeds = {}
        for line in self.index_path.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
                if row.get("openalex_id") and row.get("qualified") and row.get("score", 0) >= 80:
                    seeds[row["paper_id"]] = row
            except (json.JSONDecodeError, KeyError):
                continue
        return sorted(seeds.values(), key=lambda row: row.get("score", 0), reverse=True)[:limit]

    def discover(self, existing_ids: set, max_total: int = 20) -> List[PaperMetadata]:
        candidates = {}
        for seed in self._seeds():
            seed_id = seed["openalex_id"]
            related_ids = seed.get("related_works", [])[:3]
            relation_groups = [("related_to_seed", related_ids)]
            if self.include_seed_references:
                relation_groups.append(
                    ("referenced_by_seed", seed.get("referenced_works", [])[:3])
                )
            for relation, ids in relation_groups:
                for work_id, paper in self.openalex.lookup_by_ids(ids).items():
                    if (
                        not self._is_recent(paper)
                        or paper.paper_id in existing_ids
                        or self.openalex.is_processed(paper.paper_id)
                    ):
                        continue
                    paper.discovery = {
                        "channel": "citation_expansion",
                        "relation": relation,
                        "seed_paper_id": seed["paper_id"],
                        "seed_title": seed["title"],
                        "seed_score": seed["score"],
                    }
                    candidates[work_id] = paper
            since = (date.today() - timedelta(days=min(30, self.max_age_days))).isoformat()
            for paper in self.openalex.find_recent_citing(seed_id, since, limit=5):
                if (
                    not self._is_recent(paper)
                    or paper.paper_id in existing_ids
                    or self.openalex.is_processed(paper.paper_id)
                ):
                    continue
                paper.discovery = {
                    "channel": "citation_expansion",
                    "relation": "cites_seed",
                    "seed_paper_id": seed["paper_id"],
                    "seed_title": seed["title"],
                    "seed_score": seed["score"],
                }
                candidates[paper.openalex_id or paper.paper_id] = paper
            if len(candidates) >= max_total:
                break
        return list(candidates.values())[:max_total]
