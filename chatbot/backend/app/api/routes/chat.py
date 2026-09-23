from fastapi import APIRouter, HTTPException, Depends
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat import ChatService

router = APIRouter()

_chat_service: ChatService | None = None


def get_chat_service() -> ChatService:
    """Retorna instância singleton do ChatService.
    
    Cria a instância na primeira chamada e reutiliza nas subsequentes.
    """
    global _chat_service
    if _chat_service is None:
        _chat_service = ChatService()
    return _chat_service


def override_chat_service(service: ChatService) -> None:
    """Substitui a instância do ChatService (útil para testes)."""
    global _chat_service
    _chat_service = service


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, service: ChatService = Depends(get_chat_service)) -> ChatResponse:
    """Processa mensagem do usuário e retorna resposta da IA.
    
    Args:
        request: Contém a mensagem do usuário e session_id opcional.
        service: Instância do ChatService injetada via dependência.
    
    Returns:
        ChatResponse com a resposta gerada pela IA.
    
    Raises:
        HTTPException: 422 se mensagem estiver vazia.
    """
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=422, detail="Message cannot be empty")

    response = service.process_message(request.message, request.session_id)
    return ChatResponse(response=response)