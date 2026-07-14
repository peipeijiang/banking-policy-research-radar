"""Git-backed long-term paper library and citation graph."""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class ResearchLibrary:
    def __init__(self, root: Path = Path("knowledge")):
        self.root = root
        self.papers_dir = root / "papers"
        self.graph_path = root / "graph.json"
        self.index_path = root / "index.jsonl"
        self.papers_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _slug(paper_id: str) -> str:
        return re.sub(r"[^a-zA-Z0-9._-]+", "-", paper_id).strip("-")[:140]

    @staticmethod
    def _title_key(title: str) -> str:
        return re.sub(r"[^a-z0-9]+", "", (title or "").lower())

    @staticmethod
    def _record_quality(record: Dict) -> tuple:
        return (
            bool(record.get("analysis")),
            record.get("score", 0),
            bool(record.get("pdf_url")),
            len(record.get("abstract") or ""),
            record.get("updated_at", ""),
        )

    @staticmethod
    def _text(value) -> str:
        if isinstance(value, dict):
            labels = {
                "paper_limitations": "论文本身局限",
                "evidence_limitations": "当前证据局限",
            }
            return "；".join(
                f"{labels.get(key, str(key).replace('_', ' '))}：{ResearchLibrary._text(item)}"
                for key, item in value.items()
                if ResearchLibrary._text(item)
            )
        if isinstance(value, list):
            return "；".join(
                ResearchLibrary._text(item) for item in value if ResearchLibrary._text(item)
            )
        return str(value or "").strip()

    @staticmethod
    def _markdown_list(value) -> List[str]:
        if not value:
            return []
        if isinstance(value, dict):
            labels = {
                "paper_limitations": "论文本身局限",
                "evidence_limitations": "当前证据局限",
            }
            return [
                f"- **{labels.get(key, str(key).replace('_', ' '))}**：{ResearchLibrary._text(item)}"
                for key, item in value.items()
                if ResearchLibrary._text(item)
            ]
        items = value if isinstance(value, list) else [value]
        return [
            f"- {ResearchLibrary._text(item)}"
            for item in items
            if ResearchLibrary._text(item)
        ]

    @classmethod
    def _analysis_markdown(cls, analysis: Dict) -> List[str]:
        if not analysis:
            return []

        basis = analysis.get("_analysis_basis")
        basis_label = {
            "full_text": "全文深读",
            "abstract": "摘要分析",
        }.get(basis, "AI 深度分析")
        lines = ["", "## 深度解读", "", f"> 分析依据：**{basis_label}**"]
        scalar_sections = (
            ("核心结论", "summary"),
            ("研究方法", "methodology"),
            ("关键结果", "key_results"),
            ("与当前研究方向的关联", "relevance_to_keywords"),
        )
        list_sections = (
            ("主要创新", "innovations"),
            ("技术栈", "tech_stack"),
            ("方法优势", "strengths"),
            ("主要局限", "limitations"),
        )
        section_order = [
            ("scalar", scalar_sections[0]),
            ("list", list_sections[0]),
            ("scalar", scalar_sections[1]),
            ("scalar", scalar_sections[2]),
            ("list", list_sections[1]),
            ("list", list_sections[2]),
            ("list", list_sections[3]),
            ("scalar", scalar_sections[3]),
        ]
        for kind, (label, key) in section_order:
            value = analysis.get(key)
            if not value:
                continue
            lines += ["", f"### {label}", ""]
            if kind == "list":
                lines += cls._markdown_list(value)
            else:
                lines.append(cls._text(value))
        return lines

    @classmethod
    def render_record(cls, record: Dict) -> str:
        """Render a mobile-friendly GitHub Markdown research report."""
        analysis = record.get("analysis") or {}
        original_title = record.get("title") or "Untitled paper"
        display_title = analysis.get("chinese_title") or original_title
        frontmatter = {
            "title": display_title,
            "paper_id": record.get("paper_id"),
            "source": record.get("source"),
            "published": record.get("published_date"),
            "score": record.get("score", 0),
            "tags": ["paper", record.get("research_field_tag") or "academic-research"]
            + (record.get("topics") or [])[:5],
        }
        body = [
            "---",
            *[f"{key}: {json.dumps(value, ensure_ascii=False, default=str)}" for key, value in frontmatter.items()],
            "---",
            "",
            f"# {display_title}",
        ]
        if display_title != original_title:
            body += ["", f"> **英文原标题**：{original_title}"]

        links = []
        if record.get("url"):
            links.append(f"[查看原文]({record['url']})")
        if record.get("arxiv_url") and record.get("arxiv_url") != record.get("url"):
            links.append(f"[ArXiv]({record['arxiv_url']})")
        if record.get("semantic_scholar_url"):
            links.append(f"[Semantic Scholar]({record['semantic_scholar_url']})")
        if links:
            body += ["", " · ".join(links)]

        tldr = cls._text(record.get("tldr"))
        if tldr:
            body += ["", "## 一句话结论", "", f"> {tldr}"]

        authors = ", ".join(record.get("authors") or []) or "-"
        published = cls._text(record.get("published_date")).split("T", 1)[0] or "-"
        doi = cls._text(record.get("doi"))
        doi_text = f"[{doi}]({doi})" if doi.startswith(("http://", "https://")) else doi or "-"
        body += [
            "",
            "## 论文信息",
            "",
            f"- **作者**：{authors}",
            f"- **来源**：{cls._text(record.get('journal') or record.get('source')) or '-'}",
            f"- **发布时间**：{published}",
            f"- **相关度评分**：{float(record.get('score') or 0):.1f}",
            f"- **DOI**：{doi_text}",
        ]

        domain_scores = record.get("domain_scores") or {}
        if domain_scores:
            domain_labels = {
                "commercial_banking": "商业银行",
                "monetary_policy": "货币政策",
                "fiscal_policy": "财政政策",
            }
            matched_domain = record.get("matched_domain")
            body += ["", "## 相关性评分", ""]
            for domain_id, domain_score in domain_scores.items():
                label = domain_labels.get(domain_id, domain_id)
                marker = "（最高匹配）" if domain_id == matched_domain else ""
                body.append(f"- **{label}**：{float(domain_score):.1f}/10{marker}")
            scoring = record.get("scoring") or {}
            if scoring.get("evidence_basis"):
                evidence_labels = {
                    "abstract": "论文摘要",
                    "existing_analysis": "已有深度分析",
                    "existing_tldr": "已有一句话摘要",
                    "title_only": "仅论文标题",
                }
                body.append(
                    f"- **评分依据**：{evidence_labels.get(scoring['evidence_basis'], scoring['evidence_basis'])}"
                )
            if record.get("score_reasoning"):
                body += ["", f"> {cls._text(record['score_reasoning'])}"]

        abstract_cn = cls._text(record.get("abstract_cn"))
        abstract = cls._text(record.get("abstract"))
        if abstract_cn:
            body += [
                "",
                "<details open>",
                "<summary><strong>中文摘要</strong></summary>",
                "",
                abstract_cn,
                "",
                "</details>",
            ]
        if abstract:
            body += [
                "",
                "<details>",
                "<summary><strong>英文摘要</strong></summary>",
                "",
                abstract,
                "",
                "</details>",
            ]

        body += cls._analysis_markdown(analysis)

        repositories = record.get("code_repositories") or []
        if repositories:
            body += ["", "## 代码与复现", ""]
            for repo in repositories:
                classification = repo.get("classification") or "possible"
                confidence = repo.get("confidence")
                confidence_text = f"，置信度 {confidence}" if confidence is not None else ""
                body.append(
                    f"- [{repo.get('full_name')}]({repo.get('url')})："
                    f"{classification}{confidence_text}，Stars {repo.get('stars', 0)}"
                )

        discovery = record.get("discovery") or {}
        if discovery:
            body += [
                "",
                "<details>",
                "<summary><strong>发现与关联证据</strong></summary>",
                "",
            ]
            for key, value in discovery.items():
                body.append(f"- **{key}**：{cls._text(value)}")
            body += ["", "</details>"]

        body += [
            "",
            "---",
            "",
            f"_知识库更新时间：{record.get('updated_at') or '-'}_",
        ]
        return "\n".join(body) + "\n"

    def write_record(self, record: Dict) -> Path:
        path = self.papers_dir / f"{self._slug(record['paper_id'])}.md"
        path.write_text(self.render_record(record), encoding="utf-8")
        return path

    def persist(self, scored_by_source: Dict, analyses_by_source: Dict) -> int:
        analysis_map = {
            row["paper_id"]: row.get("analysis")
            for rows in analyses_by_source.values()
            for row in rows
        }
        records_by_id: Dict[str, Dict] = {}
        if self.index_path.exists():
            for line in self.index_path.read_text(encoding="utf-8").splitlines():
                try:
                    existing = json.loads(line)
                    records_by_id[existing["paper_id"]] = existing
                except (json.JSONDecodeError, KeyError):
                    continue
        graph = {"nodes": {}, "edges": []}
        if self.graph_path.exists():
            graph = json.loads(self.graph_path.read_text(encoding="utf-8"))

        for source, rows in scored_by_source.items():
            for row in rows:
                from config import settings

                paper = row["paper_metadata"]
                score = row["score_response"]
                domain_scores = getattr(score, "domain_scores", {})
                matched_domain = getattr(score, "matched_domain", None)
                record = paper.to_dict()
                record.update(
                    {
                        "source": source,
                        "score": score.total_score,
                        "domain_scores": domain_scores,
                        "matched_domain": matched_domain,
                        "matched_domain_label": settings.DOMAIN_KEYWORD_GROUPS.get(
                            matched_domain or "", {}
                        ).get("label"),
                        "qualified": score.is_qualified,
                        "tldr": score.tldr,
                        "abstract_cn": row.get("abstract_cn", ""),
                        "analysis": analysis_map.get(paper.paper_id),
                        "research_field": settings.RESEARCH_FIELD_NAME,
                        "research_field_tag": settings.RESEARCH_FIELD_TAG,
                        "personalization": row.get("personalization", {}),
                        "base_score": (row.get("personalization") or {}).get(
                            "base_score", score.total_score
                        ),
                        "updated_at": datetime.now().isoformat(),
                    }
                )
                self.write_record(record)
                records_by_id[paper.paper_id] = record
                graph["nodes"][paper.openalex_id or paper.paper_id] = {"title": paper.title, "paper_id": paper.paper_id}
                source_id = paper.openalex_id or paper.paper_id
                graph["edges"] = [edge for edge in graph["edges"] if edge.get("from") != source_id]
                graph["edges"] += [{"from": source_id, "to": target, "type": "cites"} for target in paper.referenced_works]
                graph["edges"] += [{"from": source_id, "to": target, "type": "related"} for target in paper.related_works]

        records_by_title: Dict[str, Dict] = {}
        duplicate_records = []
        for record in records_by_id.values():
            title_key = self._title_key(record.get("title", "")) or record["paper_id"]
            existing = records_by_title.get(title_key)
            if not existing or self._record_quality(record) > self._record_quality(existing):
                if existing:
                    duplicate_records.append(existing)
                records_by_title[title_key] = record
            else:
                duplicate_records.append(record)

        duplicate_node_ids = set()
        for record in duplicate_records:
            duplicate_node_ids.add(record.get("openalex_id") or record["paper_id"])
            duplicate_path = self.papers_dir / f"{self._slug(record['paper_id'])}.md"
            if duplicate_path.exists():
                duplicate_path.unlink()
        for node_id in duplicate_node_ids:
            graph["nodes"].pop(node_id, None)
        graph["edges"] = [
            edge for edge in graph["edges"]
            if edge.get("from") not in duplicate_node_ids and edge.get("to") not in duplicate_node_ids
        ]

        with self.index_path.open("w", encoding="utf-8") as handle:
            for record in sorted(records_by_title.values(), key=lambda item: item.get("updated_at", "")):
                handle.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
        self.graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
        return sum(len(rows) for rows in scored_by_source.values())
