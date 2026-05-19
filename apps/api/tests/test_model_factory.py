from app.core.config import Settings
from app.services.embeddings.ollama_embeddings import OllamaEmbeddingService
from app.services.llm.ollama_client import OllamaClient
from app.services.models.factory import build_embedding_adapter, build_generation_adapter
from app.services.models.openai_adapters import (
    OpenAIEmbeddingService,
    OpenAIResponsesClient,
)


def test_build_generation_adapter_defaults_to_ollama() -> None:
    adapter = build_generation_adapter(Settings(_env_file=None))

    assert isinstance(adapter, OllamaClient)
    assert adapter.provider == "ollama"
    assert adapter.model == "qwen2.5:7b"


def test_build_embedding_adapter_defaults_to_ollama() -> None:
    adapter = build_embedding_adapter(Settings(_env_file=None))

    assert isinstance(adapter, OllamaEmbeddingService)
    assert adapter.provider == "ollama"
    assert adapter.model == "bge-m3"


def test_build_generation_adapter_supports_openai() -> None:
    settings = Settings(
        _env_file=None,
        LLM_PROVIDER="openai",
        LLM_MODEL="gpt-5.5",
        OPENAI_API_KEY="test-key",
    )

    adapter = build_generation_adapter(settings)

    assert isinstance(adapter, OpenAIResponsesClient)
    assert adapter.provider == "openai"
    assert adapter.model == "gpt-5.5"


def test_build_embedding_adapter_supports_openai() -> None:
    settings = Settings(
        _env_file=None,
        EMBEDDING_PROVIDER="openai",
        EMBEDDING_MODEL="text-embedding-3-small",
        OPENAI_API_KEY="test-key",
    )

    adapter = build_embedding_adapter(settings)

    assert isinstance(adapter, OpenAIEmbeddingService)
    assert adapter.provider == "openai"
    assert adapter.model == "text-embedding-3-small"
