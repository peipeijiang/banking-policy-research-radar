#!/usr/bin/env python3
"""Build and optionally deliver a seven-day research synthesis."""

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from openai import OpenAI

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from config import settings
from library import build_evidence_pack, audit_weekly_digest


def recent_records(path=Path("knowledge/index.jsonl"), days=7):
    if not path.exists():
        return []
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    records = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            row = json.loads(line)
            updated = datetime.fromisoformat(row["updated_at"]).replace(tzinfo=timezone.utc)
            if updated >= cutoff and row.get("qualified"):
                records[row["paper_id"]] = row
        except (ValueError, KeyError, json.JSONDecodeError):
            continue
    return sorted(records.values(), key=lambda row: row.get("score", 0), reverse=True)


def personalization_summary(root=Path("knowledge/preferences")):
    try:
        profile = json.loads((root / "profile.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "## 个性化学习\n\n本周尚未形成有效偏好画像。"
    metrics = []
    if (root / "metrics.jsonl").exists():
        for line in (root / "metrics.jsonl").read_text(encoding="utf-8").splitlines()[-7:]:
            try:
                metrics.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    overlap = (
        sum(row.get("top_overlap", 0) for row in metrics) / len(metrics) if metrics else 0
    )
    positive = "、".join(profile.get("positive_terms", [])[:8]) or "暂无"
    negative = "、".join(profile.get("negative_terms", [])[:8]) or "暂无"
    return (
        "## 个性化学习\n\n"
        f"- 当前模式：{profile.get('mode', 'shadow')}\n"
        f"- 有效反馈：{profile.get('usable_feedback_count', 0)} 条"
        f"（喜欢 {profile.get('liked_count', 0)} / 忽略 {profile.get('ignored_count', 0)}）\n"
        f"- 正向偏好主题：{positive}\n"
        f"- 负向偏好主题：{negative}\n"
        f"- 最近影子排序与基础 Top N 平均重合：{overlap:.1f} 篇\n"
    )


def main():
    records = recent_records()
    if not records:
        print("No qualified papers found for this week.")
        return
    evidence_pack = build_evidence_pack(records[:50])
    prompt = f"""你是{settings.RESEARCH_FIELD_NAME}研究负责人。只能依据给定证据包输出中文周报 Markdown。
必须包含：本周三大研究主题、方法与技术演进、代表论文、已验证代码仓库、研究空白、下周阅读优先级。

证据规则：
1. 每个关键判断单独一行，并以[论文事实]、[跨论文观察]或[AI推断]开头。
2. [论文事实]必须在同一行引用至少一个证据ID，如[P01-C01]。
3. [跨论文观察]必须在同一行引用至少两篇不同论文的证据ID。
4. [AI推断]必须明确不确定性，不得伪装成作者结论；可以不引用证据。
5. 不得创造证据ID、实验数字、官方代码身份或论文未提供的信息。
6. 代码仓库必须写明official、likely或possible及置信度。
7. 内容精炼，每条带证据的陈述保持在一行内。\n\n证据包：\n"""
    client = OpenAI(api_key=settings.SMART_LLM.api_key, base_url=settings.SMART_LLM.base_url)
    response = client.chat.completions.create(
        model=settings.SMART_LLM.model_name,
        temperature=settings.SMART_LLM.temperature,
        messages=[{"role": "user", "content": prompt + json.dumps(evidence_pack, ensure_ascii=False)}],
    )
    content = response.choices[0].message.content
    valid, errors = audit_weekly_digest(content, evidence_pack)
    if not valid:
        repair_prompt = (
            prompt
            + json.dumps(evidence_pack, ensure_ascii=False)
            + "\n\n上一版周报：\n"
            + content
            + "\n\n审计错误：\n- "
            + "\n- ".join(errors)
            + "\n请修复所有错误并输出完整周报，不要解释修改过程。"
        )
        repaired = client.chat.completions.create(
            model=settings.SMART_LLM.model_name,
            temperature=0.1,
            messages=[{"role": "user", "content": repair_prompt}],
        )
        content = repaired.choices[0].message.content
        valid, errors = audit_weekly_digest(content, evidence_pack)
        if not valid:
            raise RuntimeError(f"Weekly evidence audit failed after repair: {errors}")
    now = datetime.now()
    path = Path("knowledge/reports/weekly") / f"{now:%Y}-W{now:%W}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    evidence_index = "\n".join(
        f"- [{claim['claim_id']}] [{claim['paper_id']}]({claim['source_url']}) · {claim['kind']}"
        for claim in evidence_pack["claims"]
    )
    preference_section = personalization_summary()
    path.write_text(
        f"# {settings.RESEARCH_FIELD_NAME}研究周报 {now:%Y-%m-%d}\n\n{content}\n\n"
        f"{preference_section}\n\n## 证据索引\n\n{evidence_index}\n",
        encoding="utf-8",
    )

    webhook = os.getenv("WECHAT_WEBHOOK_URL", "")
    if webhook:
        repo_url = os.getenv("FEEDBACK_REPO_URL", "")
        report_url = f"{repo_url}/blob/main/{path}" if repo_url else ""
        summary = content[:3000]
        if report_url:
            summary += f"\n\n[查看完整周报]({report_url})"
        result = requests.post(webhook, json={"msgtype": "markdown", "markdown": {"content": summary}}, timeout=30)
        result.raise_for_status()
    print(f"Weekly digest written to {path}")


if __name__ == "__main__":
    main()
