from fastapi.testclient import TestClient

from app.main import app
from app.services.llm.ollama_client import OllamaConnectionError


def test_health_endpoint_returns_ok() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_llm_health_returns_controlled_unavailable_response(monkeypatch) -> None:
    def fake_check_availability(self) -> None:
        raise OllamaConnectionError("Could not reach Ollama at http://localhost:11434")

    monkeypatch.setattr(
        "app.routes.health.OllamaClient.check_availability",
        fake_check_availability,
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

