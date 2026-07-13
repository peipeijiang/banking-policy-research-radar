"""
Semantic Scholar 数据增强器

通过 Semantic Scholar API 获取 AI 生成的 TLDR 和其他增强信息。
"""

import logging
import requests
from typing import Optional, Dict, List
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log

logger = logging.getLogger(__name__)


class SemanticScholarEnricher:
    """
    Semantic Scholar 数据增强器。

    功能：
    - 根据 DOI 获取论文的 AI 生成 TLDR
    - 获取其他补充信息（引用数、影响力评分等）
    """

    API_BASE_URL = "https://api.semanticscholar.org/graph/v1"

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 Semantic Scholar 增强器。

        参数:
            api_key: Semantic Scholar API Key（可选，提高速率限制）
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "ArxivDailyResearcher/2.0 (https://github.com/yzr278892/arxiv-daily-researcher; yzr278892@gmail.com)"
        })

        if api_key:
            self.session.headers.update({
                "x-api-key": api_key
            })

    def __enter__(self):
        """支持上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出时关闭Session"""
        self.close()

    def close(self):
        """关闭网络连接"""
        if self.session:
            self.session.close()
            logger.debug("SemanticScholar Session已关闭")

    def _api_get(self, url: str, params: dict, timeout: int = 10) -> requests.Response:
        """发送 Semantic Scholar API GET 请求，带自动重试（跳过 404/429）。"""
        from config import settings as _settings

        @retry(
            stop=stop_after_attempt(_settings.RETRY_MAX_ATTEMPTS),
            wait=wait_exponential(min=_settings.RETRY_MIN_WAIT, max=_settings.RETRY_MAX_WAIT),
            before_sleep=before_sleep_log(logger, logging.WARNING),
            reraise=True,
        )
        def _do_get():
            resp = self.session.get(url, params=params, timeout=timeout)
            # 404 和 429 不重试，直接返回
            if resp.status_code in (404, 429):
                return resp
            resp.raise_for_status()
            return resp

        return _do_get()

    def get_papers_info_batch(self, dois: List[str]) -> Dict[str, Dict]:
        """批量获取论文增强信息，避免逐篇请求耗尽公共限额。"""
        clean_dois = []
        seen = set()
        for doi in dois:
            clean = doi.replace("https://doi.org/", "").replace("DOI:", "").strip()
            if clean and clean.lower() not in seen:
                clean_dois.append(clean)
                seen.add(clean.lower())

        if not clean_dois:
            return {}

        results: Dict[str, Dict] = {}
        url = f"{self.API_BASE_URL}/paper/batch"
        fields = (
            "title,abstract,tldr,citationCount,influentialCitationCount,externalIds,"
            "publicationTypes,openAccessPdf,url,venue"
        )

        for start in range(0, len(clean_dois), 500):
            chunk = clean_dois[start : start + 500]
            try:
                response = self.session.post(
                    url,
                    params={"fields": fields},
                    json={"ids": [f"DOI:{doi}" for doi in chunk]},
                    timeout=30,
                )
                if response.status_code == 429:
                    logger.warning(
                        "⚠️  Semantic Scholar 公共 API 已限速，跳过本轮增强；"
                        "配置 API Key 后可获得独立限额"
                    )
                    break
                response.raise_for_status()

                for doi, data in zip(chunk, response.json()):
                    if not data:
                        continue
                    tldr = data.get("tldr") or {}
                    open_pdf = data.get("openAccessPdf") or {}
                    external_ids = data.get("externalIds") or {}
                    results[doi.lower()] = {
                        "paper_id": data.get("paperId"),
                        "url": data.get("url"),
                        "venue": data.get("venue"),
                        "abstract": data.get("abstract"),
                        "tldr": tldr.get("text"),
                        "citation_count": int(data.get("citationCount") or 0),
                        "influential_citation_count": int(
                            data.get("influentialCitationCount") or 0
                        ),
                        "publication_types": data.get("publicationTypes") or [],
                        "arxiv_id": external_ids.get("ArXiv"),
                        "pdf_url": open_pdf.get("url"),
                    }
            except requests.RequestException as exc:
                logger.warning(f"Semantic Scholar 批量增强失败: {exc}")
                break

        return results

    def get_tldr(self, doi: str) -> Optional[str]:
        """
        获取论文的 AI 生成 TLDR。

        参数:
            doi: 论文的 DOI

        返回:
            Optional[str]: TLDR 文本，失败时返回 None
        """
        try:
            # 清理 DOI（移除可能的前缀）
            clean_doi = doi.replace("https://doi.org/", "").replace("DOI:", "").strip()

            # 构建请求 URL
            url = f"{self.API_BASE_URL}/paper/DOI:{clean_doi}"
            params = {
                "fields": "tldr"
            }

            response = self._api_get(url, params)

            # 如果找不到论文，静默返回 None
            if response.status_code == 404:
                logger.warning(f"⚠️  Semantic Scholar 未收录论文: DOI {clean_doi[:30]}... (可能因论文太新或未被索引)")
                return None

            if response.status_code == 429:
                logger.warning(f"⚠️  Semantic Scholar API 限速 (429)，建议申请免费 API Key")
                return None

            response.raise_for_status()
            data = response.json()

            # 提取 TLDR
            tldr_obj = data.get("tldr")
            if tldr_obj and isinstance(tldr_obj, dict):
                tldr_text = tldr_obj.get("text", "")
                if tldr_text:
                    logger.debug(f"✅ 成功获取 TLDR: {clean_doi[:30]}...")
                    return tldr_text
                else:
                    logger.debug(f"ℹ️  论文无 AI TLDR: {clean_doi[:30]}...")
            else:
                logger.debug(f"ℹ️  论文无 AI TLDR: {clean_doi[:30]}...")

            return None

        except requests.exceptions.Timeout:
            logger.warning(f"⚠️  Semantic Scholar API 超时: {clean_doi[:30]}...")
            return None
        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠️  Semantic Scholar API 请求失败: {e}")
            return None
        except Exception as e:
            logger.warning(f"⚠️  获取 TLDR 异常: {e}")
            return None

    def get_paper_info(self, doi: str) -> Optional[Dict]:
        """
        获取论文的完整信息（包括 TLDR、引用数、arXiv链接等）。

        参数:
            doi: 论文的 DOI

        返回:
            Optional[Dict]: 包含各种信息的字典，失败时返回 None
        """
        try:
            clean_doi = doi.replace("https://doi.org/", "").replace("DOI:", "").strip()

            url = f"{self.API_BASE_URL}/paper/DOI:{clean_doi}"
            params = {
                "fields": "tldr,citationCount,influentialCitationCount,publicationTypes,externalIds"
            }

            response = self._api_get(url, params)

            if response.status_code == 404:
                return None

            response.raise_for_status()
            data = response.json()

            result = {}

            # 提取 TLDR
            tldr_obj = data.get("tldr")
            if tldr_obj and isinstance(tldr_obj, dict):
                result["tldr"] = tldr_obj.get("text")

            # 提取引用数
            if "citationCount" in data:
                result["citation_count"] = data["citationCount"]

            if "influentialCitationCount" in data:
                result["influential_citation_count"] = data["influentialCitationCount"]

            if "publicationTypes" in data:
                result["publication_types"] = data["publicationTypes"]

            # 提取 arXiv ID（关键新增功能）
            external_ids = data.get("externalIds", {})
            if external_ids and "ArXiv" in external_ids:
                arxiv_id = external_ids["ArXiv"]
                result["arxiv_id"] = arxiv_id
                result["arxiv_url"] = f"https://arxiv.org/abs/{arxiv_id}"
                logger.debug(f"找到 arXiv 版本: {arxiv_id}")

            return result if result else None

        except Exception as e:
            logger.warning(f"获取 Semantic Scholar 信息失败: {e}")
            return None

    def get_arxiv_id(self, doi: str) -> Optional[str]:
        """
        专门获取论文的 arXiv ID。

        参数:
            doi: 论文的 DOI

        返回:
            Optional[str]: arXiv ID，如 "2401.12345"，失败时返回 None
        """
        try:
            clean_doi = doi.replace("https://doi.org/", "").replace("DOI:", "").strip()

            url = f"{self.API_BASE_URL}/paper/DOI:{clean_doi}"
            params = {
                "fields": "externalIds"
            }

            response = self._api_get(url, params)

            if response.status_code == 404:
                return None

            response.raise_for_status()
            data = response.json()

            external_ids = data.get("externalIds", {})
            if external_ids and "ArXiv" in external_ids:
                return external_ids["ArXiv"]

            return None

        except Exception as e:
            logger.debug(f"获取 arXiv ID 失败: {e}")
            return None
