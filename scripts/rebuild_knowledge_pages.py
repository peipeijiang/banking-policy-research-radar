#!/usr/bin/env python3
"""Rebuild paper Markdown pages from the durable JSONL knowledge index."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from library.research_library import ResearchLibrary  # noqa: E402


def main() -> int:
    library = ResearchLibrary(ROOT / "knowledge")
    if not library.index_path.exists():
        raise SystemExit(f"Knowledge index not found: {library.index_path}")

    count = 0
    for line_number, line in enumerate(
        library.index_path.read_text(encoding="utf-8").splitlines(), 1
    ):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSON at line {line_number}: {exc}") from exc
        library.write_record(record)
        count += 1
    print(f"Rebuilt {count} mobile-friendly paper reports")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
