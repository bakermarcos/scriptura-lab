from typing import Protocol


class ModelProviderError(RuntimeError):
    """Raised when a configured model provider cannot complete a request."""


class UnsupportedModelProviderError(ModelProviderError):
    """Raised when the configured provider does not have an adapter."""


class TextGenerationAdapter(Protocol):
    provider: str
    model: str

    def check_availability(self) -> None:
        ...

    def generate(self, prompt: str) -> str:
        ...


class EmbeddingAdapter(Protocol):
    provider: str
    model: str

    def check_availability(self) -> None:
        ...

    def embed(self, text: str) -> list[float]:
        ...
