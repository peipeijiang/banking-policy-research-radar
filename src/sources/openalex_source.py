"""
OpenAlex 期刊数据源

通过 OpenAlex API 获取学术期刊的最新论文元数据。
相比 Crossref，OpenAlex 提供更完整的摘要和元数据。
"""

import json
import logging
import re
import traceback
import requests
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log

from .base_source import BasePaperSource, PaperMetadata

logger = logging.getLogger(__name__)

# 期刊名称到 ISSN 的映射（与 Crossref 保持一致）
JOURNAL_ISSN_MAP = {
    # Physical Review 系列
    "prl": {
        "full_name": "Physical Review Letters",
        "issn": ["0031-9007", "1079-7114"],
        "display_name": "PRL",
    },
    "pra": {
        "full_name": "Physical Review A",
        "issn": ["2469-9926", "1050-2947"],
        "display_name": "PRA",
    },
    "prb": {
        "full_name": "Physical Review B",
        "issn": ["2469-9950", "1098-0121"],
        "display_name": "PRB",
    },
    "prc": {
        "full_name": "Physical Review C",
        "issn": ["2469-9985", "0556-2813"],
        "display_name": "PRC",
    },
    "prd": {
        "full_name": "Physical Review D",
        "issn": ["2470-0010", "1550-7998"],
        "display_name": "PRD",
    },
    "pre": {
        "full_name": "Physical Review E",
        "issn": ["2470-0045", "1539-3755"],
        "display_name": "PRE",
    },
    "prx": {"full_name": "Physical Review X", "issn": ["2160-3308"], "display_name": "PRX"},
    "prxq": {"full_name": "PRX Quantum", "issn": ["2691-3399"], "display_name": "PRX Quantum"},
    "rmp": {
        "full_name": "Reviews of Modern Physics",
        "issn": ["0034-6861", "1539-0756"],
        "display_name": "RMP",
    },
    # Nature 系列
    "nature": {"full_name": "Nature", "issn": ["0028-0836", "1476-4687"], "display_name": "Nature"},
    "nature_physics": {
        "full_name": "Nature Physics",
        "issn": ["1745-2473", "1745-2481"],
        "display_name": "Nat. Phys.",
    },
    "nature_communications": {
        "full_name": "Nature Communications",
        "issn": ["2041-1723"],
        "display_name": "Nat. Commun.",
    },
    # Science 系列
    "science": {
        "full_name": "Science",
        "issn": ["0036-8075", "1095-9203"],
        "display_name": "Science",
    },
    "science_advances": {
        "full_name": "Science Advances",
        "issn": ["2375-2548"],
        "display_name": "Sci. Adv.",
    },
    # 其他重要期刊
    "npj_quantum_information": {
        "full_name": "npj Quantum Information",
        "issn": ["2056-6387"],
        "display_name": "npj QI",
    },
    "quantum": {"full_name": "Quantum", "issn": ["2521-327X"], "display_name": "Quantum"},
    "new_journal_of_physics": {
        "full_name": "New Journal of Physics",
        "issn": ["1367-2630"],
        "display_name": "NJP",
    },
}


