#!/usr/bin/env python3
"""Re-score the existing knowledge index without fetching or analyzing papers again."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agents.analysis_agent import AnalysisAgent, WeightedScoreResponse  # noqa: E402
from config import settings  # noqa: E402


SCORING_VERSION = "independent-domains-v1"
ANALYSIS_EVIDENCE_FIELDS = (
    "summary",
    "innovations",
    "methodology",
    "key_results",
    "strengths",
    "limitations",
    "relevance_to_keywords",
)


def _flatten_text(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(
            f"{key}: {_flatten_text(item)}"
            for key, item in value.items()
            if _flatten_text(item)
        )
    if isinstance(value, list):
        return "\n".join(_flatten_text(item) for item in value if _flatten_text(item))
    return str(value or "").strip()


def build_scoring_evidence(record: Dict[str, Any], max_chars: int = 12000) -> Tuple[str, str]:
    """Return evidence text and its provenance for relevance scoring."""
    abstract = _flatten_text(record.get("abstract"))
    if abstract:
        return abstract[:max_chars], "abstract"

    analysis = record.get("analysis") or {}
    sections = []
    for field in ANALYSIS_EVIDENCE_FIELDS:
        text = _flatten_text(analysis.get(field))
        if text:
            sections.append(f"{field}: {text}")
    if sections:
        return "\n".join(sections)[:max_chars], "existing_analysis"

    tldr = _flatten_text(record.get("tldr"))
    if tldr and "评分失败" not in tldr:
        return tldr[:max_chars], "existing_tldr"

    return "[No abstract or analysis is available; assess conservatively from the title.]", "title_only"


def apply_score(
    record: Dict[str, Any],
    score: WeightedScoreResponse,
    evidence_basis: str,
    rescored_at: str,
) -> Dict[str, Any]:
    """Apply a successful domain score while preserving all paper content."""
    updated = dict(record)
    total_score = round(float(score.total_score), 2)
    matched_domain = score.matched_domain
    matched_config = settings.DOMAIN_KEYWORD_GROUPS.get(matched_domain or "", {})

    updated.update(
        {
            "score": total_score,
            "base_score": total_score,
            "qualified": bool(score.is_qualified),
            "domain_scores": {
                key: round(float(value), 2) for key, value in score.domain_scores.items()
            },
            "matched_domain": matched_domain,
            "matched_domain_label": matched_config.get("label"),
            "score_reasoning": score.reasoning,
            "scoring": {
                "version": SCORING_VERSION,
                "rescored_at": rescored_at,
                "evidence_basis": evidence_basis,
                "passing_rule": (
                    f"any domain >= {float(settings.DOMAIN_PASSING_SCORE):.1f}/10"
                ),
            },
        }
    )

    personalization = dict(updated.get("personalization") or {})
    if personalization:
        adjustment = float(personalization.get("adjustment") or 0)
        personalization["base_score"] = total_score
        personalization["personalized_score"] = round(total_score + adjustment, 2)
        updated["personalization"] = personalization

    return updated


def _load_records(path: Path) -> list[Dict[str, Any]]:
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON at {path}:{line_number}: {exc}") from exc
        if not record.get("paper_id") or not record.get("title"):
            raise ValueError(f"Missing paper_id or title at {path}:{line_number}")
        records.append(record)
    return records


def _atomic_write_jsonl(path: Path, records: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            for record in records:
                handle.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def _score_one(
    agent: AnalysisAgent,
    record: Dict[str, Any],
    keywords: Dict[str, float],
) -> Tuple[WeightedScoreResponse, str]:
    evidence, evidence_basis = build_scoring_evidence(record)
    authors = ", ".join(record.get("authors") or [])
    score = None
    for _ in range(2):
        score = agent.score_paper_with_keywords(
            record["title"], authors, evidence, keywords
        )
        if not _is_failed_score(score):
            break
    assert score is not None
    return score, evidence_basis


def _is_failed_score(score: WeightedScoreResponse) -> bool:
    return score.matched_domain is None or str(score.reasoning).startswith("评分失败")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, default=ROOT / "knowledge" / "index.jsonl")
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--limit", type=int, default=0, help="0 means all eligible records")
    parser.add_argument("--force", action="store_true", help="Re-score already migrated records")
    parser.add_argument(
        "--max-failure-ratio",
        type=float,
        default=0.2,
        help="Abort without writing when this fraction of attempted records fails",
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=ROOT / "data" / "run" / "rescore_history_summary.json",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not settings.DOMAIN_KEYWORD_GROUPS:
        raise SystemExit("DOMAIN_KEYWORD_GROUPS is empty; refusing to use legacy scoring")
    if args.workers < 1 or args.workers > 8:
        raise SystemExit("--workers must be between 1 and 8")

    records = _load_records(args.index)
    candidates = [
        index
        for index, record in enumerate(records)
        if args.force or (record.get("scoring") or {}).get("version") != SCORING_VERSION
    ]
    if args.limit > 0:
        candidates = candidates[: args.limit]

    if not candidates:
        print("No historical records need re-scoring")
        return 0

    print(
        f"Re-scoring {len(candidates)} of {len(records)} historical records "
        f"with {args.workers} workers"
    )
    agent = AnalysisAgent()
    keywords = settings.get_merged_keywords()
    rescored_at = datetime.now(timezone.utc).isoformat()
    successes: Dict[int, Dict[str, Any]] = {}
    failures: Dict[int, str] = {}
    evidence_counts: Dict[str, int] = {}

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(_score_one, agent, records[index], keywords): index
            for index in candidates
        }
        for completed, future in enumerate(as_completed(futures), 1):
            index = futures[future]
            record = records[index]
            try:
                score, evidence_basis = future.result()
                if _is_failed_score(score):
                    failures[index] = score.reasoning
                else:
                    successes[index] = apply_score(
                        record, score, evidence_basis, rescored_at
                    )
                    evidence_counts[evidence_basis] = evidence_counts.get(evidence_basis, 0) + 1
            except Exception as exc:
                failures[index] = str(exc)

            if completed % 10 == 0 or completed == len(candidates):
                print(
                    f"Progress {completed}/{len(candidates)} | "
                    f"success {len(successes)} | failed {len(failures)}",
                    flush=True,
                )

    failure_ratio = len(failures) / len(candidates)
    summary = {
        "scoring_version": SCORING_VERSION,
        "total_records": len(records),
        "attempted": len(candidates),
        "updated": len(successes),
        "failed": len(failures),
        "failure_ratio": round(failure_ratio, 4),
        "evidence_basis": evidence_counts,
        "failures": [
            {
                "paper_id": records[index]["paper_id"],
                "title": records[index]["title"],
                "error": error,
            }
            for index, error in failures.items()
        ],
        "rescored_at": rescored_at,
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    if failure_ratio > args.max_failure_ratio:
        print(
            f"Failure ratio {failure_ratio:.1%} exceeds {args.max_failure_ratio:.1%}; "
            "knowledge index was not changed",
            file=sys.stderr,
        )
        return 2

    for index, updated in successes.items():
        records[index] = updated
    _atomic_write_jsonl(args.index, records)
    print(f"Updated {len(successes)} records; preserved {len(failures)} failed records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
