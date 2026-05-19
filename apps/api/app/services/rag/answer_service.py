from app.schemas.chat import ChatResponse, ChatSource
from app.schemas.source import RetrievedChunk
from app.services.models.base import TextGenerationAdapter
from app.services.rag.prompt_builder import PromptBuilder
from app.services.rag.retriever import Retriever

FALLBACK_ANSWER = (
    "Não encontrei base suficiente nas fontes disponíveis para responder com segurança."
)


class AnswerService:
    def __init__(
        self,
        retriever: Retriever,
        prompt_builder: PromptBuilder,
        llm_client: TextGenerationAdapter,
        default_response_language: str,
        default_source_languages: list[str],
        min_score_threshold: float = 0.35,
    ) -> None:
        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.llm_client = llm_client
        self.default_response_language = default_response_language
        self.default_source_languages = default_source_languages
        self.min_score_threshold = min_score_threshold

    def answer_question(
        self,
        question: str,
        response_language: str | None = None,
        source_languages: list[str] | None = None,
    ) -> ChatResponse:
        chosen_response_language = response_language or self.default_response_language
        chosen_source_languages = source_languages or self.default_source_languages
        retrieved_sources = self.retriever.search(
            question=question,
            languages=chosen_source_languages,
        )

        if not self._has_usable_sources(retrieved_sources):
            return ChatResponse(answer=FALLBACK_ANSWER, sources=[])

        prompt = self.prompt_builder.build(
            question=question,
            sources=retrieved_sources,
            response_language=chosen_response_language,
        )
        answer = self.llm_client.generate(prompt)
        return ChatResponse(
            answer=answer,
            sources=[self._to_chat_source(source) for source in retrieved_sources],
        )

    def _has_usable_sources(self, sources: list[RetrievedChunk]) -> bool:
        if not sources:
            return False
        return max(source.score for source in sources) >= self.min_score_threshold

    def _to_chat_source(self, source: RetrievedChunk) -> ChatSource:
        return ChatSource(
            id=source.id,
            source_id=source.source_id,
            title=source.title,
            type=source.type,
            language=source.language,
            reference=source.reference,
            excerpt=self._build_excerpt(source.text),
            score=round(source.score, 4),
        )

    def _build_excerpt(self, text: str, limit: int = 260) -> str:
        normalized = " ".join(text.split())
        if len(normalized) <= limit:
            return normalized
        return normalized[: limit - 3].rstrip() + "..."
