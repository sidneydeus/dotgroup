import pytest
from pathlib import Path
import tempfile
import os

from src.load_documents import load_documents


class TestLoadDocuments:
    def test_loads_all_documents(self):
        docs = load_documents("data/documents")
        assert len(docs) == 5

    def test_document_structure(self):
        docs = load_documents("data/documents")
        for doc in docs:
            assert "source" in doc
            assert "text" in doc
            assert isinstance(doc["source"], str)
            assert isinstance(doc["text"], str)

    def test_source_names_correct(self):
        docs = load_documents("data/documents")
        sources = {doc["source"] for doc in docs}
        expected = {
            "python.txt",
            "databases.txt",
            "docker.txt",
            "artificial_intelligence.txt",
            "web_development.txt",
        }
        assert sources == expected

    def test_content_not_empty(self):
        docs = load_documents("data/documents")
        for doc in docs:
            assert len(doc["text"]) > 0
            assert doc["text"].strip() != ""

    def test_content_matches_expected_topics(self):
        docs = load_documents("data/documents")
        content_by_source = {doc["source"]: doc["text"].lower() for doc in docs}

        assert "python" in content_by_source["python.txt"]
        assert "banco de dados" in content_by_source["databases.txt"] or "sql" in content_by_source["databases.txt"]
        assert "container" in content_by_source["docker.txt"] or "docker" in content_by_source["docker.txt"]
        assert "inteligência artificial" in content_by_source["artificial_intelligence.txt"] or "ia" in content_by_source["artificial_intelligence.txt"]
        assert "web" in content_by_source["web_development.txt"] or "frontend" in content_by_source["web_development.txt"]

    def test_handles_missing_directory(self):
        docs = load_documents("nonexistent/path")
        assert docs == []

    def test_ignores_non_txt_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "test.txt").write_text("content", encoding="utf-8")
            Path(tmpdir, "test.md").write_text("markdown", encoding="utf-8")
            Path(tmpdir, "test.py").write_text("code", encoding="utf-8")

            docs = load_documents(tmpdir)
            assert len(docs) == 1
            assert docs[0]["source"] == "test.txt"

    def test_utf8_encoding(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "unicode.txt").write_text("café 🚀 português", encoding="utf-8")

            docs = load_documents(tmpdir)
            assert len(docs) == 1
            assert docs[0]["text"] == "café 🚀 português"