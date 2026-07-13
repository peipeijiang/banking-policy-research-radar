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


def main():
    token = os.environ.get("GITHUB_TOKEN", "")
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    if not token or not repository:
        print("GitHub credentials unavailable; keeping existing feedback.")
        return
    response = requests.get(
        f"https://api.github.com/repos/{repository}/issues",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
        params={"state": "all", "labels": "paper-feedback", "per_page": 100},
        timeout=30,
    )
    response.raise_for_status()
    path = Path("knowledge/feedback.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(parse_feedback(response.json()), ensure_ascii=False, indent=2) + "\n")
    print(f"Synchronized feedback into {path}")


if __name__ == "__main__":
    main()
