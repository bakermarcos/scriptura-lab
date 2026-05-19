import httpx

from app.services.models.base import ModelProviderError


class OllamaConnectionError(ModelProviderError):
    """Raised when Ollama cannot be reached or returns an invalid payload."""


class OllamaClient:
    provider = "ollama"

    def __init__(self, base_url: str, model: str, timeout_seconds: float = 60.0) -> None:
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

    def generate(self, prompt: str) -> str:
        try:
            response = httpx.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise OllamaConnectionError(
                f"Could not reach Ollama at {self.base_url}"
            ) from exc

        payload = response.json()
        answer = str(payload.get("response", "")).strip()
        if not answer:
            raise OllamaConnectionError("Ollama returned an empty response.")
        return answer
