#!/usr/bin/env python3
"""Resend the latest complete research batch from the local knowledge index."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from notifications.notifier import NotifierAgent, RunResult, WebhookNotifier  # noqa: E402
from config import settings  # noqa: E402


def load_records(index_path: Path) -> list[dict]:
    records = []
    for line_number, line in enumerate(index_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSON at {index_path}:{line_number}: {exc}") from exc
    return records


def batch_key(record: dict) -> str:
    """Group records written by one run, whose timestamps differ by milliseconds."""
    return str(record.get("updated_at") or "")[:16]


def select_latest_complete_batch(records: list[dict], top_n: int) -> tuple[str, list[dict]]:
    batches: dict[str, list[dict]] = {}
    for record in records:
        key = batch_key(record)
        if key:
            batches.setdefault(key, []).append(record)

    complete = []
    for key, batch in batches.items():
        analyzed = [item for item in batch if item.get("qualified") and item.get("analysis")]
        if len(analyzed) >= top_n:
            complete.append((key, batch))
    if not complete:
        raise SystemExit(f"No stored batch contains at least {top_n} analyzed papers")
    return max(complete, key=lambda item: item[0])


def build_result(key: str, batch: list[dict], top_n: int) -> RunResult:
    top_papers = sorted(
        (item for item in batch if item.get("qualified") and item.get("analysis")),
        key=lambda item: float(item.get("score") or 0),
        reverse=True,
    )[:top_n]
    fetched = Counter(str(item.get("source") or "unknown") for item in batch)
    qualified = Counter(
        str(item.get("source") or "unknown") for item in batch if item.get("qualified")
    )
    analyzed = Counter(
        str(item.get("source") or "unknown")
        for item in batch
        if item.get("qualified") and item.get("analysis")
    )
    timestamp = datetime.fromisoformat(key).strftime("%Y-%m-%d %H:%M")
    return RunResult(
        run_timestamp=f"{timestamp}（知识库重发）",
        total_papers_fetched=len(batch),
        papers_by_source=dict(fetched),
        qualified_by_source=dict(qualified),
        analyzed_by_source=dict(analyzed),
        total_qualified=sum(qualified.values()),
        total_analyzed=sum(analyzed.values()),
        top_papers=top_papers,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Resend the latest complete paper batch without fetching new papers."
    )
    parser.add_argument("--top", type=int, default=5, help="Number of top papers to resend")
    parser.add_argument(
        "--webhook-url",
        default=os.getenv("WECHAT_WEBHOOK_URL", ""),
        help="WeCom webhook; defaults to WECHAT_WEBHOOK_URL",
    )
    parser.add_argument(
        "--index", type=Path, default=ROOT / "knowledge" / "index.jsonl"
    )
    parser.add_argument("--dry-run", action="store_true", help="Print cards without sending")
    args = parser.parse_args()

    if args.top < 1:
        parser.error("--top must be at least 1")
    if not args.index.exists():
        raise SystemExit(f"Knowledge index not found: {args.index}")
    if not args.dry_run and not args.webhook_url:
        raise SystemExit("Set WECHAT_WEBHOOK_URL or pass --webhook-url")

    records = load_records(args.index)
    key, batch = select_latest_complete_batch(records, args.top)
    result = build_result(key, batch, args.top)
    formatter = NotifierAgent.__new__(NotifierAgent)
    formatter.settings = settings
    messages = [formatter._format_wechat_overview(result)]
    for index, paper in enumerate(result.top_papers, 1):
        messages.extend(formatter._format_wechat_paper_cards(paper, index, len(result.top_papers)))

    if args.dry_run:
        for index, message in enumerate(messages, 1):
            print(f"\n--- message {index}/{len(messages)} ({len(message.encode('utf-8'))} bytes) ---")
            print(message)
        return 0

    notifier = WebhookNotifier("wechat_work", args.webhook_url)
    subject = f"{settings.RESEARCH_FIELD_NAME}每日研究（知识库重发）"
    for index, message in enumerate(messages, 1):
        notifier.send(subject, message)
        print(f"Sent message {index}/{len(messages)}")
        if index < len(messages):
            time.sleep(0.4)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
