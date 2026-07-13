"""Resolve lawful open-access copies from public repositories and APIs."""

import re
from html import unescape
from typing import Dict, Optional
from urllib.parse import urljoin

import requests


class OpenAccessResolver:
    UNPAYWALL_URL = "https://api.unpaywall.org/v2"
    CORE_URL = "https://api.core.ac.uk/v3"
    OPENREVIEW_URL = "https://api2.openreview.net/notes"

    def __init__(self, email: str = "", core_api_key: str = ""):
        self.email = email
        self.core_api_key = core_api_key
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "ArxivDailyResearcher/2.0"

    @staticmethod
    def _doi(doi: str) -> str:
        return (doi or "").replace("https://doi.org/", "").replace("DOI:", "").strip()

    @staticmethod
    def _result(url: str, provider: str, **metadata) -> Dict:
        return {"pdf_url": url, "provider": provider, **metadata}

    @staticmethod
    def _title_key(title: str) -> str:
        return re.sub(r"[^a-z0-9]+", "", (title or "").lower())

    def _pdf_from_public_page(self, page_url: str) -> Optional[str]:
        """Find a directly linked PDF on an author or institutional repository page."""
        if not page_url or not page_url.startswith(("http://", "https://")):
            return None
        try:
            response = self.session.get(page_url, timeout=20, allow_redirects=True)
            response.raise_for_status()
            if "application/pdf" in response.headers.get("Content-Type", "").lower():
                return response.url
            html = response.text[:1_000_000]
            for href in re.findall(r'href=["\']([^"\']+)["\']', html, flags=re.I):
                candidate = unescape(urljoin(response.url, href))
                if re.search(r"\.pdf(?:$|[?#])", candidate, flags=re.I):
                    return candidate
        except requests.RequestException:
            return None
        return None

    def from_openalex_locations(self, paper) -> Optional[Dict]:
        for location in paper.open_access_candidates:
            if location.get("pdf_url"):
                return self._result(
                    location["pdf_url"], "openalex_repository", license=location.get("license"),
                    source=location.get("source"),
                )
            if location.get("source_type") == "repository":
                pdf = self._pdf_from_public_page(location.get("landing_page_url"))
                if pdf:
                    return self._result(pdf, "institutional_or_author_repository", source=location.get("source"))
        return None

    def from_unpaywall(self, doi: str) -> Optional[Dict]:
        clean = self._doi(doi)
        if not clean or not self.email:
            return None
        try:
            response = self.session.get(f"{self.UNPAYWALL_URL}/{clean}", params={"email": self.email}, timeout=20)
            response.raise_for_status()
            data = response.json()
            locations = [data.get("best_oa_location")] + (data.get("oa_locations") or [])
            for location in locations:
                if not location:
                    continue
                pdf = location.get("url_for_pdf")
                if pdf:
                    return self._result(
                        pdf, "unpaywall", license=location.get("license"),
                        host_type=location.get("host_type"), version=location.get("version"),
                    )
                if location.get("host_type") == "repository":
                    pdf = self._pdf_from_public_page(location.get("url_for_landing_page"))
                    if pdf:
                        return self._result(pdf, "unpaywall_repository", license=location.get("license"))
        except requests.RequestException:
            return None
        return None

    def from_core(self, doi: str, title: str) -> Optional[Dict]:
        if not self.core_api_key:
            return None
        clean = self._doi(doi)
        query = f'doi:"{clean}"' if clean else f'title:"{title}"'
        try:
            response = self.session.get(
                f"{self.CORE_URL}/search/works",
                params={"q": query, "limit": 10},
                headers={"Authorization": f"Bearer {self.core_api_key}"},
                timeout=30,
            )
            response.raise_for_status()
            for item in response.json().get("results", []):
                urls = [item.get("downloadUrl")] + (item.get("sourceFulltextUrls") or [])
                for url in urls:
                    if url:
                        return self._result(url, "core", core_id=item.get("id"))
        except requests.RequestException:
            return None
        return None

    def from_openreview(self, title: str) -> Optional[Dict]:
        """Find an exact-title public OpenReview submission and its PDF."""
        if not title:
            return None
        try:
            response = self.session.get(
                self.OPENREVIEW_URL,
                params={"content.title": title, "limit": 10},
                timeout=20,
            )
            response.raise_for_status()
            expected = self._title_key(title)
            for note in response.json().get("notes", []):
                content = note.get("content") or {}
                note_title = content.get("title") or ""
                if isinstance(note_title, dict):
                    note_title = note_title.get("value") or ""
                if self._title_key(note_title) != expected:
                    continue
                note_id = note.get("id")
                if note_id:
                    return self._result(
                        f"https://openreview.net/pdf?id={note_id}",
                        "openreview",
                        license="public submission",
                        landing_page=f"https://openreview.net/forum?id={note_id}",
                    )
        except requests.RequestException:
            return None
        return None

    def resolve(self, paper) -> Optional[Dict]:
        return (
            self.from_openalex_locations(paper)
            or self.from_unpaywall(paper.doi)
            or self.from_openreview(paper.title)
            or self.from_core(paper.doi, paper.title)
        )
