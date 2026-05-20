import httpx

from app.services.models.base import ModelProviderError


class OpenAIProviderError(ModelProviderError):
    """Raised when OpenAI cannot be reached or returns an invalid payload."""


class OpenAIBaseAdapter:
    provider = "openai"

    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        timeout_seconds: float,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key.strip()
        self.model = model
        self.timeout = httpx.Timeout(timeout_seconds, connect=5.0)

    def check_availability(self) -> None:
        try:
            response = httpx.get(
                f"{self.base_url}/models/{self.model}",
                headers=self._headers(),
                timeout=httpx.Timeout(10.0, connect=3.0),
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise OpenAIProviderError(
                f"Could not reach OpenAI API at {self.base_url}"
            ) from exc

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            raise OpenAIProviderError("OPENAI_API_KEY is not configured.")
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }


class OpenAIResponsesClient(OpenAIBaseAdapter):
    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        timeout_seconds: float = 60.0,
    ) -> None:
        super().__init__(
            base_url=base_url,
            api_key=api_key,
            model=model,
            timeout_seconds=timeout_seconds,
        )

    def generate(self, prompt: str) -> str:
        try:
            response = httpx.post(
                f"{self.base_url}/responses",
                headers=self._headers(),
                json={
                    "model": self.model,
                    "input": prompt,
                    "store": False,
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise OpenAIProviderError(
                f"Could not reach OpenAI API at {self.base_url}"
            ) from exc

        answer = self._extract_output_text(response.json())
        if not answer:
            raise OpenAIProviderError("OpenAI returned an empty response.")
        return answer

    def _extract_output_text(self, payload: dict) -> str:
        output_text = payload.get("output_text")
        if isinstance(output_text, str):
            return output_text.strip()

        extracted: list[str] = []
        output = payload.get("output")
        if not isinstance(output, list):
            return ""

        for item in output:
            if not isinstance(item, dict):
                continue
            content = item.get("content")
            if not isinstance(content, list):
                continue
            for content_item in content:
                if not isinstance(content_item, dict):
                    continue
                text = content_item.get("text")
                if isinstance(text, str):
                    extracted.append(text)

        return "\n".join(extracted).strip()


class OpenAIEmbeddingService(OpenAIBaseAdapter):
    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        timeout_seconds: float = 30.0,
    ) -> None:
        super().__init__(
            base_url=base_url,
            api_key=api_key,
            model=model,
            timeout_seconds=timeout_seconds,
        )

    def embed(self, text: str) -> list[float]:
        try:
            response = httpx.post(
                f"{self.base_url}/embeddings",
                headers=self._headers(),
                json={
                    "model": self.model,
                    "input": text,
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise OpenAIProviderError(
                f"Could not reach OpenAI API at {self.base_url}"
            ) from exc

        payload = response.json()
        data = payload.get("data")
        if isinstance(data, list) and data and isinstance(data[0], dict):
            embedding = data[0].get("embedding")
            if isinstance(embedding, list):
                return [float(value) for value in embedding]

        raise OpenAIProviderError("OpenAI returned an invalid embedding payload.")
