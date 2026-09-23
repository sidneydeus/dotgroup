import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.services.chat import ChatService
from app.core.config import Settings
from app.api.routes.chat import override_chat_service


client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_valid_message():
    mock_llm = Mock()
    mock_llm.invoke.return_value = Mock(content="Resposta mockada da LLM")

    settings = Settings(groq_api_key="test-key", groq_model="test-model")
    service = ChatService(settings=settings)

    with patch("app.services.chat.ChatGroq") as mock_chat_groq:
        mock_chat_groq.return_value = mock_llm
        override_chat_service(service)
        response = client.post("/api/chat", json={"message": "Como criar uma lista em Python?"})
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert isinstance(data["response"], str)
        assert len(data["response"]) > 0

    override_chat_service(None)


def test_chat_missing_message():
    response = client.post("/api/chat", json={})
    assert response.status_code == 422


def test_chat_empty_message():
    response = client.post("/api/chat", json={"message": ""})
    assert response.status_code == 422


def test_chat_whitespace_only():
    response = client.post("/api/chat", json={"message": "   "})
    assert response.status_code == 422


class TestChatService:
    @patch("app.services.chat.ChatGroq")
    def test_process_message_with_mock(self, mock_chat_groq):
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="Resposta mockada da LLM")
        mock_chat_groq.return_value = mock_llm

        settings = Settings(groq_api_key="test-key", groq_model="test-model")
        service = ChatService(settings=settings)
        response = service.process_message("Como criar uma lista?")

        assert response == "Resposta mockada da LLM"
        mock_llm.invoke.assert_called_once()
        call_args = mock_llm.invoke.call_args[0][0]
        assert len(call_args) == 2
        assert call_args[1].content == "Como criar uma lista?"

    @patch("app.services.chat.ChatGroq")
    def test_process_message_python_question(self, mock_chat_groq):
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="Para criar uma lista em Python, use colchetes: minha_lista = [1, 2, 3]")
        mock_chat_groq.return_value = mock_llm

        settings = Settings(groq_api_key="test-key", groq_model="test-model")
        service = ChatService(settings=settings)
        response = service.process_message("Como criar uma lista em Python?")

        assert "lista" in response.lower()
        assert "python" in response.lower()
        mock_llm.invoke.assert_called_once()

    def test_process_message_raises_error_without_api_key(self):
        settings = Settings(groq_api_key="")
        service = ChatService(settings=settings)
        with pytest.raises(ValueError, match="GROQ_API_KEY não configurada"):
            service.process_message("teste")