import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock

from src.embeddings import load_model, generate_embeddings, generate_query_embedding, MODEL_NAME


class TestEmbeddings:
    @patch("src.embeddings.cohere.ClientV2")
    def test_load_model_success(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        with patch.dict("os.environ", {"COHERE_API_KEY": "test-key"}):
            client = load_model()

        assert client == mock_client
        mock_client_class.assert_called_once_with(api_key="test-key")

    def test_load_model_missing_key(self):
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="COHERE_API_KEY não configurada"):
                load_model()

    @patch("src.embeddings.cohere.ClientV2")
    def test_generate_embeddings(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        mock_response = Mock()
        mock_response.embeddings.float = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        mock_client.embed.return_value = mock_response

        documents = [
            {"source": "doc1.txt", "text": "texto 1"},
            {"source": "doc2.txt", "text": "texto 2"},
        ]

        client = load_model()
        embeddings = generate_embeddings(documents, client)

        assert isinstance(embeddings, np.ndarray)
        assert embeddings.shape == (2, 3)
        assert embeddings.dtype == np.float32
        mock_client.embed.assert_called_once_with(
            model=MODEL_NAME,
            texts=["texto 1", "texto 2"],
            input_type="search_document",
            embedding_types=["float"]
        )

    @patch("src.embeddings.cohere.ClientV2")
    def test_generate_query_embedding(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        mock_response = Mock()
        mock_response.embeddings.float = [[0.1, 0.2, 0.3]]
        mock_client.embed.return_value = mock_response

        client = load_model()
        embedding = generate_query_embedding("query teste", client)

        assert isinstance(embedding, np.ndarray)
        assert embedding.shape == (1, 3)
        assert embedding.dtype == np.float32
        mock_client.embed.assert_called_once_with(
            model=MODEL_NAME,
            texts=["query teste"],
            input_type="search_query",
            embedding_types=["float"]
        )

    @patch("src.embeddings.cohere.ClientV2")
    def test_embeddings_return_float32(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        mock_response = Mock()
        mock_response.embeddings.float = [[1.0, 2.0, 3.0]]
        mock_client.embed.return_value = mock_response

        client = load_model()
        emb_docs = generate_embeddings([{"text": "test"}], client)
        emb_query = generate_query_embedding("test", client)

        assert emb_docs.dtype == np.float32
        assert emb_query.dtype == np.float32