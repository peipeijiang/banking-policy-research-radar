"""Build a domain-local preference profile and rerank research candidates."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import requests


def _cosine(left: Optional[List[float]], right: Optional[List[float]]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0
    dot = sum(a * b for a, b in zip(left, right))
    norm = math.sqrt(sum(a * a for a in left) * sum(b * b for b in right))
    return dot / norm if norm else 0.0


def _centroid(weighted_vectors: Iterable[tuple[List[float], float]]) -> List[float]:
    rows = [(vector, weight) for vector, weight in weighted_vectors if vector and weight > 0]
    if not rows:
        return []
    total = sum(weight for _, weight in rows)
    return [sum(vector[i] * weight for vector, weight in rows) / total for i in range(len(rows[0][0]))]


def _text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(_text(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(_text(item) for item in value)
    return str(value or "")


def _paper_text(record: Dict[str, Any]) -> str:
    analysis = record.get("analysis") or {}
    parts = [
        record.get("title"),
        record.get("abstract"),
        record.get("abstract_cn"),
        record.get("tldr"),
        record.get("journal"),
        record.get("topics"),
        record.get("categories"),
        record.get("authors"),
        analysis.get("summary"),
        analysis.get("methodology"),
        analysis.get("key_results"),
        analysis.get("innovations"),
    ]
    return "\n".join(_text(part).strip() for part in parts if _text(part).strip())[:6000]


def _tokens(record: Dict[str, Any]) -> set[str]:
    text = _paper_text(record).lower()
    stopwords = {
        "the", "and", "for", "with", "from", "this", "that", "using", "based",
        "paper", "study", "method", "model", "results", "使用", "首先", "最后",
        "然后", "本文", "论文", "提出", "通过", "结果", "实验", "显示", "表明",
    }
    return {
        token
        for token in re.findall(r"[a-z][a-z0-9_-]{2,}|[\u4e00-\u9fff]{2,8}", text)
        if token not in stopwords
    }


class MiniMaxEmbeddingCache:
    """Small append-only cache for MiniMax embo-01 vectors."""

    def __init__(self, path: Path, api_key: str, base_url: str, model: str):
        self.path = path
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.vectors: Dict[str, List[float]] = {}
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                try:
                    row = json.loads(line)
                    self.vectors[row["key"]] = row["vector"]
                except (json.JSONDecodeError, KeyError, TypeError):
                    continue

    def _key(self, text: str) -> str:
        return hashlib.sha256(f"{self.model}\0{text}".encode("utf-8")).hexdigest()

    def embed_many(self, texts: List[str]) -> List[List[float]]:
        keys = [self._key(text) for text in texts]
        missing = [(key, text) for key, text in zip(keys, texts) if key not in self.vectors]
        for offset in range(0, len(missing)):
            batch = missing[offset : offset + 1]
            payload = {"model": self.model, "texts": [text for _, text in batch], "type": "db"}
            response = requests.post(
                f"{self.base_url}/embeddings",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json=payload,
                timeout=45,
            )
            response.raise_for_status()
            data = response.json()
            if (data.get("base_resp") or {}).get("status_code", 0) != 0:
                raise RuntimeError(f"MiniMax embeddings rejected request: {data.get('base_resp')}")
            vectors = data.get("vectors") or []
            if len(vectors) != len(batch):
                raise RuntimeError("MiniMax embeddings returned an unexpected vector count")
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as handle:
                for (key, _), vector in zip(batch, vectors):
                    compact = [round(float(value), 7) for value in vector]
                    self.vectors[key] = compact
                    handle.write(json.dumps({"key": key, "model": self.model, "vector": compact}) + "\n")
        return [self.vectors.get(key, []) for key in keys]


class PersonalizationEngine:
    def __init__(
        self,
        root: Path = Path("knowledge/preferences"),
        enabled: bool = True,
        mode: str = "shadow",
        min_feedback: int = 3,
        max_adjustment: float = 15.0,
        negative_weight: float = 0.75,
        half_life_days: int = 90,
        diversity_lambda: float = 0.78,
        exploration_ratio: float = 0.2,
        embedding_api_key: str = "",
        embedding_base_url: str = "https://api.minimaxi.com/v1",
        embedding_model: str = "embo-01",
    ):
        self.root = root
        self.enabled = enabled
        self.mode = mode if mode in {"shadow", "live"} else "shadow"
        self.min_feedback = max(1, min_feedback)
        self.max_adjustment = max_adjustment
        self.negative_weight = negative_weight
        self.half_life_days = max(1, half_life_days)
        self.diversity_lambda = diversity_lambda
        self.exploration_ratio = exploration_ratio
        self.profile: Dict[str, Any] = {}
        self._vectors: Dict[str, List[float]] = {}
        self._records: Dict[str, Dict[str, Any]] = {}
        self._embedder = (
            MiniMaxEmbeddingCache(root / "embeddings.jsonl", embedding_api_key, embedding_base_url, embedding_model)
            if embedding_api_key
            else None
        )

    @classmethod
    def from_settings(cls, settings) -> "PersonalizationEngine":
        return cls(
            root=Path("knowledge/preferences"),
            enabled=settings.PERSONALIZATION_ENABLED,
            mode=settings.PERSONALIZATION_MODE,
            min_feedback=settings.PERSONALIZATION_MIN_FEEDBACK,
            max_adjustment=settings.PERSONALIZATION_MAX_ADJUSTMENT,
            negative_weight=settings.PERSONALIZATION_NEGATIVE_WEIGHT,
            half_life_days=settings.PERSONALIZATION_HALF_LIFE_DAYS,
            diversity_lambda=settings.PERSONALIZATION_DIVERSITY_LAMBDA,
            exploration_ratio=settings.PERSONALIZATION_EXPLORATION_RATIO,
            embedding_api_key=settings.MINIMAX_API_KEY,
            embedding_base_url=settings.EMBEDDING_BASE_URL,
            embedding_model=settings.EMBEDDING_MODEL,
        )

    @staticmethod
    def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
        if not path.exists():
            return []
        rows = []
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return rows

    def _feedback(self) -> Dict[str, Dict[str, Any]]:
        events = self._read_jsonl(self.root / "events.jsonl")
        latest = {}
        for event in sorted(events, key=lambda row: (row.get("created_at", ""), row.get("issue_number", 0))):
            latest[event.get("paper_id", "")] = event
        if latest:
            return latest
        legacy = self.root.parent / "feedback.json"
        if not legacy.exists():
            return {}
        try:
            data = json.loads(legacy.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
        now = datetime.now(timezone.utc).isoformat()
        return {
            paper_id: {"paper_id": paper_id, "action": action, "created_at": now}
            for action, key in (("LIKE", "liked"), ("IGNORE", "ignored"))
            for paper_id in data.get(key, [])
        }

    def _weight(self, created_at: str) -> float:
        try:
            then = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            if then.tzinfo is None:
                then = then.replace(tzinfo=timezone.utc)
            age = max(0.0, (datetime.now(timezone.utc) - then).total_seconds() / 86400)
            return 0.5 ** (age / self.half_life_days)
        except (TypeError, ValueError):
            return 1.0

    def _build_profile(self) -> None:
        self._records = {
            row.get("paper_id"): row
            for row in self._read_jsonl(self.root.parent / "index.jsonl")
            if row.get("paper_id")
        }
        feedback = self._feedback()
        positive, negative = [], []
        positive_terms, negative_terms = Counter(), Counter()
        for paper_id, event in feedback.items():
            record = self._records.get(paper_id)
            if not record:
                continue
            weight = self._weight(event.get("created_at", ""))
            target = positive if event.get("action") == "LIKE" else negative
            target.append((record, weight))
            counter = positive_terms if event.get("action") == "LIKE" else negative_terms
            counter.update({token: weight for token in _tokens(record)})

        references = positive + negative
        vectors = self._embedder.embed_many([_paper_text(record) for record, _ in references]) if self._embedder and references else [[] for _ in references]
        split = len(positive)
        positive_centroid = _centroid((vector, weight) for vector, (_, weight) in zip(vectors[:split], positive))
        negative_centroid = _centroid((vector, weight) for vector, (_, weight) in zip(vectors[split:], negative))
        active = len(references) >= self.min_feedback
        self.profile = {
            "version": 1,
            "mode": self.mode,
            "active": active,
            "feedback_count": len(feedback),
            "usable_feedback_count": len(references),
            "liked_count": len(positive),
            "ignored_count": len(negative),
            "embedding_enabled": bool(self._embedder),
            "positive_terms": [term for term, _ in positive_terms.most_common(20)],
            "negative_terms": [term for term, _ in negative_terms.most_common(20)],
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        self._positive = positive
        self._negative = negative
        self._positive_centroid = positive_centroid
        self._negative_centroid = negative_centroid
        self._positive_terms = set(self.profile["positive_terms"])
        self._negative_terms = set(self.profile["negative_terms"])
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / "profile.json").write_text(
            json.dumps(self.profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    def apply(self, rows: List[Dict[str, Any]]) -> None:
        if not self.enabled:
            return
        self._build_profile()
        if not self.profile.get("active"):
            for row in rows:
                base = float(row["score_response"].total_score)
                row["personalization"] = {
                    "mode": self.mode, "active": False, "base_score": base,
                    "personalized_score": base, "adjustment": 0.0,
                    "reasons": [f"冷启动：需要至少 {self.min_feedback} 条有效反馈"],
                }
            return

        records = []
        for row in rows:
            paper = row["paper_metadata"]
            record = paper.to_dict()
            record.update({"tldr": row["score_response"].tldr, "analysis": row.get("analysis")})
            records.append(record)
        vectors = self._embedder.embed_many([_paper_text(record) for record in records]) if self._embedder else [[] for _ in records]

        for row, record, vector in zip(rows, records, vectors):
            paper_id = row["paper_id"]
            self._vectors[paper_id] = vector
            base = float(row["score_response"].total_score)
            positive_similarity = _cosine(vector, self._positive_centroid)
            negative_similarity = _cosine(vector, self._negative_centroid)
            terms = _tokens(record)
            positive_overlap = len(terms & self._positive_terms) / max(1, len(self._positive_terms))
            negative_overlap = len(terms & self._negative_terms) / max(1, len(self._negative_terms))
            semantic = max(0.0, positive_similarity - 0.35) * 18
            penalty = max(0.0, negative_similarity - 0.35) * 14 * self.negative_weight
            lexical = 6 * positive_overlap - 4 * negative_overlap * self.negative_weight
            adjustment = max(-self.max_adjustment, min(self.max_adjustment, semantic - penalty + lexical))
            personalized = max(0.0, base + adjustment)
            reasons = []
            if positive_similarity > 0.45 and self._positive:
                nearest = max(self._positive, key=lambda item: len(terms & _tokens(item[0])))[0]
                reasons.append(f"接近喜欢过的《{nearest.get('title', '')[:42]}》")
            overlap = list(terms & self._positive_terms)[:3]
            if overlap:
                reasons.append("偏好主题：" + "、".join(overlap))
            if negative_similarity > positive_similarity and negative_similarity > 0.45:
                reasons.append("与忽略方向相似，已降权")
            if not reasons:
                reasons.append("个性化信号较弱，主要依据基础相关性")
            detail = {
                "mode": self.mode, "active": True, "base_score": round(base, 2),
                "personalized_score": round(personalized, 2), "adjustment": round(adjustment, 2),
                "positive_similarity": round(positive_similarity, 4),
                "negative_similarity": round(negative_similarity, 4), "reasons": reasons,
            }
            row["personalization"] = detail
            if self.mode == "live":
                row["score_response"].total_score = personalized
                row["score_response"].is_qualified = personalized >= row["score_response"].passing_score
                row["score_response"].reasoning += f"；个性化调整 {adjustment:+.1f}"

    def _mmr(self, candidates: List[Dict[str, Any]], top_n: int) -> List[Dict[str, Any]]:
        remaining = sorted(candidates, key=lambda row: row["personalization"]["personalized_score"], reverse=True)
        selected = []
        while remaining and len(selected) < top_n:
            best = max(
                remaining,
                key=lambda row: self.diversity_lambda * row["personalization"]["personalized_score"]
                - (1 - self.diversity_lambda) * 100 * max(
                    (_cosine(self._vectors.get(row["paper_id"]), self._vectors.get(item["paper_id"])) for item in selected),
                    default=0.0,
                ),
            )
            selected.append(best)
            remaining.remove(best)
        if top_n >= 5 and remaining and self.exploration_ratio > 0:
            pool = remaining[: max(3, top_n)]
            explorer = min(
                pool,
                key=lambda row: max(
                    (_cosine(self._vectors.get(row["paper_id"]), self._vectors.get(item["paper_id"])) for item in selected[:-1]),
                    default=0.0,
                ),
            )
            explorer["personalization"]["exploration"] = True
            selected[-1] = explorer
        return selected

    def rank(self, candidates: List[Dict[str, Any]], top_n: int) -> List[Dict[str, Any]]:
        base = sorted(candidates, key=lambda row: row["score"], reverse=True)[:top_n]
        if not self.enabled or not self.profile.get("active"):
            return base
        shadow = self._mmr(candidates, top_n)
        base_ids = {row["paper_id"] for row in base}
        overlap = len(base_ids & {row["paper_id"] for row in shadow})
        metrics = {
            "timestamp": datetime.now(timezone.utc).isoformat(), "mode": self.mode,
            "feedback_count": self.profile.get("feedback_count", 0),
            "top_n": top_n, "top_overlap": overlap,
            "average_adjustment": round(sum(row["personalization"]["adjustment"] for row in candidates) / max(1, len(candidates)), 3),
            "base_top": [row["paper_id"] for row in base],
            "personalized_top": [row["paper_id"] for row in shadow],
        }
        self.root.mkdir(parents=True, exist_ok=True)
        with (self.root / "metrics.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(metrics, ensure_ascii=False) + "\n")
        return shadow if self.mode == "live" else base
