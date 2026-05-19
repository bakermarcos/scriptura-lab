import httpx

from app.services.llm.ollama_client import OllamaConnectionError


class OllamaEmbeddingService:
    provider = "ollama"

    def __init__(self, base_url: str, model: str, timeout_seconds: float = 30.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = httpx.Timeout(timeout_seconds, connect=5.0)

    def check_availability(self) -> None:
        try:
            response = httpx.get(
                f"{self.base_url}/api/tags",
                timeout=httpx.Timeout(10.0, connect=3.0),
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise OllamaConnectionError(
                f"Could not reach Ollama at {self.base_url}"
            ) from exc

    def embed(self, text: str) -> list[float]:
        try:
            response = httpx.post(
                f"{self.base_url}/api/embed",
                json={
                    "model": self.model,
                    "input": text,
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise OllamaConnectionError(
                f"Could not reach Ollama at {self.base_url}"
            ) from exc

        payload = response.json()
        embeddings = payload.get("embeddings")
        if isinstance(embeddings, list) and embeddings and isinstance(embeddings[0], list):
            return [float(value) for value in embeddings[0]]

        embedding = payload.get("embedding")
        if isinstance(embedding, list):
            return [float(value) for value in embedding]

        raise OllamaConnectionError("Ollama returned an invalid embedding payload.")
