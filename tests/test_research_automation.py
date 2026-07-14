import base64
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from enrichers.github_code import GitHubCodeEnricher
from enrichers.open_access import OpenAccessResolver
from agents.analysis_agent import AnalysisAgent
from config import settings
from library.feedback import FeedbackStore
from library.research_library import ResearchLibrary
from library.evidence_builder import build_evidence_pack, audit_weekly_digest
from sources.base_source import PaperMetadata
from sources.citation_discovery import CitationDiscovery
from sources.institutional_rss_source import InstitutionalRssSource
from sources.repec_series_source import RepecSeriesSource
from sources.search_agent import SearchAgent
from sources.worldbank_source import WorldBankSource
from sync_feedback import parse_events, parse_feedback
from rescore_history import SCORING_VERSION, apply_score, build_scoring_evidence
from resend_last_wechat import (
    build_recent_result,
    build_result,
    select_latest_complete_batch,
    select_recent_full_text,
)
from notifications.notifier import NotifierAgent, RunResult, WebhookNotifier


class ResearchAutomationTests(unittest.TestCase):
    def test_resend_filters_abstract_analysis_and_stays_on_requested_date(self):
        records = [
            {
                "paper_id": "full",
                "title": "Full text paper",
                "source": "arxiv",
                "score": 70,
                "qualified": True,
                "updated_at": "2026-07-14T03:57:01",
                "analysis": {"_analysis_basis": "full_text", "summary": "Full"},
            },
            {
                "paper_id": "abstract",
                "title": "Abstract paper",
                "source": "openalex",
                "score": 90,
                "qualified": True,
                "updated_at": "2026-07-14T03:57:02",
                "analysis": {"_analysis_basis": "abstract", "summary": "Abstract"},
            },
            {
                "paper_id": "yesterday",
                "title": "Yesterday full text",
                "source": "arxiv",
                "score": 95,
                "qualified": True,
                "updated_at": "2026-07-13T06:39:01",
                "analysis": {"_analysis_basis": "full_text", "summary": "Old"},
            },
        ]

        key, batch = select_latest_complete_batch(
            records,
            5,
            full_text_only=True,
            batch_date="2026-07-14",
            allow_fewer=True,
        )
        result = build_result(key, batch, 5, full_text_only=True)

        self.assertEqual(key, "2026-07-14T03:57")
        self.assertEqual([paper["paper_id"] for paper in result.top_papers], ["full"])
        self.assertEqual(result.total_analyzed, 1)
        self.assertIn("仅全文", result.run_timestamp)

    def test_recent_resend_excludes_old_papers_and_prefers_direct_sources(self):
        def paper(paper_id, published, source, score=70):
            return {
                "paper_id": paper_id,
                "title": paper_id,
                "source": source,
                "score": score,
                "qualified": True,
                "published_date": published,
                "analysis": {"_analysis_basis": "full_text", "summary": "Full"},
            }

        records = [
            paper("old-high-score", "1996-02-01", "citation", 100),
            paper("repository-high-score", "2026-07-13", "openalex", 99),
            paper("arxiv-one", "2026-07-12", "arxiv", 80),
            paper("bis-one", "2026-07-11", "bis", 70),
            paper("ecb-one", "2026-07-10", "ecb", 60),
            paper("imf-one", "2026-07-09", "imf", 50),
            paper("oecd-one", "2026-07-08", "oecd", 40),
        ]

        selected = select_recent_full_text(
            records, 5, recent_days=30, as_of_date=datetime(2026, 7, 14).date()
        )
        result = build_recent_result(
            selected, 30, as_of_date=datetime(2026, 7, 14).date()
        )

        self.assertNotIn("old-high-score", [item["paper_id"] for item in selected])
        self.assertNotIn("repository-high-score", [item["paper_id"] for item in selected])
        self.assertEqual(len(selected), 5)
        self.assertEqual(result.summary_mode, "curated")
        overview_agent = NotifierAgent.__new__(NotifierAgent)
        overview_agent.settings = SimpleNamespace(RESEARCH_FIELD_NAME="测试")
        overview = overview_agent._format_wechat_overview(result)
        self.assertIn("近 30 天全文精选 **5** 篇", overview)
        self.assertNotIn("抓取 **5**", overview)

    def test_historical_rescore_prefers_abstract_then_existing_analysis(self):
        evidence, basis = build_scoring_evidence(
            {
                "abstract": "Bank lending responds to monetary tightening.",
                "analysis": {"summary": "This should not replace the abstract."},
            }
        )
        self.assertEqual(basis, "abstract")
        self.assertIn("Bank lending", evidence)

        evidence, basis = build_scoring_evidence(
            {"abstract": "", "analysis": {"summary": "Fiscal multipliers vary."}}
        )
        self.assertEqual(basis, "existing_analysis")
        self.assertIn("Fiscal multipliers", evidence)

    def test_historical_rescore_updates_scores_without_replacing_analysis(self):
        record = {
            "paper_id": "paper:1",
            "title": "Monetary Transmission",
            "analysis": {"summary": "Keep this analysis."},
            "tldr": "Keep this summary.",
            "personalization": {"active": True, "adjustment": 4.0},
        }
        score = SimpleNamespace(
            total_score=72.0,
            is_qualified=True,
            domain_scores={
                "commercial_banking": 5.0,
                "monetary_policy": 7.2,
                "fiscal_policy": 2.0,
            },
            matched_domain="monetary_policy",
            reasoning="货币政策传导是论文主线。",
        )
        updated = apply_score(record, score, "abstract", "2026-07-14T00:00:00Z")

        self.assertEqual(updated["score"], 72.0)
        self.assertTrue(updated["qualified"])
        self.assertEqual(updated["analysis"], record["analysis"])
        self.assertEqual(updated["tldr"], record["tldr"])
        self.assertEqual(updated["personalization"]["personalized_score"], 76.0)
        self.assertEqual(updated["scoring"]["version"], SCORING_VERSION)

    def test_research_page_renders_independent_domain_scores(self):
        markdown = ResearchLibrary.render_record(
            {
                "paper_id": "paper:2",
                "title": "Bank Credit Supply",
                "score": 81,
                "domain_scores": {
                    "commercial_banking": 8.1,
                    "monetary_policy": 5.0,
                    "fiscal_policy": 1.0,
                },
                "matched_domain": "commercial_banking",
                "scoring": {"evidence_basis": "abstract"},
                "score_reasoning": "银行信贷供给是核心研究对象。",
            }
        )
        self.assertIn("商业银行**：8.1/10（最高匹配）", markdown)
        self.assertIn("评分依据**：论文摘要", markdown)
        self.assertIn("银行信贷供给是核心研究对象", markdown)

    def test_domain_scoring_passes_when_one_domain_is_core(self):
        groups = {
            "commercial_banking": {"label": "商业银行", "keywords": ["bank lending"]},
            "monetary_policy": {"label": "货币政策", "keywords": ["policy rate"]},
            "fiscal_policy": {"label": "财政政策", "keywords": ["public debt"]},
        }
        agent = AnalysisAgent.__new__(AnalysisAgent)
        agent._call_cheap_llm = Mock(return_value=json.dumps({
            "domain_scores": {
                "commercial_banking": 2.0,
                "monetary_policy": 7.2,
                "fiscal_policy": 1.0,
            },
            "expert_authors_found": [],
            "reasoning": "货币政策传导是主要研究问题。",
            "tldr": "研究政策利率传导。",
            "extracted_keywords": ["monetary policy transmission"],
        }))
        with unittest.mock.patch.object(settings, "DOMAIN_KEYWORD_GROUPS", groups), \
             unittest.mock.patch.object(settings, "DOMAIN_PASSING_SCORE", 6.0):
            result = agent.score_paper_with_keywords(
                "Policy Rate Transmission", "Researcher", "We estimate policy transmission.", {}
            )

        self.assertTrue(result.is_qualified)
        self.assertEqual(result.passing_score, 60.0)
        self.assertEqual(result.total_score, 72.0)
        self.assertEqual(result.matched_domain, "monetary_policy")

    def test_search_agent_marks_repec_history_in_repec_owner(self):
        agent = SearchAgent.__new__(SearchAgent)
        repec = Mock()
        openalex = Mock()
        agent.sources = {"repec": repec, "openalex": openalex}
        agent._source_owner = {"imf": "repec"}
        agent.mark_as_processed("repec:paper", "imf")
        repec.mark_as_processed.assert_called_once_with("repec:paper")
        openalex.mark_as_processed.assert_not_called()

    def test_search_agent_reports_pdf_support_from_source_owner(self):
        agent = SearchAgent.__new__(SearchAgent)
        repec = Mock()
        repec.can_download_pdf.return_value = True
        agent.sources = {"repec": repec}
        agent._source_owner = {"imf": "repec"}
        self.assertTrue(agent.can_download_pdf("imf"))

    def test_search_agent_migrates_legacy_repec_history(self):
        agent = SearchAgent.__new__(SearchAgent)
        openalex = Mock()
        openalex.history = {"repec:paper": "2026-07-13", "https://openalex.org/W1": "2026-07-13"}
        repec = Mock()
        repec.is_processed.return_value = False
        agent.sources = {"openalex": openalex, "repec": repec}
        agent._source_owner = {"imf": "repec"}
        self.assertEqual(agent._migrate_legacy_source_history(), 1)
        repec.mark_as_processed.assert_called_once_with("repec:paper")

    def test_repec_series_keeps_only_free_records_and_direct_pdf(self):
        series_html = '<a href="/p/iza/izadps/dp18753.html">Paper</a>'
        item_html = """
        <meta name="handle" content="RePEc:iza:izadps:dp18753">
        <meta name="freedownload" content="1">
        <meta name="citation_title" content="Fiscal Policy and Federal Balance">
        <meta name="citation_abstract" content="Evidence on fiscal transfers.">
        <meta name="citation_authors" content="Ada One; Bo Two">
        <meta name="citation_publication_date" content="2026/07/12">
        <meta name="citation_journal_title" content="IZA Discussion Papers">
        <input type="radio" name="url" value="https://docs.iza.org/dp18753.pdf">
        """
        with tempfile.TemporaryDirectory() as tmp:
            source = RepecSeriesSource(
                Path(tmp),
                [{"name": "iza", "display_name": "IZA Discussion Papers", "url": "https://ideas.repec.org/s/iza/izadps.html"}],
            )
            series_response = Mock(text=series_html, url="https://ideas.repec.org/s/iza/izadps.html")
            series_response.raise_for_status.return_value = None
            item_response = Mock(text=item_html, url="https://ideas.repec.org/p/iza/izadps/dp18753.html")
            item_response.raise_for_status.return_value = None
            source.session.get = Mock(side_effect=[series_response, item_response])

            papers = source.fetch_papers(days=30)

        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0].source, "iza")
        self.assertEqual(papers[0].pdf_url, "https://docs.iza.org/dp18753.pdf")
        self.assertEqual(papers[0].fulltext_provenance["provider"], "repec_free_fulltext")

    def test_repec_series_rejects_restricted_record(self):
        series_html = '<a href="/p/test/series/1.html">Paper</a>'
        item_html = '<meta name="handle" content="RePEc:test:series:1"><meta name="freedownload" content="0"><meta name="citation_title" content="Restricted">'
        with tempfile.TemporaryDirectory() as tmp:
            source = RepecSeriesSource(
                Path(tmp), [{"name": "test", "url": "https://ideas.repec.org/s/test/series.html"}]
            )
            first = Mock(text=series_html, url="https://ideas.repec.org/s/test/series.html")
            first.raise_for_status.return_value = None
            second = Mock(text=item_html, url="https://ideas.repec.org/p/test/series/1.html")
            second.raise_for_status.return_value = None
            source.session.get = Mock(side_effect=[first, second])
            papers = source.fetch_papers(days=30)
        self.assertEqual(papers, [])

    def test_repec_series_uses_current_year_section_before_featured_links(self):
        year = datetime.now().year
        html = f'''<a href="/p/test/series/old.html">Featured old paper</a>
        <h3>{year}</h3><div><a href="/p/test/series/new.html">Newest paper</a></div>
        <h3>{year - 1}</h3><a href="/p/test/series/last-year.html">Older paper</a>'''
        with tempfile.TemporaryDirectory() as tmp:
            source = RepecSeriesSource(Path(tmp), [])
            response = Mock(text=html, url="https://ideas.repec.org/s/test/series.html")
            response.raise_for_status.return_value = None
            source.session.get = Mock(return_value=response)
            links = source._item_links("https://ideas.repec.org/s/test/series.html", 5)
        self.assertEqual(links, ["https://ideas.repec.org/p/test/series/new.html"])

    def test_repec_series_rejects_old_year_when_date_is_imprecise(self):
        series_html = '<a href="/p/test/series/old.html">Old paper</a>'
        item_html = '''<meta name="handle" content="RePEc:test:series:old">
        <meta name="freedownload" content="1"><meta name="citation_year" content="1996">
        <meta name="citation_publication_date" content="November 1996">
        <meta name="citation_title" content="Old paper"><input name="url" value="https://example.test/old.pdf">'''
        with tempfile.TemporaryDirectory() as tmp:
            source = RepecSeriesSource(Path(tmp), [{"name": "test", "url": "https://ideas.repec.org/s/test/series.html"}])
            first = Mock(text=series_html, url="https://ideas.repec.org/s/test/series.html")
            first.raise_for_status.return_value = None
            second = Mock(text=item_html, url="https://ideas.repec.org/p/test/series/old.html")
            second.raise_for_status.return_value = None
            source.session.get = Mock(side_effect=[first, second])
            papers = source.fetch_papers(days=14)
        self.assertEqual(papers, [])

    def test_institutional_rss_maps_official_pdf_and_abstract(self):
        rss = b"""<?xml version="1.0"?><rss version="2.0"><channel>
        <item><guid>paper-1</guid><title>A theory of bank liquidity requirements</title>
        <link>https://institution.example/paper.pdf</link>
        <description>Bank liquidity and regulation.</description>
        <pubDate>Thu, 09 Jul 2026 11:00:00 GMT</pubDate>
        </item></channel></rss>"""
        with tempfile.TemporaryDirectory() as tmp:
            source = InstitutionalRssSource(
                Path(tmp),
                [{"name": "ecb", "display_name": "ECB Working Papers", "url": "https://feed"}],
            )
            response = Mock(content=rss)
            response.raise_for_status.return_value = None
            source.session.get = Mock(return_value=response)

            papers = source.fetch_papers(days=30)

        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0].source, "ecb")
        self.assertEqual(papers[0].pdf_url, "https://institution.example/paper.pdf")
        self.assertEqual(
            papers[0].fulltext_provenance["provider"], "official_institution_rss"
        )

    def test_worldbank_maps_policy_working_paper(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = WorldBankSource(Path(tmp), ["monetary policy"])
            response = Mock()
            response.raise_for_status.return_value = None
            response.json.return_value = {
                "documents": {
                    "D1": {
                        "id": "1",
                        "display_title": "Monetary Policy and Bank Lending",
                        "docdt": "2026-07-12T00:00:00Z",
                        "abstracts": {"cdata!": "Evidence from bank credit."},
                        "pdfurl": "http://documents.worldbank.org/paper.pdf",
                        "url": "http://documents.worldbank.org/paper",
                    },
                    "facets": {},
                }
            }
            source.session.get = Mock(return_value=response)

            papers = source.fetch_papers(days=30)

        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0].paper_id, "worldbank:1")
        self.assertEqual(papers[0].pdf_url, "https://documents.worldbank.org/paper.pdf")
        self.assertEqual(
            papers[0].fulltext_provenance["provider"], "worldbank_documents_api"
        )

    def test_wechat_webhook_rejects_api_error_in_http_200(self):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {"errcode": 93000, "errmsg": "robot webhook error"}
        with unittest.mock.patch(
            "notifications.notifier.requests.post", return_value=response
        ):
            notifier = WebhookNotifier("wechat_work", "https://example.test/webhook")
            with self.assertRaisesRegex(RuntimeError, "93000"):
                notifier.send("subject", "body")

    def test_notify_reports_partial_wechat_delivery_failure(self):
        agent = NotifierAgent.__new__(NotifierAgent)
        agent.settings = SimpleNamespace(
            NOTIFY_ON_SUCCESS=True,
            NOTIFY_ON_FAILURE=True,
            NOTIFY_ATTACH_REPORTS=False,
            TOKEN_TRACKING_ENABLED=False,
        )
        notifier = Mock(spec=WebhookNotifier)
        notifier.platform = "wechat_work"
        notifier.send.side_effect = [True, RuntimeError("timeout")]
        agent.notifiers = [notifier]
        result = RunResult(
            success=True,
            top_papers=[{"paper_id": "arxiv:1", "title": "Paper"}],
        )

        self.assertFalse(agent.notify(result))

    def test_notify_sends_dingtalk_overview_and_paper_card(self):
        agent = NotifierAgent.__new__(NotifierAgent)
        agent.settings = SimpleNamespace(
            NOTIFY_ON_SUCCESS=True,
            NOTIFY_ON_FAILURE=True,
            NOTIFY_ATTACH_REPORTS=False,
            TOKEN_TRACKING_ENABLED=False,
            RESEARCH_FIELD_NAME="商业银行、财政和货币政策",
        )
        notifier = Mock(spec=WebhookNotifier)
        notifier.platform = "dingtalk"
        agent.notifiers = [notifier]
        result = RunResult(
            success=True,
            top_papers=[
                {
                    "paper_id": "doi:banking",
                    "title": "Banking Paper",
                    "source": "openalex",
                    "journal": "Journal of Banking & Finance",
                    "publication_type": "journal-article",
                    "published_date": "2026-07-13T00:00:00",
                    "score": 80,
                    "analysis": {"_analysis_basis": "full_text", "summary": "结论"},
                }
            ],
        )

        self.assertTrue(agent.notify(result))
        self.assertEqual(notifier.send.call_count, 2)

    def test_knowledge_report_renders_analysis_as_native_markdown(self):
        report = ResearchLibrary.render_record(
            {
                "paper_id": "arxiv:1",
                "title": "Original Paper Title",
                "authors": ["Ada", "Lin"],
                "source": "arxiv",
                "score": 88,
                "url": "https://arxiv.org/abs/1",
                "abstract": "English abstract.",
                "abstract_cn": "中文摘要。",
                "tldr": "一句话总结。",
                "analysis": {
                    "_analysis_basis": "full_text",
                    "chinese_title": "中文论文标题",
                    "summary": "完整核心结论。",
                    "innovations": ["创新一", "创新二"],
                    "methodology": "完整研究方法。",
                    "key_results": ["结果一", "结果二"],
                    "tech_stack": ["T5", "LightGCN"],
                    "limitations": ["局限一"],
                },
            }
        )
        self.assertIn("# 中文论文标题", report)
        self.assertIn("### 核心结论", report)
        self.assertIn("- 创新一", report)
        self.assertIn("<details>", report)
        self.assertNotIn("```json", report)
        self.assertNotIn('"methodology":', report)

    def test_knowledge_report_uses_configured_field_tag(self):
        report = ResearchLibrary.render_record(
            {
                "paper_id": "doi:banking",
                "title": "A Banking Paper",
                "research_field_tag": "banking-fiscal-monetary-policy",
            }
        )

        self.assertIn('"banking-fiscal-monetary-policy"', report)
        self.assertNotIn('"recommender-systems"', report)

    def test_wechat_paper_card_uses_deep_analysis(self):
        agent = NotifierAgent.__new__(NotifierAgent)
        with unittest.mock.patch.dict(
            os.environ, {"FEEDBACK_REPO_URL": "https://github.com/o/r"}
        ):
            card = agent._format_wechat_paper_card(
                {
                    "paper_id": "arxiv:1",
                    "title": "An English Paper",
                    "source": "arxiv",
                    "score": 88,
                    "url": "https://arxiv.org/abs/1",
                    "tldr": "short",
                    "analysis": {
                        "_analysis_basis": "full_text",
                        "chinese_title": "一篇论文",
                        "summary": "完整核心结论",
                        "methodology": "完整方法",
                        "key_results": ["关键结果"],
                        "limitations": ["主要局限"],
                    },
                    "code_repositories": [],
                },
                1,
                5,
            )
        self.assertIn("全文深读", card)
        self.assertIn("完整方法", card)
        self.assertIn("关键结果", card)
        self.assertIn("主要局限", card)
        self.assertNotIn("未获取论文正文", card)
        self.assertLessEqual(len(card.encode("utf-8")), 4000)

    def test_dingtalk_card_keeps_report_and_feedback_links(self):
        agent = NotifierAgent.__new__(NotifierAgent)
        with unittest.mock.patch.dict(
            os.environ,
            {
                "FEEDBACK_REPO_URL": "https://github.com/o/r",
                "FEEDBACK_API_URL": "https://feedback.example.workers.dev",
                "FEEDBACK_SIGNING_SECRET": "test-secret",
            },
        ):
            card = agent._format_dingtalk_paper_cards(
                {
                    "paper_id": "doi:banking",
                    "title": "Banking Paper",
                    "source": "openalex",
                    "journal": "Journal of Banking & Finance",
                    "publication_type": "journal-article",
                    "published_date": "2026-07-13T00:00:00",
                    "score": 80,
                    "url": "https://example.test/paper",
                    "analysis": {"_analysis_basis": "full_text", "summary": "结论"},
                },
                1,
                1,
            )[0]

        self.assertIn("[深度报告]", card)
        self.assertIn("[查看原文]", card)
        self.assertIn("[喜欢]", card)
        self.assertIn("[忽略]", card)
        self.assertIn("feedback.example.workers.dev/feedback", card)
        self.assertNotIn("<font", card)
        self.assertIn("**期刊 / 会议 / 系列**\n> Journal of Banking & Finance", card)
        self.assertIn("`期刊论文` · `2026-07-13`", card)
        self.assertIn("全文深读 · 基础分 **80.0**", card)
        self.assertIn("发现渠道：OPENALEX", card)
        self.assertIn("[深度报告]", card)
        self.assertIn("[查看原文]", card)
        self.assertIn("\n\n[喜欢]", card)

    def test_wechat_abstract_card_prominently_marks_missing_full_text(self):
        agent = NotifierAgent.__new__(NotifierAgent)
        card = agent._format_wechat_paper_card(
            {
                "paper_id": "doi:abstract-only",
                "title": "Abstract Only Paper",
                "source": "www",
                "score": 50,
                "analysis": {
                    "_analysis_basis": "abstract",
                    "summary": "摘要结论",
                },
            },
            1,
            1,
        )

        self.assertIn('<font color="warning">摘要分析</font>', card)
        self.assertIn("未获取论文正文，本卡片仅基于摘要", card)
        self.assertIn("实验细节、关键结果和局限性可能不完整", card)

    def test_wechat_overview_counts_full_text_and_abstract_cards(self):
        agent = NotifierAgent.__new__(NotifierAgent)
        overview = agent._format_wechat_overview(
            RunResult(
                top_papers=[
                    {"analysis": {"_analysis_basis": "full_text"}},
                    {"analysis": {"_analysis_basis": "abstract"}},
                ]
            )
        )

        self.assertIn("全文深读 **1** 篇", overview)
        self.assertIn("仅摘要 **1** 篇", overview)
        self.assertIn("存在未获取正文的论文", overview)

    def test_wechat_overview_uses_configured_research_field(self):
        agent = NotifierAgent.__new__(NotifierAgent)
        agent.settings = SimpleNamespace(RESEARCH_FIELD_NAME="商业银行、财政和货币政策")

        overview = agent._format_wechat_overview(RunResult())

        self.assertIn("## 商业银行、财政和货币政策每日研究", overview)
        self.assertNotIn("推荐系统每日研究", overview)

    def test_structured_limitations_render_as_readable_labels(self):
        limitations = {
            "paper_limitations": "摘要未提供具体局限性。",
            "evidence_limitations": "当前仅基于摘要分析。",
        }
        agent = NotifierAgent.__new__(NotifierAgent)
        card = agent._format_wechat_paper_card(
            {
                "paper_id": "arxiv:structured",
                "title": "Structured Limitations",
                "source": "www",
                "score": 50,
                "analysis": {"summary": "结论", "limitations": limitations},
            },
            1,
            1,
        )
        report = ResearchLibrary.render_record(
            {
                "paper_id": "arxiv:structured",
                "title": "Structured Limitations",
                "analysis": {"summary": "结论", "limitations": limitations},
            }
        )

        for output in (card, report):
            self.assertIn("论文本身局限", output)
            self.assertIn("当前证据局限", output)
            self.assertNotIn("{'paper_limitations'", output)

    def test_wechat_paper_cards_split_without_ellipsis_or_data_loss(self):
        agent = NotifierAgent.__new__(NotifierAgent)
        long_method = "甲" * 3000 + "方法终点"
        limitations = ["局限一", "局限二", "局限三"]
        with unittest.mock.patch.dict(
            os.environ, {"FEEDBACK_REPO_URL": "https://github.com/o/r"}
        ):
            cards = agent._format_wechat_paper_cards(
                {
                    "paper_id": "arxiv:long",
                    "title": "Long Paper",
                    "source": "arxiv",
                    "score": 90,
                    "url": "https://arxiv.org/abs/long",
                    "analysis": {
                        "_analysis_basis": "full_text",
                        "summary": "完整结论",
                        "methodology": long_method,
                        "key_results": ["结果一", "结果二"],
                        "limitations": limitations,
                    },
                    "code_repositories": [],
                },
                1,
                5,
            )
        joined = "".join(cards)
        self.assertGreater(len(cards), 1)
        self.assertNotIn("…", joined)
        self.assertEqual(joined.count("甲"), 3000)
        self.assertIn("方法终点", joined)
        self.assertIn("局限一；局限二；局限三", joined)
        self.assertTrue(all(len(card.encode("utf-8")) <= 4000 for card in cards))

    def test_unpaywall_returns_repository_pdf_with_provenance(self):
        resolver = OpenAccessResolver(email="researcher@example.com")
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "best_oa_location": {
                "url_for_pdf": "https://repository.example.edu/paper.pdf",
                "host_type": "repository",
                "license": "cc-by",
                "version": "acceptedVersion",
            },
            "oa_locations": [],
        }
        resolver.session.get = Mock(return_value=response)
        result = resolver.from_unpaywall("https://doi.org/10.1/example")
        self.assertEqual(result["provider"], "unpaywall")
        self.assertEqual(result["license"], "cc-by")

    def test_openalex_repository_page_can_reveal_pdf(self):
        resolver = OpenAccessResolver()
        resolver._pdf_from_public_page = Mock(
            return_value="https://university.example.edu/files/paper.pdf"
        )
        paper = SimpleNamespace(
            open_access_candidates=[{
                "landing_page_url": "https://university.example.edu/item/1",
                "pdf_url": None,
                "source": "University Repository",
                "source_type": "repository",
                "license": None,
            }]
        )
        result = resolver.from_openalex_locations(paper)
        self.assertEqual(result["provider"], "institutional_or_author_repository")

    def test_openalex_doi_landing_page_is_not_treated_as_pdf(self):
        resolver = OpenAccessResolver()
        paper = SimpleNamespace(
            open_access_candidates=[{
                "landing_page_url": "https://doi.org/10.3386/w1234",
                "pdf_url": "https://doi.org/10.3386/w1234",
                "source": "Working Paper Index",
                "source_type": "repository",
                "license": None,
            }]
        )
        resolver._pdf_from_public_page = Mock(return_value=None)

        self.assertIsNone(resolver.from_openalex_locations(paper))

    def test_openreview_exact_title_returns_public_pdf(self):
        resolver = OpenAccessResolver()
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "notes": [
                {
                    "id": "openreview-note-id",
                    "content": {"title": {"value": "Exact Research Title"}},
                }
            ]
        }
        resolver.session.get = Mock(return_value=response)

        result = resolver.from_openreview("Exact Research Title")

        self.assertEqual(result["provider"], "openreview")
        self.assertEqual(
            result["pdf_url"], "https://openreview.net/pdf?id=openreview-note-id"
        )
    def test_wechat_truncation_never_cuts_markdown_link(self):
        link = "[忽略](https://github.com/example/issues/new?title=paper)\n"
        content = "标题\n" + link + ("普通内容\n" * 300)
        result = WebhookNotifier._truncate_wechat_markdown(content, max_bytes=500)
        self.assertLessEqual(len(result.encode("utf-8")), 500)
        self.assertIn(link.strip(), result)
        self.assertNotIn("https://github.com/example/issues/new?title=paper\n普通内容\n...", result)

    def test_feedback_links_omit_large_issue_body(self):
        with unittest.mock.patch.dict(os.environ, {"FEEDBACK_REPO_URL": "https://github.com/o/r"}):
            links = NotifierAgent._feedback_links(
                {"paper_id": "doi:10.1/example", "title": "A" * 500, "url": "https://example.com"}
            )
        self.assertNotIn("body=", links)
        self.assertIn("[喜欢]", links)
        self.assertIn("[忽略]", links)

    def test_feedback_links_use_signed_one_click_endpoint_when_configured(self):
        with unittest.mock.patch.dict(
            os.environ,
            {
                "FEEDBACK_REPO_URL": "https://github.com/o/r",
                "FEEDBACK_API_URL": "https://feedback.example.workers.dev",
                "FEEDBACK_SIGNING_SECRET": "test-secret",
            },
            clear=False,
        ):
            links = NotifierAgent._feedback_links({"paper_id": "doi:10.1/example"})
        self.assertIn("feedback.example.workers.dev/feedback", links)
        self.assertIn("action=LIKE", links)
        self.assertIn("sig=", links)
        self.assertNotIn("issues/new", links)
    def test_feedback_parser_uses_latest_action(self):
        result = parse_feedback(
            [
                {"number": 1, "title": "[LIKE] arxiv:1"},
                {"number": 2, "title": "[IGNORE] arxiv:1"},
            ]
        )
        self.assertEqual(result, {"liked": [], "ignored": ["arxiv:1"]})

    def test_feedback_store_defers_likes_to_personalization_engine(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "feedback.json"
            path.write_text('{"liked":["p1"],"ignored":[]}', encoding="utf-8")
            score = SimpleNamespace(total_score=70.0, reasoning="base", is_qualified=False)
            FeedbackStore(path).apply("p1", score)
            self.assertEqual(score.total_score, 70.0)
            self.assertFalse(score.is_qualified)
            self.assertIn("个性化引擎", score.reasoning)

    def test_feedback_events_preserve_complete_history(self):
        events = parse_events(
            [
                {"number": 1, "title": "[LIKE] p1", "created_at": "2026-07-01T00:00:00Z"},
                {"number": 2, "title": "[IGNORE] p1", "created_at": "2026-07-02T00:00:00Z"},
            ]
        )
        self.assertEqual([event["action"] for event in events], ["LIKE", "IGNORE"])
        self.assertEqual(events[1]["paper_id"], "p1")

    def test_github_enricher_filters_unrelated_results(self):
        enricher = GitHubCodeEnricher(token="test")
        response = Mock()
        response.status_code = 200
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "items": [
                {
                    "name": "modern-recommender-models",
                    "full_name": "lab/modern-recommender-models",
                    "description": "Modern recommender models with graph learning",
                    "html_url": "https://github.com/lab/modern-recommender-models",
                    "stargazers_count": 42,
                    "updated_at": "2026-01-01T00:00:00Z",
                },
                {"name": "unrelated", "description": "image editor"},
            ]
        }
        readme = Mock()
        readme.status_code = 200
        readme.raise_for_status.return_value = None
        readme.json.return_value = {
            "content": base64.b64encode(b"Modern Recommender Models with Graph Learning").decode()
        }
        enricher.session.get = Mock(side_effect=[response, readme])
        matches = enricher.find("Modern Recommender Models with Graph Learning")
        self.assertEqual([item["full_name"] for item in matches], ["lab/modern-recommender-models"])
        self.assertEqual(matches[0]["classification"], "possible")
        self.assertTrue(matches[0]["evidence"])

    def test_github_enricher_finds_readme_linked_author_pdf(self):
        enricher = GitHubCodeEnricher(token="test")
        readme = Mock()
        readme.status_code = 200
        readme.raise_for_status.return_value = None
        readme.json.return_value = {
            "content": base64.b64encode(
                b"# Exact Research Title\n[paper](blob/The_WebConf_2025_.pdf)"
            ).decode()
        }
        contents = Mock()
        contents.raise_for_status.return_value = None
        contents.json.return_value = {
            "download_url": "https://raw.githubusercontent.com/author/repo/main/paper.pdf"
        }
        enricher.session.get = Mock(side_effect=[readme, contents])

        result = enricher.find_paper_pdf("author/repo", "Exact Research Title")

        self.assertEqual(result["provider"], "github_author_repository")
        self.assertEqual(result["repository"], "author/repo")

    def test_title_only_possible_repository_cannot_supply_fulltext(self):
        repository = {
            "classification": "possible",
            "confidence": 30,
            "evidence": [{"type": "title_in_readme", "overlap": 1.0}],
        }

        self.assertFalse(GitHubCodeEnricher.can_supply_paper_pdf(repository))
        self.assertTrue(
            GitHubCodeEnricher.can_supply_paper_pdf(
                {**repository, "evidence": [{"type": "doi_in_readme"}]}
            )
        )

    def test_edited_book_publication_type_is_visible(self):
        venue, publication_type, date_label, source = NotifierAgent._publication_metadata(
            {
                "journal": "Cambridge University Press eBooks",
                "publication_type": "edited-book",
                "published_date": "2003-12-04T00:00:00",
                "source": "citation",
            }
        )
        self.assertEqual(venue, "Cambridge University Press eBooks")
        self.assertEqual(publication_type, "学术专著")
        self.assertEqual(date_label, "2003-12-04")
        self.assertEqual(source, "CITATION")

    def test_declared_repository_is_official(self):
        enricher = GitHubCodeEnricher(token="test")
        search = Mock(status_code=200)
        search.raise_for_status.return_value = None
        search.json.return_value = {"items": []}
        repo = Mock()
        repo.raise_for_status.return_value = None
        repo.json.return_value = {
            "name": "paper-code",
            "full_name": "author/paper-code",
            "html_url": "https://github.com/author/paper-code",
            "description": "code",
            "owner": {"login": "author"},
            "stargazers_count": 1,
        }
        readme = Mock(status_code=404)
        enricher.session.get = Mock(side_effect=[search, repo, readme])
        matches = enricher.find("Paper", abstract="Code: https://github.com/author/paper-code")
        self.assertEqual(matches[0]["classification"], "official")

    def test_bibliography_repository_is_rejected_without_authority_evidence(self):
        enricher = GitHubCodeEnricher(token="test")
        item = {
            "full_name": "community/paper-list",
            "description": "A collection of works and survey",
            "owner": {"login": "community"},
        }
        enricher._readme = Mock(return_value="Paper title DOI 10.1/example")
        result = enricher._verify(item, "Paper title", [], None, "10.1/example")
        self.assertEqual(result["classification"], "rejected")
        self.assertEqual(result["confidence"], 0)

    def test_papers_collection_repository_is_rejected(self):
        enricher = GitHubCodeEnricher(token="test")
        item = {
            "full_name": "community/Generative-Recommendation-Papers",
            "description": "Reading resources",
            "owner": {"login": "community"},
        }
        enricher._readme = Mock(return_value="Paper title DOI 10.1/example")
        result = enricher._verify(item, "Paper title", [], None, "10.1/example")
        self.assertEqual(result["classification"], "rejected")

    def test_library_deduplicates_index_and_writes_graph(self):
        with tempfile.TemporaryDirectory() as tmp:
            paper = PaperMetadata(
                paper_id="arxiv:1",
                source="arxiv",
                title="A Recommender Paper",
                authors=["A. Author"],
                abstract="Abstract",
                url="https://example.com/paper",
                published_date=datetime(2026, 7, 12),
                openalex_id="W1",
                referenced_works=["W2"],
                related_works=["W3"],
            )
            score = SimpleNamespace(total_score=88.0, is_qualified=True, tldr="Useful")
            rows = {"arxiv": [{"paper_metadata": paper, "score_response": score, "abstract_cn": "摘要"}]}
            library = ResearchLibrary(Path(tmp) / "knowledge")
            library.persist(rows, {})
            library.persist(rows, {})
            self.assertEqual(len(library.index_path.read_text().splitlines()), 1)
            graph = json.loads(library.graph_path.read_text())
            self.assertEqual({edge["type"] for edge in graph["edges"]}, {"cites", "related"})

    def test_library_deduplicates_different_ids_with_identical_titles(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "knowledge"
            library = ResearchLibrary(root)
            published = datetime(2026, 7, 12)
            low = PaperMetadata(
                paper_id="doi:version-1", source="openalex", title="Same Paper Title",
                authors=[], abstract="abstract", published_date=published, url="https://one"
            )
            high = PaperMetadata(
                paper_id="doi:version-2", source="openalex", title="Same Paper Title",
                authors=[], abstract="abstract", published_date=published, url="https://two"
            )
            low_score = SimpleNamespace(total_score=30, is_qualified=False, tldr="low")
            high_score = SimpleNamespace(total_score=80, is_qualified=True, tldr="high")
            rows = {"openalex": [
                {"paper_metadata": low, "score_response": low_score},
                {"paper_metadata": high, "score_response": high_score},
            ]}
            library.persist(rows, {})
            saved = [json.loads(line) for line in library.index_path.read_text().splitlines()]
            self.assertEqual(len(saved), 1)
            self.assertEqual(saved[0]["paper_id"], "doi:version-2")
            self.assertFalse((library.papers_dir / "doi-version-1.md").exists())

    def test_citation_discovery_is_bounded_and_records_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            index = Path(tmp) / "index.jsonl"
            seed = {
                "paper_id": "seed", "title": "Seed", "score": 90, "qualified": True,
                "openalex_id": "W1", "related_works": ["W2"], "referenced_works": []
            }
            index.write_text(json.dumps(seed) + "\n")
            candidate = PaperMetadata(
                paper_id="candidate", source="citation", title="Candidate", authors=[], abstract="",
                published_date=datetime(2026, 7, 12), url="https://openalex.org/W2", openalex_id="W2"
            )
            openalex = Mock()
            openalex.lookup_by_ids.side_effect = lambda ids: {"W2": candidate} if ids else {}
            openalex.find_recent_citing.return_value = []
            openalex.is_processed.return_value = False
            result = CitationDiscovery(openalex, index).discover(set(), max_total=1)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0].discovery["relation"], "related_to_seed")

    def test_citation_discovery_rejects_old_papers_and_seed_references(self):
        with tempfile.TemporaryDirectory() as tmp:
            index = Path(tmp) / "index.jsonl"
            seed = {
                "paper_id": "seed", "title": "Seed", "score": 90, "qualified": True,
                "openalex_id": "W1", "related_works": ["W2"], "referenced_works": ["W3"]
            }
            index.write_text(json.dumps(seed) + "\n")
            old = PaperMetadata(
                paper_id="old", source="citation", title="Old", authors=[], abstract="",
                published_date=datetime(2010, 1, 1), url="https://openalex.org/W2", openalex_id="W2"
            )
            reference = PaperMetadata(
                paper_id="reference", source="citation", title="Reference", authors=[], abstract="",
                published_date=datetime.now(), url="https://openalex.org/W3", openalex_id="W3"
            )
            openalex = Mock()
            openalex.lookup_by_ids.side_effect = lambda ids: {
                key: value for key, value in {"W2": old, "W3": reference}.items() if key in ids
            }
            openalex.find_recent_citing.return_value = []
            openalex.is_processed.return_value = False

            result = CitationDiscovery(
                openalex, index, max_age_days=90, include_seed_references=False
            ).discover(set())

            self.assertEqual(result, [])

    def test_pdf_access_rejects_doi_landing_page(self):
        paper = PaperMetadata(
            paper_id="doi", source="citation", title="Paper", authors=[], abstract="",
            published_date=datetime.now(), url="https://doi.org/10.1/test",
            pdf_url="https://doi.org/10.3386/w1234",
        )
        self.assertFalse(paper.has_pdf_access())

    def test_weekly_evidence_audit_requires_two_papers_for_observation(self):
        with tempfile.TemporaryDirectory() as tmp:
            records = [
                {"paper_id": "p1", "title": "One", "url": "u1", "tldr": "one", "qualified": True},
                {"paper_id": "p2", "title": "Two", "url": "u2", "tldr": "two", "qualified": True},
            ]
            pack = build_evidence_pack(records, Path(tmp))
            valid, errors = audit_weekly_digest("[跨论文观察] 趋势。[P01-C01][P02-C01]", pack)
            self.assertTrue(valid, errors)
            valid, _ = audit_weekly_digest("[跨论文观察] 趋势。[P01-C01]", pack)
            self.assertFalse(valid)


if __name__ == "__main__":
    unittest.main()
