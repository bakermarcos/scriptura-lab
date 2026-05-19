from fastapi.testclient import TestClient

from app.main import app
from app.services.models.base import ModelProviderError


class UnavailableAdapter:
    provider = "ollama"
    model = "qwen2.5:7b"

    def check_availability(self) -> None:
        raise ModelProviderError("Could not reach Ollama at http://localhost:11434")


def test_health_endpoint_returns_ok() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_llm_health_returns_controlled_unavailable_response(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.routes.health.build_generation_adapter",
        lambda settings: UnavailableAdapter(),
    )

    client = TestClient(app)
    response = client.get("/health/llm")

    assert response.status_code == 200
    assert response.json() == {
        "provider": "ollama",
        "model": "qwen2.5:7b",
        "status": "unavailable",
        "error": "Could not reach Ollama at http://localhost:11434",
    }


def test_embeddings_health_returns_controlled_unavailable_response(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.routes.health.build_embedding_adapter",
        lambda settings: UnavailableAdapter(),
    )

    client = TestClient(app)
    response = client.get("/health/embeddings")

    assert response.status_code == 200
    assert response.json() == {
        "provider": "ollama",
        "model": "qwen2.5:7b",
        "status": "unavailable",
        "error": "Could not reach Ollama at http://localhost:11434",
    }
