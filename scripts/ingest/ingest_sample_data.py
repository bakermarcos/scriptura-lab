from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
API_DIR = ROOT_DIR / "apps" / "api"

if str(API_DIR) not in sys.path:
    sys.path.insert(0, str(API_DIR))

from app.core.config import get_settings
from app.services.embeddings.ollama_embeddings import OllamaEmbeddingService
from app.services.ingestion.chunker import TextChunker
from app.services.ingestion.ingest_service import IngestService
from app.services.ingestion.markdown_loader import MarkdownLoader
from app.services.vector.qdrant_store import QdrantStore


def main() -> None:
    settings = get_settings()
    ingest_service = IngestService(
        loader=MarkdownLoader(),
        chunker=TextChunker(),
        embedding_service=OllamaEmbeddingService(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.EMBEDDING_MODEL,
        ),
        store=QdrantStore(
            url=settings.QDRANT_URL,
            collection_name=settings.QDRANT_COLLECTION,
        ),
    )

    stats = ingest_service.ingest_directory(ROOT_DIR / "data" / "sample" / "sources")
    print(f"Loaded documents: {stats.documents_loaded}")
    print(f"Created chunks: {stats.chunks_created}")
    print(f"Indexed chunks: {stats.chunks_indexed}")
    print(f"Collection: {stats.collection_name}")


if __name__ == "__main__":
    main()
