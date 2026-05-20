from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.chat import HealthResponse, LlmHealthResponse
from app.services.models.base import ModelProviderError
from app.services.models.factory import build_embedding_adapter, build_generation_adapter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/llm", response_model=LlmHealthResponse)
def get_llm_health() -> LlmHealthResponse:
    settings = get_settings()
    try:
        client = build_generation_adapter(settings)
    except ModelProviderError as exc:
        return LlmHealthResponse(
            provider=settings.LLM_PROVIDER,
            model=settings.LLM_MODEL,
            status="unavailable",
            error=str(exc),
        )

    try:
        client.check_availability()
    except ModelProviderError as exc:
        return LlmHealthResponse(
            provider=client.provider,
            model=client.model,
            status="unavailable",
            error=str(exc),
        )

    return LlmHealthResponse(
        provider=client.provider,
        model=client.model,
        status="available",
    )


@router.get("/embeddings", response_model=LlmHealthResponse)
def get_embeddings_health() -> LlmHealthResponse:
    settings = get_settings()
    try:
        client = build_embedding_adapter(settings)
    except ModelProviderError as exc:
        return LlmHealthResponse(
            provider=settings.EMBEDDING_PROVIDER,
            model=settings.EMBEDDING_MODEL,
            status="unavailable",
            error=str(exc),
        )

    try:
        client.check_availability()
    except ModelProviderError as exc:
        return LlmHealthResponse(
            provider=client.provider,
            model=client.model,
            status="unavailable",
            error=str(exc),
        )

    return LlmHealthResponse(
        provider=client.provider,
        model=client.model,
        status="available",
    )
