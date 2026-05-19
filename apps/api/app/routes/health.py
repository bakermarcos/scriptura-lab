from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.chat import HealthResponse, LlmHealthResponse
from app.services.llm.ollama_client import OllamaClient, OllamaConnectionError

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/llm", response_model=LlmHealthResponse)
def get_llm_health() -> LlmHealthResponse:
    settings = get_settings()
    client = OllamaClient(
        base_url=settings.OLLAMA_BASE_URL,
        model=settings.LLM_MODEL,
    )

    try:
        client.check_availability()
    except OllamaConnectionError as exc:
        return LlmHealthResponse(
            provider="ollama",
            model=settings.LLM_MODEL,
            status="unavailable",
            error=str(exc),
        )

    return LlmHealthResponse(
        provider="ollama",
        model=settings.LLM_MODEL,
        status="available",
    )

