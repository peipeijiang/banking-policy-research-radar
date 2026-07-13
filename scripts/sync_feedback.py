#!/usr/bin/env python3
"""Synchronize WeCom feedback issues into the local preference store."""

import json
import os
import re
from pathlib import Path

import requests


def parse_feedback(issues):
    liked, ignored = set(), set()
    for issue in sorted(issues, key=lambda item: item.get("number", 0)):
        match = re.match(r"^\[(LIKE|IGNORE)\]\s+(.+)$", issue.get("title", "").strip())
        if not match:
            continue
        action, paper_id = match.groups()
        liked.discard(paper_id)
        ignored.discard(paper_id)
        (liked if action == "LIKE" else ignored).add(paper_id)
    return {"liked": sorted(liked), "ignored": sorted(ignored)}


def parse_events(issues):
    events = []
    for issue in sorted(issues, key=lambda item: item.get("number", 0)):
        match = re.match(r"^\[(LIKE|IGNORE)\]\s+(.+)$", issue.get("title", "").strip())
        if not match:
            continue
        action, paper_id = match.groups()
        events.append(
            {
                "event_id": f"github-issue-{issue.get('number')}",
                "issue_number": issue.get("number", 0),
                "action": action,
                "paper_id": paper_id,
                "created_at": issue.get("created_at") or "",
                "source": "github_issue",
            }
        )
    return events


def main():
    token = os.environ.get("GITHUB_TOKEN", "")
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    if not token or not repository:
        print("GitHub credentials unavailable; keeping existing feedback.")
        return
    issues = []
    for page in range(1, 101):
        response = requests.get(
            f"https://api.github.com/repos/{repository}/issues",
            headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
            params={"state": "all", "labels": "paper-feedback", "per_page": 100, "page": page},
            timeout=30,
        )
        response.raise_for_status()
        batch = response.json()
        issues.extend(item for item in batch if "pull_request" not in item)
        if len(batch) < 100:
            break
    path = Path("knowledge/feedback.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(parse_feedback(issues), ensure_ascii=False, indent=2) + "\n")
    events_path = Path("knowledge/preferences/events.jsonl")
    events_path.parent.mkdir(parents=True, exist_ok=True)
    events_path.write_text(
        "".join(json.dumps(event, ensure_ascii=False) + "\n" for event in parse_events(issues)),
        encoding="utf-8",
    )
    print(f"Synchronized {len(issues)} feedback events into {path} and {events_path}")


if __name__ == "__main__":
    main()
