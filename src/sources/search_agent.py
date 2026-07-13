"""
统一搜索调度器

管理多个论文数据源，根据配置调用相应的源进行论文抓取。
"""

import logging
import re
from pathlib import Path
from typing import List, Dict, Optional

from .base_source import BasePaperSource, PaperMetadata
from .arxiv_source import ArxivSource
from .openalex_source import OpenAlexSource, JOURNAL_ISSN_MAP
from .dblp_source import DblpSource
from .institutional_rss_source import InstitutionalRssSource
from .repec_series_source import RepecSeriesSource
from .worldbank_source import WorldBankSource
from .semantic_scholar_enricher import SemanticScholarEnricher
try:
    from enrichers.open_access import OpenAccessResolver
except ModuleNotFoundError:  # package import path used by tests and library consumers
    from ..enrichers.open_access import OpenAccessResolver

logger = logging.getLogger(__name__)


class SearchAgent:
    """
    统一搜索调度器。

    职责：
    - 管理多个数据源（ArXiv、Crossref 等）
    - 根据配置初始化和调用相应的数据源
    - 返回统一格式的论文列表
    - 支持按数据源分组返回结果
    """

    def __init__(
        self,
        history_dir: Path,
        enabled_sources: List[str] = None,
        arxiv_domains: List[str] = None,
        journals: List[str] = None,
        max_results: int = 100,
        max_results_per_source: Dict[str, int] = None,
        openalex_email: str = None,
        openalex_api_key: str = None,
        openalex_search_terms: List[str] = None,
        dblp_venues: List[str] = None,
        dblp_title_terms: List[str] = None,
        institutional_feeds: List[Dict[str, str]] = None,
        repec_series: List[Dict[str, str]] = None,
        worldbank_search_terms: List[str] = None,
        enable_semantic_scholar: bool = True,
        semantic_scholar_api_key: str = None,
        core_api_key: str = None,
    ):
        """
        初始化搜索调度器。

        参数:
            history_dir: 历史记录存储目录
            enabled_sources: 启用的数据源列表，如 ["arxiv", "prl", "pra"]
            arxiv_domains: ArXiv 领域列表，如 ["quant-ph", "cs.AI"]
            journals: 期刊代码列表，如 ["prl", "pra"]
            max_results: 每个数据源最多抓取的论文数（全局默认值）
            max_results_per_source: 按数据源单独配置的最大结果数，如 {"arxiv": 150, "prl": 50}
            openalex_email: OpenAlex 礼貌池邮箱
            openalex_api_key: OpenAlex API Key
            enable_semantic_scholar: 是否启用 Semantic Scholar TLDR
            semantic_scholar_api_key: Semantic Scholar API Key
        """
        self.history_dir = history_dir
        self.history_dir.mkdir(parents=True, exist_ok=True)

        self.enabled_sources = enabled_sources or ["arxiv"]
        self.arxiv_domains = arxiv_domains or []
        self.journals = journals or []
        self.max_results = max_results
        self.max_results_per_source = max_results_per_source or {}
        self.openalex_email = openalex_email
        self.openalex_api_key = openalex_api_key
        self.openalex_search_terms = openalex_search_terms or []
        self.dblp_venues = dblp_venues or []
        self.dblp_title_terms = dblp_title_terms or []
        self.institutional_feeds = institutional_feeds or []
        self.repec_series = repec_series or []
        self.worldbank_search_terms = worldbank_search_terms or []
        self.open_access_resolver = OpenAccessResolver(
            email=openalex_email or "", core_api_key=core_api_key or ""
        )

        # 初始化 Semantic Scholar 增强器
        self.enable_semantic_scholar = enable_semantic_scholar
        self.semantic_scholar_enricher = None
        if enable_semantic_scholar:
            # 空字符串视为 None，使用公共 API（无需 API Key）
            api_key = semantic_scholar_api_key if semantic_scholar_api_key else None
            self.semantic_scholar_enricher = SemanticScholarEnricher(api_key=api_key)
            if api_key:
                logger.info("[SearchAgent] 已启用 Semantic Scholar TLDR 增强（使用 API Key）")
            else:
                logger.info(
                    "[SearchAgent] 已启用 Semantic Scholar TLDR 增强（公共 API，限速 100次/5分钟）"
                )

        # 初始化数据源
        self.sources: Dict[str, BasePaperSource] = {}
        self._init_sources()

    def _get_max_results(self, source: str) -> int:
        """获取指定数据源的最大结果数，优先使用单独配置，否则回退到全局默认值。"""
        return self.max_results_per_source.get(source, self.max_results)

    def _init_sources(self):
        """根据配置初始化数据源"""
        from config import settings as _settings

        # 检查是否启用 ArXiv
        if "arxiv" in self.enabled_sources:
            arxiv_proxy = _settings.get_proxy_dict("arxiv")
            self.sources["arxiv"] = ArxivSource(
                history_dir=self.history_dir,
                max_results=self._get_max_results("arxiv"),
                proxy_dict=arxiv_proxy,
            )
            logger.info("[SearchAgent] 已启用 ArXiv 数据源")

        # 检查是否启用期刊（通过 OpenAlex）
        # 期刊代码可以直接作为 enabled_sources 的一部分
        journal_codes = []
        for source in self.enabled_sources:
            if source != "arxiv" and source in JOURNAL_ISSN_MAP:
                journal_codes.append(source)

        # 也支持通过 journals 参数指定
        for journal in self.journals:
            if journal not in journal_codes and journal in JOURNAL_ISSN_MAP:
                journal_codes.append(journal)

        if journal_codes or "openalex" in self.enabled_sources:
            # 使用期刊中最大的单独配置值，如果都没有则用全局默认
            openalex_max = max(
                [self._get_max_results("openalex")]
                + [self._get_max_results(jc) for jc in journal_codes]
            )
            self.sources["openalex"] = OpenAlexSource(
                history_dir=self.history_dir,
                journals=journal_codes,
                max_results=openalex_max,
                email=self.openalex_email,
                api_key=self.openalex_api_key,
                search_terms=self.openalex_search_terms,
            )
            # 注入代理
            openalex_proxy = _settings.get_proxy_dict("openalex")
            if openalex_proxy:
                self.sources["openalex"].session.proxies.update(openalex_proxy)
                logger.info("[SearchAgent] OpenAlex 已配置网络代理")
            self._journal_codes = journal_codes
            logger.info(
                f"[SearchAgent] 已启用 OpenAlex 数据源，"
                f"主题检索: {len(self.openalex_search_terms)} 条，期刊: {journal_codes}"
            )
        else:
            self._journal_codes = []

        # 注入代理到 Semantic Scholar
        if self.semantic_scholar_enricher:
            s2_proxy = _settings.get_proxy_dict("semantic_scholar")
            if s2_proxy:
                self.semantic_scholar_enricher.session.proxies.update(s2_proxy)
                logger.info("[SearchAgent] Semantic Scholar 已配置网络代理")

        if "dblp" in self.enabled_sources and self.dblp_venues:
            self.sources["dblp"] = DblpSource(
                history_dir=self.history_dir,
                venues=self.dblp_venues,
                title_terms=self.dblp_title_terms,
                max_results=self._get_max_results("dblp"),
            )
            logger.info(f"[SearchAgent] 已启用 DBLP 会议源: {self.dblp_venues}")

        if "institutional" in self.enabled_sources and self.institutional_feeds:
            self.sources["institutional"] = InstitutionalRssSource(
                history_dir=self.history_dir,
                feeds=self.institutional_feeds,
                max_results=self._get_max_results("institutional"),
            )
            logger.info(
                f"[SearchAgent] 已启用 {len(self.institutional_feeds)} 个官方机构 RSS 源"
            )

        if "worldbank" in self.enabled_sources and self.worldbank_search_terms:
            self.sources["worldbank"] = WorldBankSource(
                history_dir=self.history_dir,
                search_terms=self.worldbank_search_terms,
                max_results=self._get_max_results("worldbank"),
            )
            logger.info("[SearchAgent] 已启用世界银行政策研究工作论文源")

        if "repec" in self.enabled_sources and self.repec_series:
            self.sources["repec"] = RepecSeriesSource(
                history_dir=self.history_dir,
                series=self.repec_series,
                max_results=self._get_max_results("repec"),
            )
            logger.info(f"[SearchAgent] 已启用 {len(self.repec_series)} 个 RePEc 免费全文系列")

    def fetch_all_papers(self, days: int = 7) -> Dict[str, List[PaperMetadata]]:
        """
        从所有启用的数据源抓取论文。

        参数:
            days: 搜索最近 N 天的论文

        返回:
            Dict[str, List[PaperMetadata]]: {数据源名: 论文列表}
            例如: {"arxiv": [...], "prl": [...], "pra": [...]}
        """
        results = {}

        for source_name, source in self.sources.items():
            logger.info(f">>> 从 {source.display_name} 抓取论文...")

            try:
                if source_name == "arxiv":
                    papers = source.fetch_papers(days=days, domains=self.arxiv_domains)
                    results["arxiv"] = papers

                elif source_name == "openalex":
                    # OpenAlex 返回的论文按期刊分组
                    papers = source.fetch_papers(days=days)
                    # 增强：获取 Semantic Scholar TLDR
                    if self.enable_semantic_scholar and self.semantic_scholar_enricher:
                        papers = self._enrich_with_semantic_scholar(papers)
                    # 按 source 字段分组（期刊代码）
                    for paper in papers:
                        if paper.source not in results:
                            results[paper.source] = []
                        results[paper.source].append(paper)

                elif source_name == "dblp":
                    papers = source.fetch_papers(days=days)
                    papers = self._enrich_dblp_with_openalex(papers)
                    if self.enable_semantic_scholar and self.semantic_scholar_enricher:
                        papers = self._enrich_with_semantic_scholar(papers)
                    for paper in papers:
                        results.setdefault(paper.source, []).append(paper)

                elif source_name == "institutional":
                    papers = source.fetch_papers(days=days)
                    for paper in papers:
                        results.setdefault(paper.source, []).append(paper)

                elif source_name == "repec":
                    papers = source.fetch_papers(days=days)
                    for paper in papers:
                        results.setdefault(paper.source, []).append(paper)

                else:
                    papers = source.fetch_papers(days=days)
                    results[source_name] = papers

            except Exception as e:
                logger.error(f"[{source_name}] 抓取失败: {e}")
                import traceback

                traceback.print_exc()

        self._resolve_missing_arxiv_versions(results)
        self._resolve_missing_open_access(results)
        results = self._deduplicate_across_sources(results)

        # 统计
        total = sum(len(papers) for papers in results.values())
        logger.info(f">>> 总计抓取 {total} 篇论文，来自 {len(results)} 个数据源")

        return results

    def _resolve_missing_arxiv_versions(self, results: Dict[str, List[PaperMetadata]]) -> int:
        """Actively search ArXiv for papers whose upstream metadata has no PDF."""
        arxiv_source = self.sources.get("arxiv")
        if not arxiv_source:
            return 0
        resolved = 0
        attempted = 0
        for source, papers in results.items():
            if source == "arxiv":
                continue
            for paper in papers:
                if paper.has_pdf_access() or attempted >= 20:
                    continue
                attempted += 1
                match = arxiv_source.find_by_title(paper.title, paper.authors, paper.doi)
                if not match:
                    continue
                paper.arxiv_id = match.arxiv_id
                paper.arxiv_url = match.arxiv_url
                paper.pdf_url = match.pdf_url
                paper.abstract = paper.abstract or match.abstract
                paper.categories = paper.categories or match.categories
                resolved += 1
                logger.info(f">>> ArXiv 反查命中: {paper.title[:55]} -> {match.arxiv_id}")
        if attempted:
            logger.info(f">>> 缺失全文主动反查: 尝试 {attempted} 篇，找到 ArXiv 版本 {resolved} 篇")
        return resolved

    def _resolve_missing_open_access(self, results: Dict[str, List[PaperMetadata]]) -> int:
        """Try lawful repository APIs after ArXiv resolution has been exhausted."""
        resolved = 0
        attempted = 0
        for source, papers in results.items():
            if source == "arxiv":
                continue
            for paper in papers:
                if paper.arxiv_id or paper.fulltext_provenance or attempted >= 40:
                    continue
                attempted += 1
                candidate = self.open_access_resolver.resolve(paper)
                if not candidate:
                    continue
                paper.pdf_url = candidate["pdf_url"]
                paper.fulltext_provenance = candidate
                resolved += 1
                logger.info(
                    f">>> 开放全文命中 [{candidate['provider']}]: {paper.title[:55]}"
                )
        if attempted:
            logger.info(f">>> 合法开放全文反查: 尝试 {attempted} 篇，命中 {resolved} 篇")
        return resolved

    def _enrich_dblp_with_openalex(
        self, papers: List[PaperMetadata]
    ) -> List[PaperMetadata]:
        openalex = self.sources.get("openalex")
        if not openalex:
            return papers
        lookup = openalex.lookup_by_dois([paper.doi for paper in papers if paper.doi])
        enriched = 0
        for paper in papers:
            match = lookup.get(self._doi_key(paper.doi))
            if not match:
                continue
            paper.abstract = match.abstract or paper.abstract
            paper.authors = match.authors or paper.authors
            paper.pdf_url = match.pdf_url or paper.pdf_url
            paper.openalex_id = match.openalex_id
            paper.cited_by_count = match.cited_by_count
            paper.topics = match.topics
            paper.arxiv_id = match.arxiv_id
            paper.arxiv_url = match.arxiv_url
            paper.publication_type = match.publication_type or paper.publication_type
            paper.referenced_works = match.referenced_works
            paper.related_works = match.related_works
            enriched += 1
        logger.info(f">>> DBLP → OpenAlex 元数据增强: {enriched}/{len(papers)} 篇")
        return papers

    @staticmethod
    def _title_key(title: str) -> str:
        """生成跨来源标题指纹，仅用于严格标题去重。"""
        return re.sub(r"[^a-z0-9]+", "", (title or "").lower())

    @staticmethod
    def _doi_key(doi: Optional[str]) -> str:
        return (doi or "").lower().replace("https://doi.org/", "").strip()

    def _deduplicate_across_sources(
        self, results: Dict[str, List[PaperMetadata]]
    ) -> Dict[str, List[PaperMetadata]]:
        """合并 ArXiv 与 OpenAlex 的同一论文，优先保留可下载的 ArXiv 记录。"""
        arxiv_papers = results.get("arxiv", [])
        by_doi = {self._doi_key(p.doi): p for p in arxiv_papers if self._doi_key(p.doi)}
        by_title = {self._title_key(p.title): p for p in arxiv_papers if self._title_key(p.title)}

        deduped_openalex = []
        merged = 0
        for paper in results.get("openalex", []):
            existing = by_doi.get(self._doi_key(paper.doi)) or by_title.get(
                self._title_key(paper.title)
            )
            if not existing:
                deduped_openalex.append(paper)
                continue

            existing.doi = existing.doi or paper.doi
            existing.journal = existing.journal or paper.journal
            existing.openalex_id = paper.openalex_id
            existing.cited_by_count = max(existing.cited_by_count, paper.cited_by_count)
            existing.publication_type = paper.publication_type
            existing.topics = paper.topics
            existing.semantic_scholar_tldr = (
                existing.semantic_scholar_tldr or paper.semantic_scholar_tldr
            )
            existing.semantic_scholar_id = paper.semantic_scholar_id
            existing.semantic_scholar_url = paper.semantic_scholar_url
            existing.influential_citation_count = paper.influential_citation_count
            existing.referenced_works = paper.referenced_works
            existing.related_works = paper.related_works
            existing.pdf_url = existing.pdf_url or paper.pdf_url
            merged += 1

        if "openalex" in results:
            results["openalex"] = deduped_openalex

        canonical = results.get("arxiv", []) + results.get("openalex", [])
        canonical_by_doi = {
            self._doi_key(p.doi): p for p in canonical if self._doi_key(p.doi)
        }
        canonical_by_title = {
            self._title_key(p.title): p for p in canonical if self._title_key(p.title)
        }
        dblp_merged = 0
        for venue in getattr(self, "dblp_venues", []):
            deduped_venue = []
            for paper in results.get(venue, []):
                existing = canonical_by_doi.get(self._doi_key(paper.doi)) or canonical_by_title.get(
                    self._title_key(paper.title)
                )
                if not existing:
                    deduped_venue.append(paper)
                    continue
                existing.journal = existing.journal or paper.journal
                existing.doi = existing.doi or paper.doi
                existing.pdf_url = existing.pdf_url or paper.pdf_url
                existing.arxiv_id = existing.arxiv_id or paper.arxiv_id
                existing.arxiv_url = existing.arxiv_url or paper.arxiv_url
                if "dblp" in self.sources:
                    self.sources["dblp"].mark_as_processed(paper.paper_id)
                dblp_merged += 1
            if venue in results:
                results[venue] = deduped_venue

        if merged:
            logger.info(f">>> 跨来源去重: 合并 {merged} 篇 ArXiv/OpenAlex 重复论文")
        if dblp_merged:
            logger.info(f">>> 跨来源去重: 合并 {dblp_merged} 篇 DBLP 重复论文")
        return results

    def _enrich_with_semantic_scholar(self, papers: List[PaperMetadata]) -> List[PaperMetadata]:
        """
        使用 Semantic Scholar 增强论文元数据（添加 TLDR 和 arXiv 信息）。

        参数:
            papers: 论文列表

        返回:
            List[PaperMetadata]: 增强后的论文列表
        """
        if not self.semantic_scholar_enricher:
            return papers

        logger.info("  正在从 Semantic Scholar 批量获取增强信息...")
        enriched_count = 0
        arxiv_found_count = 0
        dois = [paper.doi for paper in papers if paper.doi]
        batch_info = self.semantic_scholar_enricher.get_papers_info_batch(dois)

        for paper in papers:
            doi_key = self._doi_key(paper.doi)
            paper_info = batch_info.get(doi_key)
            if not paper_info:
                continue

            paper.semantic_scholar_id = paper_info.get("paper_id")
            paper.semantic_scholar_url = paper_info.get("url")
            paper.abstract = paper.abstract or paper_info.get("abstract") or ""
            paper.influential_citation_count = paper_info.get(
                "influential_citation_count", 0
            )
            if paper_info.get("venue") and paper.journal == "OpenAlex":
                paper.journal = paper_info["venue"]
            if paper_info.get("tldr"):
                paper.semantic_scholar_tldr = paper_info["tldr"]
                enriched_count += 1
            if paper_info.get("pdf_url"):
                paper.pdf_url = paper.pdf_url or paper_info["pdf_url"]

            arxiv_id = paper_info.get("arxiv_id")
            if arxiv_id:
                paper.arxiv_id = paper.arxiv_id or arxiv_id
                paper.arxiv_url = paper.arxiv_url or f"https://arxiv.org/abs/{arxiv_id}"
                paper.pdf_url = paper.pdf_url or f"https://arxiv.org/pdf/{arxiv_id}.pdf"
                arxiv_found_count += 1
                logger.debug(f"    找到 arXiv 版本: {arxiv_id}")

        if enriched_count > 0 or arxiv_found_count > 0:
            logger.info(f"    TLDR: {enriched_count}/{len(papers)} 篇")
            logger.info(f"    arXiv版本: {arxiv_found_count}/{len(papers)} 篇")
        else:
            logger.info("    未获取到增强信息")

        return papers

    def mark_as_processed(self, paper_id: str, source: str):
        """
        标记论文为已处理。

        参数:
            paper_id: 论文 ID
            source: 数据源名称（arxiv 或期刊代码）
        """
        # ArXiv 论文
        if source == "arxiv" and "arxiv" in self.sources:
            self.sources["arxiv"].mark_as_processed(paper_id)
        elif source in getattr(self, "dblp_venues", []) and "dblp" in self.sources:
            self.sources["dblp"].mark_as_processed(paper_id)
        # 期刊论文（都通过 openalex）
        elif "openalex" in self.sources:
            self.sources["openalex"].mark_as_processed(paper_id)

    def get_source(self, source_name: str) -> Optional[BasePaperSource]:
        """获取指定的数据源实例"""
        if source_name == "arxiv":
            return self.sources.get("arxiv")
        # 期刊通过 openalex
        return self.sources.get("openalex")

    def can_download_pdf(self, source: str) -> bool:
        """检查指定数据源是否支持 PDF 下载"""
        if source == "arxiv":
            return True
        return False  # 期刊默认不支持

    def get_enabled_sources(self) -> List[str]:
        """获取所有启用的数据源名称"""
        sources = []
        if "arxiv" in self.sources:
            sources.append("arxiv")
        if "openalex" in self.sources:
            # 添加具体的期刊代码
            sources.extend(self._journal_codes)
        return sources

    @staticmethod
    def get_available_journals() -> Dict[str, Dict]:
        """获取所有可用的期刊列表"""
        return JOURNAL_ISSN_MAP
