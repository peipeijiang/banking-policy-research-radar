#!/usr/bin/env python3
"""Resend the latest complete knowledge batch through configured notifiers."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from notifications.notifier import NotifierAgent  # noqa: E402
from resend_last_wechat import (  # noqa: E402
    build_result,
    load_records,
    select_latest_complete_batch,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Resend stored research without fetching or LLM analysis."
    )
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument(
        "--index", type=Path, default=ROOT / "knowledge" / "index.jsonl"
    )
    parser.add_argument("--full-text-only", action="store_true")
    parser.add_argument("--batch-date", default="", help="Batch date in YYYY-MM-DD")
    parser.add_argument(
        "--allow-fewer",
        action="store_true",
        help="Send all eligible papers when fewer than --top are available",
    )
    args = parser.parse_args()
    if args.top < 1:
        parser.error("--top must be at least 1")

    records = load_records(args.index)
    key, batch = select_latest_complete_batch(
        records,
        args.top,
        full_text_only=args.full_text_only,
        batch_date=args.batch_date,
        allow_fewer=args.allow_fewer,
    )
    result = build_result(
        key, batch, args.top, full_text_only=args.full_text_only
    )
    if not NotifierAgent().notify(result):
        raise SystemExit("Notification delivery failed")
    print(f"Resent batch {key}: {len(result.top_papers)} papers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
