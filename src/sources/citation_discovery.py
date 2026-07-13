"""Bounded discovery of papers connected to strong historical seeds."""

import json
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List

from .base_source import PaperMetadata


class CitationDiscovery:
    def __init__(self, openalex, index_path: Path = Path("knowledge/index.jsonl")):
        self.openalex = openalex
        self.index_path = index_path

    def _seeds(self, limit: int = 10) -> List[Dict]:
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

    def discover(self, existing_ids: set, max_total: int = 60) -> List[PaperMetadata]:
        candidates = {}
        for seed in self._seeds():
            seed_id = seed["openalex_id"]
            related_ids = seed.get("related_works", [])[:5]
            reference_ids = seed.get("referenced_works", [])[:5]
            for relation, ids in (("related_to_seed", related_ids), ("referenced_by_seed", reference_ids)):
                for work_id, paper in self.openalex.lookup_by_ids(ids).items():
                    if paper.paper_id in existing_ids or self.openalex.is_processed(paper.paper_id):
                        continue
                    paper.discovery = {
                        "channel": "citation_expansion",
                        "relation": relation,
                        "seed_paper_id": seed["paper_id"],
                        "seed_title": seed["title"],
                        "seed_score": seed["score"],
                    }
                    candidates[work_id] = paper
            since = (date.today() - timedelta(days=30)).isoformat()
            for paper in self.openalex.find_recent_citing(seed_id, since, limit=10):
                if paper.paper_id in existing_ids or self.openalex.is_processed(paper.paper_id):
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
