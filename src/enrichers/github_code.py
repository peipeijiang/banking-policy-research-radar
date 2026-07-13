"""Find likely official code repositories for research papers."""

import os
import re
import base64
from typing import Dict, List
from urllib.parse import quote

import requests


class GitHubCodeEnricher:
    API_URL = "https://api.github.com/search/repositories"
    REPO_API_URL = "https://api.github.com/repos"

    def __init__(self, token: str = None):
        self.session = requests.Session()
        self._readme_cache: Dict[str, str] = {}
        token = token or os.getenv("GITHUB_TOKEN", "")
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
        self.session.headers.update(
            {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
        )

    @staticmethod
    def _tokens(title: str) -> set:
        return {
            token
            for token in re.findall(r"[a-z0-9]+", title.lower())
            if len(token) >= 4 and token not in {"with", "from", "using", "based", "towards"}
        }

    @staticmethod
    def _classification(score: int, authority_evidence: bool = False) -> str:
        if score >= 70 and authority_evidence:
            return "official"
        if score >= 40:
            return "likely"
        return "possible"

    def _readme(self, full_name: str) -> str:
        if full_name in self._readme_cache:
            return self._readme_cache[full_name]
        try:
            response = self.session.get(f"{self.REPO_API_URL}/{full_name}/readme", timeout=20)
            if response.status_code == 404:
                return ""
            response.raise_for_status()
            readme = base64.b64decode(response.json().get("content", "")).decode(
                "utf-8", errors="ignore"
            )
            self._readme_cache[full_name] = readme
            return readme
        except (requests.RequestException, ValueError):
            return ""

    def find_paper_pdf(self, full_name: str, title: str) -> Dict:
        """Return a paper PDF explicitly linked by a title-matched repository README."""
        readme = self._readme(full_name)
        title_tokens = self._tokens(title)
        overlap = len(title_tokens & self._tokens(readme)) / max(len(title_tokens), 1)
        if overlap < 0.8:
            return {}

        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", readme)
        for label, href in links:
            clean_href = href.strip().split("#", 1)[0]
            if "paper" not in label.lower() and not re.search(r"\.pdf$", clean_href, re.I):
                continue
            if clean_href.startswith(("http://", "https://")):
                if "github.com" not in clean_href and "raw.githubusercontent.com" not in clean_href:
                    continue
                return {
                    "pdf_url": clean_href,
                    "provider": "github_author_repository",
                    "repository": full_name,
                }

            relative_path = re.sub(r"^\./", "", clean_href).lstrip("/")
            if not relative_path.lower().endswith(".pdf"):
                continue
            candidate_paths = [relative_path]
            if relative_path.startswith("blob/"):
                candidate_paths.append(relative_path.removeprefix("blob/"))
            for path in candidate_paths:
                try:
                    response = self.session.get(
                        f"{self.REPO_API_URL}/{full_name}/contents/{quote(path)}", timeout=20
                    )
                    if response.status_code == 404:
                        continue
                    response.raise_for_status()
                    download_url = response.json().get("download_url")
                    if download_url:
                        return {
                            "pdf_url": download_url,
                            "provider": "github_author_repository",
                            "repository": full_name,
                        }
                except (requests.RequestException, ValueError):
                    continue
        return {}

    @staticmethod
    def can_supply_paper_pdf(repository: Dict) -> bool:
        """Require identity evidence stronger than a generic title match."""
        if repository.get("classification") in {"official", "likely"}:
            return True
        strong_evidence = {
            "paper_declared_url",
            "arxiv_id_in_readme",
            "doi_in_readme",
            "author_owner_match",
        }
        return any(
            item.get("type") in strong_evidence
            for item in repository.get("evidence", [])
        )

    def _verify(
        self, item: Dict, title: str, authors: List[str], arxiv_id: str, doi: str, declared: bool = False
    ) -> Dict:
        readme = self._readme(item.get("full_name", ""))
        normalized_readme = readme.lower()
        evidence = []
        score = 0
        if declared:
            score += 70
            evidence.append({"type": "paper_declared_url", "value": item.get("html_url")})
        if arxiv_id and arxiv_id.lower() in normalized_readme:
            score += 50
            evidence.append({"type": "arxiv_id_in_readme", "value": arxiv_id})
        clean_doi = (doi or "").lower().replace("https://doi.org/", "")
        if clean_doi and clean_doi in normalized_readme:
            score += 50
            evidence.append({"type": "doi_in_readme", "value": clean_doi})
        title_tokens = self._tokens(title)
        overlap = len(title_tokens & self._tokens(readme)) / max(len(title_tokens), 1)
        if overlap >= 0.8:
            score += 30
            evidence.append({"type": "title_in_readme", "overlap": round(overlap, 2)})
        elif overlap >= 0.4:
            score += 15
            evidence.append({"type": "partial_title_in_readme", "overlap": round(overlap, 2)})
        owner = (item.get("owner") or {}).get("login", "").lower()
        author_tokens = {part.lower() for name in authors for part in re.findall(r"[a-z]+", name) if len(part) > 3}
        author_owner_match = owner and any(token in owner for token in author_tokens)
        if author_owner_match:
            score += 20
            evidence.append({"type": "author_owner_match", "owner": owner})
        authority_evidence = declared or bool(author_owner_match)
        repository_text = f"{item.get('full_name', '')} {item.get('description') or ''}".lower()
        collection_markers = ("survey", "awesome", "paper-list", "paper list", "collection of works")
        repo_name = (item.get("full_name") or "").rsplit("/", 1)[-1].lower()
        looks_like_paper_collection = repo_name.endswith(("-papers", "_papers"))
        if not authority_evidence and (
            any(marker in repository_text for marker in collection_markers)
            or looks_like_paper_collection
        ):
            evidence.append({"type": "bibliography_collection"})
            return {"confidence": 0, "classification": "rejected", "evidence": evidence}
        confidence = min(score, 100) if authority_evidence else min(score, 69)
        return {
            "confidence": confidence,
            "classification": self._classification(confidence, authority_evidence),
            "evidence": evidence,
        }

    def find(
        self,
        title: str,
        authors: List[str] = None,
        arxiv_id: str = None,
        doi: str = None,
        abstract: str = "",
        max_results: int = 3,
    ) -> List[Dict]:
        query = f'"{title[:180]}" in:readme'
        try:
            response = self.session.get(
                self.API_URL,
                params={"q": query, "sort": "stars", "order": "desc", "per_page": 10},
                timeout=20,
            )
            if response.status_code in (403, 429):
                return []
            response.raise_for_status()
        except requests.RequestException:
            return []

        items = response.json().get("items", [])
        declared_names = {
            match.rstrip("/.,)")
            for match in re.findall(r"github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)", abstract or "")
        }
        for full_name in declared_names:
            try:
                repo_response = self.session.get(f"{self.REPO_API_URL}/{full_name}", timeout=20)
                repo_response.raise_for_status()
                declared_item = repo_response.json()
                declared_item["_paper_declared"] = True
                items.insert(0, declared_item)
            except requests.RequestException:
                continue

        title_tokens = self._tokens(title)
        matches = []
        seen = set()
        for item in items:
            if not item.get("full_name") or item["full_name"] in seen:
                continue
            seen.add(item["full_name"])
            text = f"{item.get('name', '')} {item.get('description') or ''}"
            overlap = len(title_tokens & self._tokens(text))
            if not item.get("_paper_declared") and title_tokens and overlap / len(title_tokens) < 0.15:
                continue
            verification = self._verify(
                item, title, authors or [], arxiv_id, doi, declared=item.get("_paper_declared", False)
            )
            if verification["confidence"] < 20:
                continue
            matches.append(
                {
                    "full_name": item.get("full_name"),
                    "url": item.get("html_url"),
                    "description": item.get("description"),
                    "stars": int(item.get("stargazers_count") or 0),
                    "updated_at": item.get("updated_at"),
                    **verification,
                }
            )
        return sorted(matches, key=lambda row: (row["confidence"], row["stars"]), reverse=True)[:max_results]
