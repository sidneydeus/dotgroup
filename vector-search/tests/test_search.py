import pytest
import numpy as np
import faiss
import json
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.search import search, print_results
from src.vector_store import INDEX_PATH, DOCUMENTS_PATH
import src.vector_store as vs
import src.search as ss


class TestSearch:
    @patch("src.search.generate_query_embedding")
    def test_search_returns_correct_structure(self, mock_gen_query):
        mock_client = Mock()
        mock_gen_query.return_value = np.array([[0.1, 0.2, 0.3]], dtype=np.float32)

        embeddings = np.array(
            [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]],
            dtype=np.float32
        )
        index = faiss.IndexFlatIP(3)
        index.add(embeddings)

        documents = [
            {"source": "doc1.txt", "text": "conteúdo 1"},
            {"source": "doc2.txt", "text": "conteúdo 2"},
            {"source": "doc3.txt", "text": "conteúdo 3"},
        ]

        result = search("query teste", index, documents, mock_client, top_k=2)

        assert "query" in result
        assert "results" in result
        assert result["query"] == "query teste"
        assert len(result["results"]) == 2
        for r in result["results"]:
            assert "source" in r
            assert "text" in r
            assert "score" in r
            assert isinstance(r["score"], float)

    @patch("src.search.generate_query_embedding")
    def test_search_respects_top_k(self, mock_gen_query):
        mock_client = Mock()
        mock_gen_query.return_value = np.array([[0.1, 0.2, 0.3]], dtype=np.float32)

        embeddings = np.array(
            [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]],
            dtype=np.float32
        )
        index = faiss.IndexFlatIP(3)
        index.add(embeddings)

        documents = [
            {"source": "doc1.txt", "text": "conteúdo 1"},
            {"source": "doc2.txt", "text": "conteúdo 2"},
            {"source": "doc3.txt", "text": "conteúdo 3"},
        ]

        result = search("query", index, documents, mock_client, top_k=1)
        assert len(result["results"]) == 1

        result = search("query", index, documents, mock_client, top_k=5)
        assert len(result["results"]) == 3

    @patch("src.search.generate_query_embedding")
    def test_search_scores_are_float(self, mock_gen_query):
        mock_client = Mock()
        mock_gen_query.return_value = np.array([[0.1, 0.2, 0.3]], dtype=np.float32)

        embeddings = np.array([[0.1, 0.2, 0.3]], dtype=np.float32)
        index = faiss.IndexFlatIP(3)
        index.add(embeddings)

        documents = [{"source": "doc1.txt", "text": "conteúdo 1"}]

        result = search("query", index, documents, mock_client)
        assert isinstance(result["results"][0]["score"], float)

    @patch("src.search.generate_query_embedding")
    def test_search_returns_highest_score_first(self, mock_gen_query):
        mock_client = Mock()
        mock_gen_query.return_value = np.array([[1.0, 0.0, 0.0]], dtype=np.float32)

        embeddings = np.array(
            [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
            dtype=np.float32
        )
        index = faiss.IndexFlatIP(3)
        index.add(embeddings)

        documents = [
            {"source": "doc1.txt", "text": "conteúdo 1"},
            {"source": "doc2.txt", "text": "conteúdo 2"},
        ]

        result = search("query", index, documents, mock_client, top_k=2)
        assert result["results"][0]["source"] == "doc1.txt"
        assert result["results"][0]["score"] >= result["results"][1]["score"]


class TestSearchIntegration:
    @pytest.fixture
    def temp_setup(self, tmp_path):
        old_index = INDEX_PATH
        old_docs = DOCUMENTS_PATH
        import src.vector_store as vs
        import src.search as ss
        vs.INDEX_PATH = str(tmp_path / "index.faiss")
        vs.DOCUMENTS_PATH = str(tmp_path / "documents.json")
        ss.INDEX_PATH = vs.INDEX_PATH
        ss.DOCUMENTS_PATH = vs.DOCUMENTS_PATH
        yield tmp_path
        vs.INDEX_PATH = old_index
        vs.DOCUMENTS_PATH = old_docs
        ss.INDEX_PATH = old_index
        ss.DOCUMENTS_PATH = old_docs

    @patch("src.search.load_model")
    @patch("src.ingest.load_documents")
    @patch("src.ingest.load_model")
    @patch("src.ingest.generate_embeddings")
    @patch("src.ingest.create_index")
    @patch("src.ingest.save_index")
    @patch("src.ingest.save_documents")
    def test_search_with_persisted_index(self, mock_save_docs, mock_save_idx, mock_create_idx,
                                          mock_gen_emb, mock_ingest_load_model, mock_ingest_load_docs,
                                          mock_search_load_model, temp_setup):
        mock_ingest_load_docs.return_value = [
            {"source": "docker.txt", "text": "Docker permite executar aplicações em containers isolados"},
            {"source": "python.txt", "text": "Python é linguagem popular para IA e machine learning"},
            {"source": "databases.txt", "text": "Bancos de dados relacionais usam SQL e tabelas"},
        ]
        
        mock_client = Mock()
        mock_ingest_load_model.return_value = mock_client
        mock_search_load_model.return_value = mock_client

        mock_response = Mock()
        mock_response.embeddings.float = [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
        mock_client.embed.return_value = mock_response

        mock_index = Mock()
        mock_index.ntotal = 3
        mock_create_idx.return_value = mock_index

        from src.ingest import ingest
        ingest()

        mock_query_response = Mock()
        mock_query_response.embeddings.float = [[1.0, 0.0, 0.0]]
        mock_client.embed.return_value = mock_query_response

        mock_index.search.return_value = (
            np.array([[0.9, 0.1, 0.05]], dtype=np.float32),
            np.array([[0, 1, 2]], dtype=np.int64)
        )

        from src.search import search
        result = search("containers isolados", mock_index, mock_ingest_load_docs.return_value, mock_client, top_k=3)

        assert result["query"] == "containers isolados"
        assert len(result["results"]) == 3