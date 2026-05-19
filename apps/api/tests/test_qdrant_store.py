from types import SimpleNamespace
from uuid import NAMESPACE_URL, uuid5

from app.schemas.source import EmbeddedChunk
from app.services.vector.qdrant_store import QdrantStore


def test_qdrant_store_upsert_uses_uuid_point_ids_and_preserves_chunk_id() -> None:
    captured: dict[str, object] = {}

    class FakeClient:
        def upsert(self, collection_name: str, points: list, wait: bool) -> None:
            captured["collection_name"] = collection_name
            captured["points"] = points
            captured["wait"] = wait

    store = QdrantStore(url="http://localhost:6333", collection_name="scriptura_sources")
    store.client = FakeClient()

    chunk = EmbeddedChunk(
        id="john-1-note::chunk-0",
        source_id="john-1-note",
        text="João 1 apresenta o Logos como preexistente.",
        title="João 1 - Nota de estudo",
        type="study_note",
        language="pt-BR",
        license="project-created",
        status="approved",
        use_in_rag=True,
        reference="John 1",
        metadata={"lemma": "logos"},
        vector=[0.1, 0.2, 0.3],
    )

    store.upsert_chunks([chunk])

    point = captured["points"][0]
    assert captured["collection_name"] == "scriptura_sources"
    assert captured["wait"] is True
    assert point.id == str(uuid5(NAMESPACE_URL, "john-1-note::chunk-0"))
    assert point.payload["chunk_id"] == "john-1-note::chunk-0"
    assert point.payload["lemma"] == "logos"


def test_qdrant_store_search_uses_query_points_and_maps_chunk_id() -> None:
    class FakeClient:
        def collection_exists(self, collection_name: str) -> bool:
            return True

        def query_points(self, **kwargs):
            return SimpleNamespace(
                points=[
                    SimpleNamespace(
                        id="b77c2ec4-e505-5995-a8ab-0cd422f86a7b",
                        score=0.87,
                        payload={
                            "chunk_id": "john-1-note::chunk-0",
                            "text": "João 1 conecta o Logos ao princípio.",
                            "source_id": "john-1-note",
                            "title": "João 1 - Nota de estudo",
                            "type": "study_note",
                            "language": "pt-BR",
                            "license": "project-created",
                            "reference": "John 1",
                            "status": "approved",
                            "use_in_rag": True,
                        },
                    )
                ]
            )

    store = QdrantStore(url="http://localhost:6333", collection_name="scriptura_sources")
    store.client = FakeClient()

    results = store.search(query_vector=[0.1, 0.2, 0.3], languages=["pt-BR"])

    assert len(results) == 1
    assert results[0].id == "john-1-note::chunk-0"
    assert results[0].source_id == "john-1-note"
    assert results[0].score == 0.87
