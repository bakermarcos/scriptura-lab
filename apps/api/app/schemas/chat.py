from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "ok"


class LlmHealthResponse(BaseModel):
    provider: str = "ollama"
    model: str
    status: str
    error: str | None = None


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=3)
    response_language: str | None = None
    source_languages: list[str] | None = None


class ChatSource(BaseModel):
    id: str
    source_id: str
    title: str
    type: str
    language: str
    reference: str | None = None
    excerpt: str
    score: float | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[ChatSource]

