from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import Mock
from types import SimpleNamespace

from src.sources.base_source import PaperMetadata
from src.sources.openalex_source import OpenAlexSource
from src.sources.dblp_source import DblpSource
from src.sources.search_agent import SearchAgent
from src.sources.semantic_scholar_enricher import SemanticScholarEnricher


class OpenAlexMetadataTests(TestCase):
    def test_resolves_missing_pdf_by_exact_arxiv_title(self):
        result = SimpleNamespace(
            title="A Sequential Recommendation Method",
            doi="10.1145/example",
            authors=[SimpleNamespace(name="Ada Example")],
            summary="Full abstract",
            published=datetime.now(timezone.utc),
            entry_id="https://arxiv.org/abs/2607.12345v2",
            pdf_url="https://arxiv.org/pdf/2607.12345v2",
            categories=["cs.IR"],
            get_short_id=lambda: "2607.12345v2",
        )
        with TemporaryDirectory() as directory:
            from src.sources.arxiv_source import ArxivSource
            source = ArxivSource(history_dir=Path(directory))
            source.client.results = Mock(return_value=[result])
            paper = source.find_by_title(
                "A Sequential Recommendation Method", ["Ada Example"], "10.1145/example"
            )
        self.assertEqual(paper.arxiv_id, "2607.12345")
        self.assertEqual(paper.pdf_url, "https://arxiv.org/pdf/2607.12345v2")

    def test_maps_conference_metadata(self):
        item = {
            "id": "https://openalex.org/W123",
            "doi": "https://doi.org/10.1145/example",
            "title": "A Sequential Recommendation Method",
            "publication_date": "2026-07-10",
            "authorships": [{"author": {"display_name": "Ada Example"}}],
            "abstract_inverted_index": {"Recommendation": [0], "method": [1]},
            "primary_location": {
                "landing_page_url": "https://doi.org/10.1145/example",
                "source": None,
                "raw_source_name": "Proceedings of ACM SIGIR",
                "raw_type": "proceedings-article",
            },
            "locations": [],
            "best_oa_location": None,
            "open_access": {"is_oa": False},
            "cited_by_count": 3,
            "type": "article",
            "topics": [{"display_name": "Recommender Systems"}],
        }

        with TemporaryDirectory() as directory:
            source = OpenAlexSource(history_dir=Path(directory))
            paper = source._metadata_from_item(item, source="openalex")

        self.assertIsNotNone(paper)
        self.assertEqual(paper.journal, "Proceedings of ACM SIGIR")
        self.assertEqual(paper.publication_type, "proceedings-article")
        self.assertEqual(paper.cited_by_count, 3)
        self.assertEqual(paper.abstract, "Recommendation method")

    def test_merges_openalex_record_into_arxiv_record(self):
        arxiv = PaperMetadata(
            paper_id="2607.12345",
            title="A Sequential Recommendation Method",
            authors=["Ada Example"],
            abstract="Abstract",
            published_date=datetime.now(timezone.utc),
            url="https://arxiv.org/abs/2607.12345",
            source="arxiv",
            pdf_url="https://arxiv.org/pdf/2607.12345.pdf",
        )
        openalex = PaperMetadata(
            paper_id="https://doi.org/10.1145/example",
            title="A Sequential Recommendation Method",
            authors=["Ada Example"],
            abstract="Abstract",
            published_date=datetime.now(timezone.utc),
            url="https://doi.org/10.1145/example",
            source="openalex",
            doi="https://doi.org/10.1145/example",
            journal="Proceedings of ACM SIGIR",
            openalex_id="W123",
            cited_by_count=3,
        )

        agent = SearchAgent.__new__(SearchAgent)
        results = agent._deduplicate_across_sources(
            {"arxiv": [arxiv], "openalex": [openalex]}
        )

        self.assertEqual(results["openalex"], [])
        self.assertEqual(arxiv.doi, "https://doi.org/10.1145/example")
        self.assertEqual(arxiv.journal, "Proceedings of ACM SIGIR")
        self.assertEqual(arxiv.openalex_id, "W123")
        self.assertEqual(arxiv.cited_by_count, 3)

    def test_merges_dblp_record_into_existing_openalex_record(self):
        openalex = PaperMetadata(
            paper_id="https://doi.org/10.1145/example",
            title="A Sequential Recommendation Method",
            authors=["Ada Example"],
            abstract="Abstract",
            published_date=datetime.now(timezone.utc),
            url="https://doi.org/10.1145/example",
            source="openalex",
            doi="https://doi.org/10.1145/example",
        )
        dblp = PaperMetadata(
            paper_id="https://doi.org/10.1145/example",
            title="A Sequential Recommendation Method",
            authors=["Ada Example"],
            abstract="",
            published_date=datetime.now(timezone.utc),
            url="https://dblp.org/rec/conf/wsdm/Example26",
            source="wsdm",
            doi="https://doi.org/10.1145/example",
            journal="WSDM",
        )
        dblp_source = Mock()
        agent = SearchAgent.__new__(SearchAgent)
        agent.dblp_venues = ["wsdm"]
        agent.sources = {"dblp": dblp_source}

        results = agent._deduplicate_across_sources(
            {"arxiv": [], "openalex": [openalex], "wsdm": [dblp]}
        )

        self.assertEqual(results["wsdm"], [])
        self.assertEqual(openalex.journal, "WSDM")
        dblp_source.mark_as_processed.assert_called_once_with(dblp.paper_id)


