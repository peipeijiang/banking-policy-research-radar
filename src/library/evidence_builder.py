"""Create traceable evidence packs and validate weekly narrative citations."""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


def build_evidence_pack(records: List[Dict], root: Path = Path("knowledge/evidence")) -> Dict:
    root.mkdir(parents=True, exist_ok=True)
    claims = []
    papers = []
    for paper_index, row in enumerate(records, 1):
        paper_ref = f"P{paper_index:02d}"
        paper_claims = []
        if row.get("tldr"):
            paper_claims.append(("paper_summary", row["tldr"], "AI paper-level summary"))
        if row.get("cited_by_count") is not None:
            paper_claims.append(
                ("metadata", f"OpenAlex citation count: {row.get('cited_by_count', 0)}", "OpenAlex metadata")
            )
        for repo in row.get("code_repositories", [])[:2]:
            paper_claims.append(
                (
                    "code_repository",
                    f"Code candidate {repo.get('full_name')} is classified {repo.get('classification')} with confidence {repo.get('confidence')}",
                    repo.get("url", ""),
                )
            )
        claim_ids = []
        for claim_index, (kind, text, location) in enumerate(paper_claims, 1):
            claim_id = f"{paper_ref}-C{claim_index:02d}"
            claim_ids.append(claim_id)
            claims.append(
                {
                    "claim_id": claim_id,
                    "paper_id": row["paper_id"],
                    "paper_ref": paper_ref,
                    "kind": kind,
                    "text": text,
                    "location": location,
                    "source_url": row.get("url", ""),
                }
            )
        papers.append(
            {
                "paper_ref": paper_ref,
                "paper_id": row["paper_id"],
                "title": row.get("title"),
                "url": row.get("url"),
                "topics": row.get("topics", [])[:5],
                "score": row.get("score"),
                "discovery": row.get("discovery", {}),
                "claim_ids": claim_ids,
            }
        )
    pack = {"generated_at": datetime.now().isoformat(), "papers": papers, "claims": claims}
    path = root / f"weekly-{datetime.now():%Y-W%W}.json"
    path.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return pack


def audit_weekly_digest(content: str, evidence_pack: Dict) -> Tuple[bool, List[str]]:
    valid_claims = {claim["claim_id"] for claim in evidence_pack.get("claims", [])}
    errors = []
    tagged_lines = [line.strip() for line in content.splitlines() if re.match(r"^\[(论文事实|跨论文观察|AI推断)\]", line.strip())]
    if not tagged_lines:
        errors.append("没有使用[论文事实]/[跨论文观察]/[AI推断]标签")
    for line in tagged_lines:
        cited = re.findall(r"\[(P\d{2}-C\d{2})\]", line)
        unknown = [claim for claim in cited if claim not in valid_claims]
        if unknown:
            errors.append(f"不存在的证据ID: {', '.join(unknown)}")
        if line.startswith("[论文事实]") and not cited:
            errors.append("论文事实缺少证据ID")
        if line.startswith("[跨论文观察]"):
            paper_refs = {claim.split("-")[0] for claim in cited}
            if len(paper_refs) < 2:
                errors.append("跨论文观察至少需要两篇不同论文")
    return not errors, errors