class OpenAlexSource(BasePaperSource):
    """
    OpenAlex 期刊数据源。

    特点：
    - 支持多种学术期刊（PRL、PRA、Nature 等）
    - 通过 OpenAlex API 获取元数据
    - 提供倒排索引格式的摘要（自动重建为文本）
    - 不支持 PDF 下载，仅进行评分分析
    """

    API_BASE_URL = "https://api.openalex.org"

    def __init__(
        self,
        history_dir: Path,
        journals: List[str] = None,
        max_results: int = 100,
        email: str = None,
        api_key: str = None,
        search_terms: List[str] = None,
    ):
        """
        初始化 OpenAlex 数据源。

        参数:
            history_dir: 历史记录存储目录
            journals: 要抓取的期刊代码列表，如 ["prl", "pra"]
            max_results: 每个期刊最多抓取的论文数
            email: 用户邮箱（用于礼貌池，提高速率限制）
            api_key: OpenAlex API Key（可选，2026年2月后必需）
        """
        super().__init__("openalex", history_dir)
        self.journals = journals or []
        self.max_results = max_results
        self.email = email
        self.api_key = api_key
        self.search_terms = search_terms or []

        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "ArxivDailyResearcher/2.0 (https://github.com/yzr278892/arxiv-daily-researcher; yzr278892@gmail.com)"
            }
        )

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
            logger.debug("OpenAlex Session已关闭")

    def _api_request(self, url: str, params: dict) -> dict:
        """发送 OpenAlex API 请求，带自动重试。"""
        from config import settings as _settings

        @retry(
            stop=stop_after_attempt(_settings.RETRY_MAX_ATTEMPTS),
            wait=wait_exponential(min=_settings.RETRY_MIN_WAIT, max=_settings.RETRY_MAX_WAIT),
            before_sleep=before_sleep_log(logger, logging.WARNING),
            reraise=True,
        )
        def _do_request():
            resp = self.session.get(url, params=params, timeout=30)
            resp.raise_for_status()
            return resp.json()

        return _do_request()

    @property
    def display_name(self) -> str:
        return "OpenAlex"

    def can_download_pdf(self) -> bool:
        return False  # OpenAlex 只提供元数据

    def get_journal_info(self, journal_code: str) -> Optional[Dict]:
        """获取期刊信息"""
        return JOURNAL_ISSN_MAP.get(journal_code.lower())

    def fetch_papers(self, days: int, journals: List[str] = None, **kwargs) -> List[PaperMetadata]:
        """
        从 OpenAlex 抓取指定期刊最近 N 天的论文。

        参数:
            days: 搜索最近 N 天的论文
            journals: 期刊代码列表，如 ["prl", "pra"]

        返回:
            List[PaperMetadata]: 论文元数据列表
        """
        if journals:
            self.journals = journals

        all_papers = []
        from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        to_date = datetime.now().strftime("%Y-%m-%d")

        if self.search_terms:
            all_papers.extend(self._fetch_topic_papers(from_date, to_date))

        if not self.journals:
            logger.info(f"[OpenAlex] 主题检索共发现 {len(all_papers)} 篇论文")
            return all_papers

        logger.info(f"[OpenAlex] 开始抓取期刊论文")
        logger.info(f"  目标期刊: {self.journals}")
        logger.info(f"  时间范围: 最近 {days} 天（从 {from_date}）")

        for journal_code in self.journals:
            journal_info = self.get_journal_info(journal_code)
            if not journal_info:
                logger.warning(f"  未知期刊代码: {journal_code}，跳过")
                continue

            issn_list = journal_info["issn"]
            journal_name = journal_info["full_name"]
            display_name = journal_info["display_name"]

            logger.info(f"  正在抓取 {journal_name}...")

            try:
                papers = self._fetch_journal_papers(
                    issn_list=issn_list,
                    journal_code=journal_code,
                    journal_name=journal_name,
                    from_date=from_date,
                )
                all_papers.extend(papers)
                logger.info(f"    {display_name}: 发现 {len(papers)} 篇新论文")

            except Exception as e:
                logger.error(f"    {display_name} 抓取失败: {e}")
                import traceback

                traceback.print_exc()

        logger.info(f"[OpenAlex] 总计发现 {len(all_papers)} 篇新论文")
        return all_papers

    def _base_params(self) -> Dict[str, str]:
        params = {}
        if self.api_key:
            params["api_key"] = self.api_key
        elif self.email:
            params["mailto"] = self.email
        return params

    def _fetch_topic_papers(self, from_date: str, to_date: str) -> List[PaperMetadata]:
        """按标题和摘要中的推荐系统短语检索近期 OpenAlex Works。"""
        logger.info("[OpenAlex] 开始主题检索")
        logger.info(f"  检索短语: {self.search_terms}")
        logger.info(f"  时间范围: {from_date} 至 {to_date}")

        papers_by_id: Dict[str, PaperMetadata] = {}
        per_term = max(10, min(50, self.max_results // max(1, len(self.search_terms)) + 5))
        url = f"{self.API_BASE_URL}/works"

        for index, term in enumerate(self.search_terms):
            if len(papers_by_id) >= self.max_results:
                break
            params = {
                "filter": (
                    f'from_publication_date:{from_date},to_publication_date:{to_date},'
                    f'type:article|preprint,title_and_abstract.search:"{term}"'
                ),
                "per_page": per_term,
                "sort": "publication_date:desc",
                "select": (
                    "id,doi,title,authorships,abstract_inverted_index,publication_date,"
                    "primary_location,open_access,locations,best_oa_location,ids,"
                    "cited_by_count,type,topics"
                    ",referenced_works,related_works"
                ),
            }
            params.update(self._base_params())

            try:
                data = self._api_request(url, params)
                found = 0
                for item in data.get("results", []):
                    metadata = self._metadata_from_item(item, source="openalex")
                    if not metadata or self.is_processed(metadata.paper_id):
                        continue
                    dedupe_key = metadata.openalex_id or metadata.paper_id
                    papers_by_id[dedupe_key] = metadata
                    found += 1
                    if len(papers_by_id) >= self.max_results:
                        break
                logger.info(f"  {term}: 新增 {found} 篇")
            except Exception as exc:
                logger.warning(f"  OpenAlex 主题检索失败 ({term}): {exc}")

            # 免费 API 上限为每秒 10 次，主动留出余量。
            if index < len(self.search_terms) - 1:
                time.sleep(0.25)

        papers_by_title = {}
        for paper in papers_by_id.values():
            title_key = re.sub(r"[^a-z0-9]+", "", paper.title.lower())
            existing = papers_by_title.get(title_key)
            quality = (
                bool(paper.pdf_url),
                bool(paper.abstract),
                paper.cited_by_count,
                len(paper.referenced_works),
            )
            existing_quality = (
                bool(existing.pdf_url),
                bool(existing.abstract),
                existing.cited_by_count,
                len(existing.referenced_works),
            ) if existing else None
            if not existing or quality > existing_quality:
                papers_by_title[title_key] = paper
        papers = list(papers_by_title.values())[: self.max_results]
        logger.info(f"[OpenAlex] 主题检索去重后共 {len(papers)} 篇")
        return papers

    def _metadata_from_item(self, item: Dict, source: str) -> Optional[PaperMetadata]:
        """将 OpenAlex Work 转为统一论文元数据。"""
        openalex_id = item.get("id", "").replace("https://openalex.org/", "")
        doi_url = item.get("doi")
        paper_id = doi_url or (f"openalex:{openalex_id}" if openalex_id else "")
        if not paper_id:
            return None

        title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", item.get("title") or "")).strip()
        if not title:
            return None

        authors = []
        for authorship in item.get("authorships", [])[:20]:
            name = (authorship.get("author") or {}).get("display_name")
            if name:
                authors.append(name)

        abstract = self._rebuild_abstract(item.get("abstract_inverted_index") or {})
        primary_location = item.get("primary_location") or {}
        source_info = primary_location.get("source") or {}
        venue = (
            source_info.get("display_name")
            or primary_location.get("raw_source_name")
            or "OpenAlex"
        )
        landing_page_url = primary_location.get("landing_page_url")
        if not landing_page_url:
            landing_page_url = doi_url or f"https://openalex.org/{openalex_id}"

        best_oa = item.get("best_oa_location") or {}
        pdf_url = best_oa.get("pdf_url") or primary_location.get("pdf_url")
        if not pdf_url:
            oa_url = (item.get("open_access") or {}).get("oa_url")
            if oa_url and oa_url.lower().endswith(".pdf"):
                pdf_url = oa_url

        arxiv_id = None
        arxiv_url = None
        for location in item.get("locations", []):
            location_url = location.get("landing_page_url") or ""
            location_source = (location.get("source") or {}).get("display_name", "")
            if "arxiv" not in location_source.lower() and "arxiv.org" not in location_url:
                continue
            match = re.search(r"arxiv\.org/(?:abs|pdf)/([^/?#]+)", location_url)
            if match:
                arxiv_id = match.group(1).removesuffix(".pdf")
                arxiv_url = f"https://arxiv.org/abs/{arxiv_id}"
                pdf_url = pdf_url or f"https://arxiv.org/pdf/{arxiv_id}.pdf"
                break

        topics = [
            topic.get("display_name")
            for topic in item.get("topics", [])[:5]
            if topic.get("display_name")
        ]
        open_access_candidates = []
        for location in item.get("locations", []):
            source_info = location.get("source") or {}
            landing = location.get("landing_page_url")
            pdf = location.get("pdf_url")
            if not (landing or pdf):
                continue
            if pdf or source_info.get("type") == "repository" or location.get("is_oa"):
                open_access_candidates.append(
                    {
                        "landing_page_url": landing,
                        "pdf_url": pdf,
                        "source": source_info.get("display_name"),
                        "source_type": source_info.get("type"),
                        "license": location.get("license"),
                    }
                )

        return PaperMetadata(
            paper_id=paper_id,
            title=title,
            authors=authors,
            abstract=abstract,
            published_date=self._parse_date(item.get("publication_date")),
            url=landing_page_url,
            source=source,
            pdf_url=pdf_url,
            doi=doi_url,
            journal=venue,
            arxiv_id=arxiv_id,
            arxiv_url=arxiv_url,
            openalex_id=openalex_id or None,
            cited_by_count=int(item.get("cited_by_count") or 0),
            publication_type=primary_location.get("raw_type") or item.get("type"),
            topics=topics,
            referenced_works=[
                value.replace("https://openalex.org/", "")
                for value in item.get("referenced_works", [])[:100]
            ],
            related_works=[
                value.replace("https://openalex.org/", "")
                for value in item.get("related_works", [])[:20]
            ],
            open_access_candidates=open_access_candidates,
        )

    def lookup_by_dois(self, dois: List[str]) -> Dict[str, PaperMetadata]:
        """批量查询 DOI，为 DBLP 会议记录补摘要、引用和开放 PDF。"""
        clean_dois = []
        for doi in dois:
            clean = doi.lower().replace("https://doi.org/", "").replace("doi:", "").strip()
            if clean and clean not in clean_dois:
                clean_dois.append(clean)

        enriched = {}
        select = (
            "id,doi,title,authorships,abstract_inverted_index,publication_date,"
            "primary_location,open_access,locations,best_oa_location,ids,"
            "cited_by_count,type,topics"
            ",referenced_works,related_works"
        )
        for start in range(0, len(clean_dois), 50):
            chunk = clean_dois[start : start + 50]
            params = {
                "filter": f"doi:{'|'.join(chunk)}",
                "per_page": len(chunk),
                "select": select,
            }
            params.update(self._base_params())
            try:
                data = self._api_request(f"{self.API_BASE_URL}/works", params)
            except Exception as exc:
                logger.warning(f"OpenAlex DOI 批量增强失败: {exc}")
                continue
            for item in data.get("results", []):
                metadata = self._metadata_from_item(item, source="openalex")
                if metadata and metadata.doi:
                    key = metadata.doi.lower().replace("https://doi.org/", "")
                    enriched[key] = metadata
        return enriched

    def lookup_by_ids(self, work_ids: List[str]) -> Dict[str, PaperMetadata]:
        """Batch-resolve OpenAlex work IDs for bounded graph expansion."""
        clean_ids = list(dict.fromkeys(value.replace("https://openalex.org/", "") for value in work_ids if value))
        resolved = {}
        select = (
            "id,doi,title,authorships,abstract_inverted_index,publication_date,"
            "primary_location,open_access,locations,best_oa_location,ids,"
            "cited_by_count,type,topics,referenced_works,related_works"
        )
        for start in range(0, len(clean_ids), 50):
            chunk = clean_ids[start : start + 50]
            params = {"filter": f"openalex:{'|'.join(chunk)}", "per_page": len(chunk), "select": select}
            params.update(self._base_params())
            data = self._api_request(f"{self.API_BASE_URL}/works", params)
            for item in data.get("results", []):
                paper = self._metadata_from_item(item, source="citation")
                if paper and paper.openalex_id:
                    resolved[paper.openalex_id] = paper
        return resolved

    def find_recent_citing(self, work_id: str, from_date: str, limit: int = 10) -> List[PaperMetadata]:
        """Find recent works that cite one seed work."""
        params = {
            "filter": f"cites:{work_id},from_publication_date:{from_date}",
            "sort": "publication_date:desc",
            "per_page": min(limit, 25),
            "select": (
                "id,doi,title,authorships,abstract_inverted_index,publication_date,"
                "primary_location,open_access,locations,best_oa_location,ids,"
                "cited_by_count,type,topics,referenced_works,related_works"
            ),
        }
        params.update(self._base_params())
        data = self._api_request(f"{self.API_BASE_URL}/works", params)
        return [paper for item in data.get("results", []) if (paper := self._metadata_from_item(item, source="citation"))]

    def _fetch_from_arxiv(
        self, arxiv_id: str, journal_code: str, journal_name: str, doi: str
    ) -> Optional[PaperMetadata]:
        """
        通过 arXiv ID 从 ArXiv 获取论文元数据。

        参数:
            arxiv_id: arXiv ID
            journal_code: 期刊代码
            journal_name: 期刊全名
            doi: DOI

        返回:
            Optional[PaperMetadata]: 论文元数据，失败时返回 None
        """
        try:
            import arxiv

            # 使用 arXiv API 获取论文
            search = arxiv.Search(id_list=[arxiv_id])
            client = arxiv.Client(page_size=1, delay_seconds=3.0, num_retries=2)

            results = list(client.results(search))
            if not results:
                logger.warning(f"    ⚠️  arXiv API 未找到论文: {arxiv_id}")
                return None

            result = results[0]

            # 转换为统一格式，保留期刊信息
            metadata = PaperMetadata(
                paper_id=result.get_short_id(),
                title=result.title,
                authors=[author.name for author in result.authors],
                abstract=result.summary,  # arXiv 提供完整摘要
                published_date=result.published,
                url=result.entry_id,
                source=journal_code,  # 保留期刊代码
                pdf_url=result.pdf_url,
                doi=doi,  # 使用期刊的 DOI
                journal=journal_name,  # 标注期刊名称
                arxiv_id=arxiv_id,
                arxiv_url=result.entry_id,
                categories=list(result.categories) if result.categories else [],
            )

            logger.info(
                f"    ✅ [{result.title[:30]}...] 使用 arXiv 源获取完整元数据 (arXiv:{arxiv_id})"
            )
            return metadata

        except Exception as e:
            logger.warning(f"    ⚠️  从 arXiv 获取论文失败 ({arxiv_id}): {e}")
            return None

    def _fetch_journal_papers(
        self, issn_list: List[str], journal_code: str, journal_name: str, from_date: str
    ) -> List[PaperMetadata]:
        """
        抓取单个期刊的论文。

        参数:
            issn_list: 期刊 ISSN 列表
            journal_code: 期刊代码（用于 source 字段）
            journal_name: 期刊全名
            from_date: 起始日期 (YYYY-MM-DD)

        返回:
            List[PaperMetadata]: 论文列表
        """
        papers = []

        # 构建 ISSN 过滤器（支持多个ISSN）
        issn_filter = "|".join(issn_list)

        url = f"{self.API_BASE_URL}/works"

        # 添加邮箱或API Key到基础参数
        base_params = {}
        if self.api_key:
            base_params["api_key"] = self.api_key
        elif self.email:
            base_params["mailto"] = self.email

        # 实现分页逻辑，支持获取超过200条的结果
        page = 1
        per_page = min(200, self.max_results)  # OpenAlex单页最大200
        total_fetched = 0

        try:
            while total_fetched < self.max_results:
                params = {
                    "filter": f"primary_location.source.issn:{issn_filter},from_publication_date:{from_date}",
                    "per_page": per_page,
                    "page": page,
                    "sort": "publication_date:desc",
                    "select": "id,doi,title,authorships,abstract_inverted_index,publication_date,primary_location,open_access,locations,best_oa_location,ids",
                }
                params.update(base_params)

                logger.debug(f"  正在获取第 {page} 页...")
                data = self._api_request(url, params)

                results = data.get("results", [])
                if not results:
                    logger.debug(f"  第 {page} 页无更多结果，停止分页")
                    break

                for item in results:
                    doi = item.get("doi")
                    if not doi:
                        # 使用 OpenAlex ID 作为后备
                        openalex_id = item.get("id", "").replace("https://openalex.org/", "")
                        if not openalex_id:
                            continue
                        doi = f"openalex:{openalex_id}"

                    # 去重检查
                    if self.is_processed(doi):
                        continue

                    # 提取标题
                    title = item.get("title", "Untitled")
                    if not title or title == "Untitled":
                        continue

                    # 清理标题（移除可能的HTML标签）
                    title = re.sub(r"<[^>]+>", "", title)
                    title = re.sub(r"\s+", " ", title).strip()

                    # 提取作者
                    authors = []
                    authorships = item.get("authorships", [])
                    for authorship in authorships[:20]:  # 最多20个作者
                        author = authorship.get("author", {})
                        display_name = author.get("display_name")
                        if display_name:
                            authors.append(display_name)

                    # 提取并重建摘要
                    abstract = ""
                    inverted_index = item.get("abstract_inverted_index")
                    if inverted_index:
                        abstract = self._rebuild_abstract(inverted_index)
                        logger.debug(f"    ✅ [{title[:30]}...] 成功获取摘要")
                    else:
                        logger.warning(
                            f"    ⚠️  [{title[:30]}...] OpenAlex 未提供摘要数据 (可能因期刊版权限制)"
                        )

                    # 提取发布日期
                    pub_date_str = item.get("publication_date")
                    published_date = self._parse_date(pub_date_str)

                    # 提取 URL
                    if doi.startswith("http"):
                        landing_page_url = doi
                    elif doi.startswith("openalex:"):
                        landing_page_url = f"https://openalex.org/{doi.replace('openalex:', '')}"
                    else:
                        landing_page_url = f"https://doi.org/{doi}"
                    primary_location = item.get("primary_location", {})
                    if primary_location and primary_location.get("landing_page_url"):
                        landing_page_url = primary_location["landing_page_url"]

                    # 提取 PDF URL（如果开放获取）
                    pdf_url = None
                    open_access = item.get("open_access", {})
                    if open_access.get("is_oa") and open_access.get("oa_url"):
                        pdf_url = open_access["oa_url"]
                        logger.debug(f"    ✅ [{title[:30]}...] 找到开放获取 PDF")

                    # 从 locations 提取 arXiv 信息（使用正则表达式提高健壮性）
                    arxiv_id = None
                    arxiv_url = None
                    locations = item.get("locations", [])
                    for loc in locations:
                        source_info = loc.get("source", {})
                        if source_info:
                            source_name = source_info.get("display_name", "")
                            # 检查是否是 arXiv 来源
                            if "arxiv" in source_name.lower():
                                loc_url = loc.get("landing_page_url", "")
                                if loc_url and "arxiv.org" in loc_url:
                                    arxiv_url = loc_url
                                    # 使用正则表达式提取 arXiv ID，更健壮
                                    try:
                                        match = re.search(
                                            r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", loc_url
                                        )
                                        if match:
                                            arxiv_id = match.group(1)
                                    except Exception as e:
                                        logger.debug(f"arXiv ID提取失败: {e}")
                                    break

                    # 🎯 优先策略：如果找到 arXiv 版本，使用 ArXiv 源获取完整元数据
                    if arxiv_id:
                        logger.info(
                            f"    🔄 [{title[:30]}...] 检测到 arXiv 版本: {arxiv_id}，转而使用 ArXiv 源获取完整元数据"
                        )
                        arxiv_metadata = self._fetch_from_arxiv(
                            arxiv_id, journal_code, journal_name, doi
                        )
                        if arxiv_metadata:
                            papers.append(arxiv_metadata)
                            total_fetched += 1
                            if total_fetched >= self.max_results:
                                break
                            continue  # 跳过 OpenAlex 的元数据提取，直接处理下一篇论文
                        else:
                            logger.warning(f"    ⚠️  从 ArXiv 获取失败，回退到 OpenAlex 元数据")
                            # 继续使用 OpenAlex 数据
                    else:
                        logger.debug(
                            f"    ℹ️  [{title[:30]}...] 未找到 arXiv 版本，使用 OpenAlex 元数据"
                        )

                    # 构建论文元数据
                    metadata = PaperMetadata(
                        paper_id=doi,
                        title=title,
                        authors=authors,
                        abstract=abstract,
                        published_date=published_date,
                        url=landing_page_url,
                        source=journal_code,  # 使用期刊代码作为 source
                        pdf_url=pdf_url,
                        doi=doi if not doi.startswith("openalex:") else None,
                        journal=journal_name,
                        arxiv_id=arxiv_id,
                        arxiv_url=arxiv_url,
                    )
                    papers.append(metadata)
                    total_fetched += 1

                    if total_fetched >= self.max_results:
                        break

                # 检查是否还有更多页
                page += 1
                if total_fetched >= self.max_results:
                    logger.debug(f"  已达到最大结果数 {self.max_results}，停止分页")
                    break

        except requests.exceptions.RequestException as e:
            logger.error(f"OpenAlex API 请求失败: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"OpenAlex API 响应解析失败: {e}")
        except Exception as e:
            logger.error(f"OpenAlex 数据处理失败: {e}")
            traceback.print_exc()

        logger.info(f"  共获取 {len(papers)} 篇论文（分 {page - 1} 页）")
        return papers

    def _rebuild_abstract(self, inverted_index: Dict[str, List[int]]) -> str:
        """
        将倒排索引格式的摘要重建为普通文本。

        OpenAlex 使用倒排索引存储摘要以规避版权问题。
        格式: {"word": [position1, position2, ...], ...}

        参数:
            inverted_index: 倒排索引字典

        返回:
            str: 重建的摘要文本
        """
        if not inverted_index:
            return ""

        try:
            # 找到最大位置索引
            max_position = 0
            for positions in inverted_index.values():
                if positions:
                    max_position = max(max_position, max(positions))

            # 防止内存溢出：限制最大position值
            MAX_ALLOWED_POSITION = 50000  # 约50KB的文本
            if max_position > MAX_ALLOWED_POSITION:
                logger.warning(
                    f"摘要position过大 ({max_position})，可能数据损坏，截断到 {MAX_ALLOWED_POSITION}"
                )
                max_position = MAX_ALLOWED_POSITION

            # 创建位置数组
            words_array = [""] * (max_position + 1)

            # 填充单词到对应位置
            for word, positions in inverted_index.items():
                for pos in positions:
                    if 0 <= pos <= max_position:
                        words_array[pos] = word

            # 合并为文本
            abstract = " ".join(word for word in words_array if word)

            # 基本清理
            abstract = abstract.strip()

            return abstract

        except Exception as e:
            logger.warning(f"摘要重建失败: {e}")
            return ""

    def _parse_date(self, date_str: str) -> datetime:
        """
        解析 OpenAlex 返回的日期。

        OpenAlex 日期格式: "YYYY-MM-DD"

        参数:
            date_str: 日期字符串

        返回:
            datetime: 解析后的日期对象
        """
        try:
            if date_str:
                return datetime.strptime(date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            pass

        return datetime.now()
