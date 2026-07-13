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
from library.feedback import FeedbackStore
from library.research_library import ResearchLibrary
from library.evidence_builder import build_evidence_pack, audit_weekly_digest
from sources.base_source import PaperMetadata
from sources.citation_discovery import CitationDiscovery
from sources.institutional_rss_source import InstitutionalRssSource
from sources.repec_series_source import RepecSeriesSource
from sources.search_agent import SearchAgent
from sources.worldbank_source import WorldBankSource
from sync_feedback import parse_feedback
from notifications.notifier import NotifierAgent, RunResult, WebhookNotifier


class ResearchAutomationTests(unittest.TestCase):
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
        self.assertIn("全文深读\n`OPENALEX` · Score **80.0**", card)
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

    def test_feedback_store_boosts_liked_paper(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "feedback.json"
            path.write_text('{"liked":["p1"],"ignored":[]}', encoding="utf-8")
            score = SimpleNamespace(total_score=70.0, reasoning="base", is_qualified=False)
            FeedbackStore(path).apply("p1", score)
            self.assertEqual(score.total_score, 80.0)
            self.assertTrue(score.is_qualified)

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
