import pytest
import numpy as np
import faiss
import json
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.ingest import ingest
from src.vector_store import INDEX_PATH, DOCUMENTS_PATH
import src.vector_store as vs


class TestIngest:
    @patch("src.ingest.load_documents")
    @patch("src.ingest.load_model")
    @patch("src.ingest.generate_embeddings")
    @patch("src.ingest.create_index")
    @patch("src.ingest.save_index")
    @patch("src.ingest.save_documents")
    def test_ingest_calls_all_steps(self, mock_save_docs, mock_save_idx, mock_create_idx,
                                     mock_gen_emb, mock_load_model, mock_load_docs):
        mock_load_docs.return_value = [
            {"source": "doc1.txt", "text": "conteúdo 1"},
            {"source": "doc2.txt", "text": "conteúdo 2"},
        ]
        mock_client = Mock()
        mock_load_model.return_value = mock_client
        mock_gen_emb.return_value = np.array([[0.1, 0.2], [0.3, 0.4]], dtype=np.float32)
        mock_index = Mock()
        mock_index.ntotal = 2
        mock_create_idx.return_value = mock_index

        ingest()

        mock_load_docs.assert_called_once()
        mock_load_model.assert_called_once()
        mock_gen_emb.assert_called_once()
        mock_create_idx.assert_called_once()
        mock_save_idx.assert_called_once()
        mock_save_docs.assert_called_once()

    @patch("src.ingest.load_documents")
    @patch("src.ingest.load_model")
    @patch("src.ingest.generate_embeddings")
    @patch("src.ingest.create_index")
    @patch("src.ingest.save_index")
    @patch("src.ingest.save_documents")
    def test_ingest_saves_correct_files(self, mock_save_docs, mock_save_idx, mock_create_idx,
                                         mock_gen_emb, mock_load_model, mock_load_docs):
        test_docs = [
            {"source": "python.txt", "text": "Python é uma linguagem..."},
            {"source": "docker.txt", "text": "Docker permite containers..."},
        ]
        mock_load_docs.return_value = test_docs
        mock_client = Mock()
        mock_load_model.return_value = mock_client
        mock_gen_emb.return_value = np.array([[0.1, 0.2], [0.3, 0.4]], dtype=np.float32)
        mock_index = Mock()
        mock_index.ntotal = 2
        mock_create_idx.return_value = mock_index

        ingest()

        mock_save_idx.assert_called_once()
        saved_index, saved_path = mock_save_idx.call_args[0]
        assert saved_path == INDEX_PATH
        assert saved_index == mock_index

        mock_save_docs.assert_called_once()
        saved_docs, saved_path = mock_save_docs.call_args[0]
        assert saved_path == DOCUMENTS_PATH
        assert saved_docs == test_docs


class TestIngestIntegration:
    @pytest.fixture
    def temp_storage(self, tmp_path):
        old_index = INDEX_PATH
        old_docs = DOCUMENTS_PATH
        import src.vector_store as vs
        vs.INDEX_PATH = str(tmp_path / "index.faiss")
        vs.DOCUMENTS_PATH = str(tmp_path / "documents.json")
        yield tmp_path
        vs.INDEX_PATH = old_index
        vs.DOCUMENTS_PATH = old_docs

    @patch("src.ingest.load_documents")
    @patch("src.ingest.load_model")
    def test_ingest_creates_files(self, mock_load_model, mock_load_docs, temp_storage):
        test_docs = [
            {"source": "doc1.txt", "text": "conteúdo 1"},
            {"source": "doc2.txt", "text": "conteúdo 2"},
        ]
        mock_load_docs.return_value = test_docs

        mock_client = Mock()
        mock_load_model.return_value = mock_client

        mock_response = Mock()
        mock_response.embeddings.float = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        mock_client.embed.return_value = mock_response

        from src.ingest import ingest
        ingest()

        assert os.path.exists(INDEX_PATH)
        assert os.path.exists(DOCUMENTS_PATH)

        with open(DOCUMENTS_PATH, "r", encoding="utf-8") as f:
            saved_docs = json.load(f)
        assert len(saved_docs) == 2
        assert saved_docs[0]["source"] == "doc1.txt"

        import faiss
        index = faiss.read_index(INDEX_PATH)
        assert index.ntotal == 2
        assert index.d == 3