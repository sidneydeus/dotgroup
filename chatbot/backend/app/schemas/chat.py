from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User message")
    session_id: str | None = Field(None, description="Optional session ID for conversation tracking")


class ChatResponse(BaseModel):
    response: str