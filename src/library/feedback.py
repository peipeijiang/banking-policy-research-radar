import json
from pathlib import Path


class FeedbackStore:
    def __init__(self, path: Path = Path("knowledge/feedback.json")):
        self.path = path
        self.data = {"liked": [], "ignored": []}
        if path.exists():
            self.data.update(json.loads(path.read_text(encoding="utf-8")))

    def is_ignored(self, paper_id: str) -> bool:
        return paper_id in self.data.get("ignored", [])

    def apply(self, paper_id: str, score_response) -> None:
        if paper_id in self.data.get("liked", []):
            score_response.reasoning += "；用户历史反馈：喜欢（交由个性化引擎计算）"