class SemanticScholarBatchTests(TestCase):
    def test_maps_batch_response_by_doi(self):
        enricher = SemanticScholarEnricher()
        response = Mock()
        response.status_code = 200
        response.json.return_value = [
            {
                "paperId": "s2-paper",
                "url": "https://www.semanticscholar.org/paper/s2-paper",
                "venue": "SIGIR",
                "abstract": "A complete abstract.",
                "tldr": {"text": "A concise summary."},
                "citationCount": 9,
                "influentialCitationCount": 2,
                "publicationTypes": ["Conference"],
                "externalIds": {"ArXiv": "2607.12345"},
                "openAccessPdf": {"url": "https://example.test/paper.pdf"},
            }
        ]
        response.raise_for_status.return_value = None
        enricher.session.post = Mock(return_value=response)

        result = enricher.get_papers_info_batch(["https://doi.org/10.1145/example"])

        paper = result["10.1145/example"]
        self.assertEqual(paper["paper_id"], "s2-paper")
        self.assertEqual(paper["influential_citation_count"], 2)
        self.assertEqual(paper["arxiv_id"], "2607.12345")
        self.assertEqual(paper["pdf_url"], "https://example.test/paper.pdf")
        self.assertEqual(paper["abstract"], "A complete abstract.")


class DblpConferenceTests(TestCase):
    def test_filters_and_maps_recommender_paper(self):
        payload = {
            "result": {
                "hits": {
                    "hit": [
                        {
                            "info": {
                                "authors": {"author": [{"text": "Ada Example"}]},
                                "title": "A Generative Recommendation Model.",
                                "year": "2026",
                                "venue": "WSDM",
                                "doi": "10.1145/example",
                                "key": "conf/wsdm/Example26",
                                "url": "https://dblp.org/rec/conf/wsdm/Example26",
                            }
                        },
                        {
                            "info": {
                                "title": "Unrelated Graph Mining Paper.",
                                "year": "2026",
                                "venue": "WSDM",
                                "key": "conf/wsdm/Other26",
                            }
                        },
                    ]
                }
            }
        }
        with TemporaryDirectory() as directory:
            source = DblpSource(
                history_dir=Path(directory),
                venues=["wsdm"],
                title_terms=["recommend"],
            )
            source._request = Mock(return_value=payload)
            papers = source.fetch_papers(days=3)

        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0].source, "wsdm")
        self.assertEqual(papers[0].doi, "https://doi.org/10.1145/example")
        self.assertEqual(papers[0].authors, ["Ada Example"])
