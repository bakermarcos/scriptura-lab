from dataclasses import dataclass
from pathlib import Path

from app.schemas.source import EmbeddedChunk
from app.services.ingestion.chunker import TextChunker
from app.services.ingestion.markdown_loader import MarkdownLoader
from app.services.models.base import EmbeddingAdapter
from app.services.vector.qdrant_store import QdrantStore


@dataclass
class IngestionStats:
    documents_loaded: int
    chunks_created: int
    chunks_indexed: int
    collection_name: str


class IngestService:
    def __init__(
        self,
        loader: MarkdownLoader,
        chunker: TextChunker,
        embedding_service: EmbeddingAdapter,
        store: QdrantStore,
    ) -> None:
        self.loader = loader
        self.chunker = chunker
        self.embedding_service = embedding_service
        self.store = store

    def ingest_directory(self, directory: Path) -> IngestionStats:
        documents = self.loader.load_directory(directory)
        created_chunks = [
            chunk
            for document in documents
            for chunk in self.chunker.chunk_document(document)
        ]

        embedded_chunks: list[EmbeddedChunk] = []
        vector_size: int | None = None

        for chunk in created_chunks:
            vector = self.embedding_service.embed(chunk.text)
            if vector_size is None:
                vector_size = len(vector)
            embedded_chunks.append(
                EmbeddedChunk(
                    **chunk.model_dump(),
                    vector=vector,
                )
            )

        if vector_size is not None:
            self.store.ensure_collection(vector_size)
            self.store.upsert_chunks(embedded_chunks)

        return IngestionStats(
            documents_loaded=len(documents),
            chunks_created=len(created_chunks),
            chunks_indexed=len(embedded_chunks),
            collection_name=self.store.collection_name,
        )
