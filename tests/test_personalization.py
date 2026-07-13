import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from personalization import PersonalizationEngine


class FakeEmbedder:
    @staticmethod
    def embed_many(texts):
        vectors = []
        for text in texts:
            lowered = text.lower()
            if "graph" in lowered:
                vectors.append([1.0, 0.0, 0.0])
            elif "causal" in lowered:
                vectors.append([0.0, 1.0, 0.0])
            else:
                vectors.append([0.0, 0.0, 1.0])
        return vectors


class Paper:
    def __init__(self, paper_id, title, abstract):
        self.paper_id = paper_id
        self.title = title
        self.abstract = abstract

    def to_dict(self):
        return {"paper_id": self.paper_id, "title": self.title, "abstract": self.abstract}


def scored_row(paper_id, title, abstract, score):
    return {
        "paper_id": paper_id,
        "paper_metadata": Paper(paper_id, title, abstract),
        "score_response": SimpleNamespace(
            total_score=score,
            passing_score=50.0,
            is_qualified=score >= 50,
            reasoning="base",
            tldr="summary",
        ),
    }


class PersonalizationTests(unittest.TestCase):
    def test_shadow_profile_scores_without_changing_base_score(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "knowledge" / "preferences"
            root.mkdir(parents=True)
            records = [
                {"paper_id": "liked-1", "title": "Graph recommendation one", "abstract": "graph"},
                {"paper_id": "liked-2", "title": "Graph recommendation two", "abstract": "graph"},
                {"paper_id": "ignored-1", "title": "Causal ranking", "abstract": "causal"},
            ]
            (root.parent / "index.jsonl").write_text(
                "".join(json.dumps(row) + "\n" for row in records), encoding="utf-8"
            )
            events = [
                {"paper_id": "liked-1", "action": "LIKE", "created_at": "2026-07-01T00:00:00Z"},
                {"paper_id": "liked-2", "action": "LIKE", "created_at": "2026-07-02T00:00:00Z"},
                {"paper_id": "ignored-1", "action": "IGNORE", "created_at": "2026-07-03T00:00:00Z"},
            ]
            (root / "events.jsonl").write_text(
                "".join(json.dumps(row) + "\n" for row in events), encoding="utf-8"
            )
            engine = PersonalizationEngine(root=root, mode="shadow", min_feedback=3)
            engine._embedder = FakeEmbedder()
            rows = [
                scored_row("graph-new", "New graph recommender", "graph", 60),
                scored_row("causal-new", "New causal ranker", "causal", 60),
            ]

            engine.apply(rows)

            self.assertTrue(engine.profile["active"])
            self.assertEqual(rows[0]["score_response"].total_score, 60)
            self.assertGreater(
                rows[0]["personalization"]["personalized_score"],
                rows[1]["personalization"]["personalized_score"],
            )
            self.assertTrue((root / "profile.json").exists())

    def test_live_mode_applies_personalized_score(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "knowledge" / "preferences"
            root.mkdir(parents=True)
            (root.parent / "index.jsonl").write_text(
                json.dumps({"paper_id": "liked", "title": "Graph recommendation", "abstract": "graph"}) + "\n",
                encoding="utf-8",
            )
            (root / "events.jsonl").write_text(
                json.dumps({"paper_id": "liked", "action": "LIKE", "created_at": "2026-07-01T00:00:00Z"}) + "\n",
                encoding="utf-8",
            )
            engine = PersonalizationEngine(root=root, mode="live", min_feedback=1)
            engine._embedder = FakeEmbedder()
            row = scored_row("new", "Graph retrieval", "graph", 45)

            engine.apply([row])

            self.assertGreater(row["score_response"].total_score, 45)
            self.assertTrue(row["score_response"].is_qualified)


if __name__ == "__main__":
    unittest.main()
