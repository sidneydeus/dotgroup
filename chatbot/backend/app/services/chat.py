from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langsmith import traceable
from app.core.config import get_settings, Settings
from app.core.langsmith import init_langsmith

SYSTEM_PROMPT = """Você é um assistente especializado em programação Python.

Suas responsabilidades:
- Responder em português
- Explicar conceitos de forma didática
- Fornecer exemplos de código quando apropriado
- Explicar o código apresentado
- Não responder assuntos que não estejam relacionados à programação com Python

Se a pergunta não for sobre Python, responda educadamente que só pode ajudar com programação Python."""


class ChatService:
    def __init__(self, settings: Settings | None = None):
        self._llm = None
        self._settings = settings or get_settings()
        init_langsmith()

    def _get_llm(self):
        if self._llm is None:
            if not self._settings.groq_api_key:
                raise ValueError("GROQ_API_KEY não configurada")
            self._llm = ChatGroq(
                api_key=self._settings.groq_api_key,
                model=self._settings.groq_model,
                temperature=0.1,
            )
        return self._llm

    @traceable(name="chat_service", run_type="chain")
    def process_message(self, message: str, session_id: str | None = None) -> str:
        llm = self._get_llm()
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=message),
        ]

        config = {}
        if session_id:
            config["metadata"] = {"session_id": session_id}

        response = llm.invoke(messages, config=config)
        return response.content