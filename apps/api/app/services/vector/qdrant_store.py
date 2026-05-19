from uuid import NAMESPACE_URL, uuid5

from qdrant_client import QdrantClient, models

from app.schemas.source import EmbeddedChunk, RetrievedChunk, SourceSummary


class QdrantStore:
    def __init__(self, url: str, collection_name: str) -> None:
        self.client = QdrantClient(url=url, timeout=10.0)
        self.collection_name = collection_name

    def ensure_collection(self, vector_size: int) -> None:
        try:
            if self.client.collection_exists(self.collection_name):
                return
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE,
                ),
            )
        except Exception as exc:  # pragma: no cover - network/runtime dependent
            raise RuntimeError(f"Failed to initialize Qdrant collection: {exc}") from exc

    def upsert_chunks(self, chunks: list[EmbeddedChunk]) -> None:
        if not chunks:
            return

        points = [
            models.PointStruct(
                id=str(uuid5(NAMESPACE_URL, chunk.id)),
                vector=chunk.vector,
                payload={
                    "chunk_id": chunk.id,
                    "text": chunk.text,
                    "source_id": chunk.source_id,
                    "title": chunk.title,
                    "type": chunk.type,
                    "language": chunk.language,
                    "license": chunk.license,
                    "reference": chunk.reference,
                    "status": chunk.status,
                    "use_in_rag": chunk.use_in_rag,
                    **chunk.metadata,
                },
            )
            for chunk in chunks
        ]

        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
                wait=True,
            )
        except Exception as exc:  # pragma: no cover - network/runtime dependent
            raise RuntimeError(f"Failed to upsert chunks into Qdrant: {exc}") from exc

    def search(
        self,
        query_vector: list[float],
        limit: int = 6,
        languages: list[str] | None = None,
    ) -> list[RetrievedChunk]:
        try:
            if not self.client.collection_exists(self.collection_name):
                return []

            response = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=limit,
                query_filter=self._build_filter(languages),
                with_payload=True,
            )
            results = response.points
        except Exception as exc:  # pragma: no cover - network/runtime dependent
            raise RuntimeError(f"Failed to query Qdrant: {exc}") from exc

        chunks: list[RetrievedChunk] = []
        for result in results:
            payload = result.payload or {}
            chunks.append(
                RetrievedChunk(
                    id=str(payload.get("chunk_id", result.id)),
                    source_id=str(payload.get("source_id", "")),
                    text=str(payload.get("text", "")),
                    title=str(payload.get("title", "")),
                    type=str(payload.get("type", "")),
                    language=str(payload.get("language", "")),
                    license=str(payload.get("license", "")),
                    reference=payload.get("reference"),
                    status=str(payload.get("status", "")),
                    use_in_rag=bool(payload.get("use_in_rag", False)),
                    score=float(result.score),
                )
            )
        return chunks

    def list_sources(self, limit: int = 100) -> list[SourceSummary]:
        try:
            if not self.client.collection_exists(self.collection_name):
                return []

            points, _ = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=self._build_filter(None),
                with_payload=True,
                limit=limit,
            )
        except Exception as exc:  # pragma: no cover - network/runtime dependent
            raise RuntimeError(f"Failed to list sources from Qdrant: {exc}") from exc

        source_map: dict[str, SourceSummary] = {}
        for point in points:
            payload = point.payload or {}
            source_id = str(payload.get("source_id", ""))
            if not source_id or source_id in source_map:
                continue

            source_map[source_id] = SourceSummary(
                id=source_id,
                title=str(payload.get("title", "")),
                type=str(payload.get("type", "")),
                language=str(payload.get("language", "")),
                license=str(payload.get("license", "")),
                reference=payload.get("reference"),
            )

        return sorted(source_map.values(), key=lambda item: item.title.lower())

    def _build_filter(self, languages: list[str] | None) -> models.Filter:
        must_conditions = [
            models.FieldCondition(
                key="status",
                match=models.MatchValue(value="approved"),
            ),
            models.FieldCondition(
                key="use_in_rag",
                match=models.MatchValue(value=True),
            ),
        ]

        if languages:
            must_conditions.append(
                models.FieldCondition(
                    key="language",
                    match=models.MatchAny(any=languages),
                )
            )

        return models.Filter(must=must_conditions)
