from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[4]


class Settings(BaseSettings):
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    WEB_API_BASE_URL: str = "http://localhost:8000"

    LLM_PROVIDER: str = "ollama"
    EMBEDDING_PROVIDER: str = "ollama"

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    LLM_MODEL: str = "qwen2.5:7b"
    EMBEDDING_MODEL: str = "bge-m3"

    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_API_KEY: str = ""

    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "scriptura_sources"

    DEFAULT_RESPONSE_LANGUAGE: str = "pt-BR"
    DEFAULT_SOURCE_LANGUAGES: str = "pt-BR,en"

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def default_source_languages(self) -> list[str]:
        return [
            language.strip()
            for language in self.DEFAULT_SOURCE_LANGUAGES.split(",")
            if language.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
