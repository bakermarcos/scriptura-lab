from app.schemas.source import RetrievedChunk
from app.services.models.base import EmbeddingAdapter
from app.services.vector.qdrant_store import QdrantStore


class Retriever:
    def __init__(
        self,
        embedding_service: EmbeddingAdapter,
        store: QdrantStore,
        limit: int = 6,
    ) -> None:
        self.embedding_service = embedding_service
        self.store = store
        self.limit = limit

    def search(
        self,
        question: str,
        languages: list[str] | None = None,
    ) -> list[RetrievedChunk]:
        query_vector = self.embedding_service.embed(question)
        return self.store.search(
            query_vector=query_vector,
            limit=self.limit,
            languages=languages,
        )
