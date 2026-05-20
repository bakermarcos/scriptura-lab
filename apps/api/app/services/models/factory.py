from app.core.config import Settings
from app.services.embeddings.ollama_embeddings import OllamaEmbeddingService
from app.services.llm.ollama_client import OllamaClient
from app.services.models.base import (
    EmbeddingAdapter,
    TextGenerationAdapter,
    UnsupportedModelProviderError,
)
from app.services.models.openai_adapters import (
    OpenAIEmbeddingService,
    OpenAIResponsesClient,
)


def build_generation_adapter(settings: Settings) -> TextGenerationAdapter:
    provider = _normalize_provider(settings.LLM_PROVIDER)

    if provider == "ollama":
        return OllamaClient(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.LLM_MODEL,
        )

    if provider == "openai":
        return OpenAIResponsesClient(
            base_url=settings.OPENAI_BASE_URL,
            api_key=settings.OPENAI_API_KEY,
            model=settings.LLM_MODEL,
        )

    raise UnsupportedModelProviderError(
        f"Unsupported LLM_PROVIDER '{settings.LLM_PROVIDER}'."
    )


def build_embedding_adapter(settings: Settings) -> EmbeddingAdapter:
    provider = _normalize_provider(settings.EMBEDDING_PROVIDER)

    if provider == "ollama":
        return OllamaEmbeddingService(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.EMBEDDING_MODEL,
        )

    if provider == "openai":
        return OpenAIEmbeddingService(
            base_url=settings.OPENAI_BASE_URL,
            api_key=settings.OPENAI_API_KEY,
            model=settings.EMBEDDING_MODEL,
        )

    raise UnsupportedModelProviderError(
        f"Unsupported EMBEDDING_PROVIDER '{settings.EMBEDDING_PROVIDER}'."
    )


def _normalize_provider(provider: str) -> str:
    return provider.strip().lower()
