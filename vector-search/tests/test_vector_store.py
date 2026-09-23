import pytest
import numpy as np
import faiss
import json
import tempfile
import os
from pathlib import Path

from src.vector_store import (
    create_index,
    save_index,
    load_index,
    save_documents,
    load_documents,
    INDEX_PATH,
    DOCUMENTS_PATH,
)


class TestVectorStore:
    def test_create_index(self):
        embeddings = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]], dtype=np.float32)
        index = create_index(embeddings)

        assert isinstance(index, faiss.IndexFlatIP)
        assert index.ntotal == 2
        assert index.d == 3

    def test_create_index_empty(self):
        embeddings = np.array([], dtype=np.float32).reshape(0, 3)
        index = create_index(embeddings)
        assert index.ntotal == 0

    def test_save_and_load_index(self):
        embeddings = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]], dtype=np.float32)
        index = create_index(embeddings)

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test_index.faiss")
            save_index(index, path)
            assert os.path.exists(path)

            loaded = load_index(path)
            assert loaded.ntotal == 2
            assert loaded.d == 3

    def test_save_documents(self):
        documents = [
            {"source": "doc1.txt", "text": "conteúdo 1"},
            {"source": "doc2.txt", "text": "conteúdo 2"},
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "documents.json")
            save_documents(documents, path)

            assert os.path.exists(path)
            with open(path, "r", encoding="utf-8") as f:
                loaded = json.load(f)

            assert len(loaded) == 2
            assert loaded[0]["source"] == "doc1.txt"
            assert loaded[1]["text"] == "conteúdo 2"

    def test_load_documents(self):
        documents = [
            {"source": "doc1.txt", "text": "conteúdo 1"},
            {"source": "doc2.txt", "text": "conteúdo 2"},
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "documents.json")
            save_documents(documents, path)

            loaded = load_documents(path)
            assert len(loaded) == 2
            assert loaded[0]["source"] == "doc1.txt"

    def test_save_documents_creates_directory(self):
        documents = [{"source": "test.txt", "text": "test"}]

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "subdir", "documents.json")
            save_documents(documents, path)
            assert os.path.exists(path)

    def test_save_index_creates_directory(self):
        embeddings = np.array([[0.1, 0.2, 0.3]], dtype=np.float32)
        index = create_index(embeddings)

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "subdir", "index.faiss")
            save_index(index, path)
            assert os.path.exists(path)

    def test_index_search_returns_correct_shape(self):
        embeddings = np.array(
            [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
            dtype=np.float32
        )
        index = create_index(embeddings)

        query = np.array([[1.0, 0.0, 0.0]], dtype=np.float32)
        scores, indices = index.search(query, 2)

        assert scores.shape == (1, 2)
        assert indices.shape == (1, 2)
        assert indices[0][0] == 0