#!/usr/bin/env python3
"""Reanalyze one stored paper from a verified full-text PDF URL."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agents.analysis_agent import AnalysisAgent  # noqa: E402
from library.research_library import ResearchLibrary  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-id", required=True)
    parser.add_argument("--pdf-url", required=True)
    parser.add_argument("--provider", default="manual_verified_open_access")
    args = parser.parse_args()

    library = ResearchLibrary(ROOT / "knowledge")
    records = [
        json.loads(line)
        for line in library.index_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    record = next((item for item in records if item.get("paper_id") == args.paper_id), None)
    if not record:
        raise SystemExit(f"Paper not found: {args.paper_id}")

    analysis = AnalysisAgent().deep_analyze(
        title=record.get("title", ""),
        pdf_url=args.pdf_url,
        abstract=record.get("abstract", ""),
        fallback_to_abstract=False,
    )
    if not analysis or analysis.get("_analysis_basis") != "full_text":
        raise SystemExit("Full-text analysis failed; knowledge was not modified")

    record["pdf_url"] = args.pdf_url
    record["fulltext_provenance"] = {
        "provider": args.provider,
        "pdf_url": args.pdf_url,
    }
    record["analysis"] = analysis
    record["updated_at"] = datetime.now().isoformat()
    library.write_record(record)

    temp_index = library.index_path.with_suffix(".jsonl.tmp")
    with temp_index.open("w", encoding="utf-8") as handle:
        for item in records:
            handle.write(json.dumps(item, ensure_ascii=False, default=str) + "\n")
    temp_index.replace(library.index_path)

    print(f"Updated {args.paper_id}: full_text")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
