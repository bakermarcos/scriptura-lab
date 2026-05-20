import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
API_DIR = ROOT_DIR / "apps" / "api"

if str(API_DIR) not in sys.path:
    sys.path.insert(0, str(API_DIR))

from app.core.config import get_settings
from app.services.ingestion.chunker import TextChunker
from app.services.ingestion.ingest_service import IngestService
from app.services.ingestion.markdown_loader import MarkdownLoader
from app.services.models.factory import build_embedding_adapter
from app.services.vector.qdrant_store import QdrantStore


def resolve_source_directory(raw_directory: str) -> Path:
    directory = Path(raw_directory)
    if directory.is_absolute():
        return directory
    return ROOT_DIR / directory


def display_source_directory(directory: Path) -> str:
    try:
        return str(directory.relative_to(ROOT_DIR))
    except ValueError:
        return str(directory)


def main() -> None:
    settings = get_settings()
    ingest_service = IngestService(
        loader=MarkdownLoader(),
        chunker=TextChunker(),
        embedding_service=build_embedding_adapter(settings),
        store=QdrantStore(
            url=settings.QDRANT_URL,
            collection_name=settings.QDRANT_COLLECTION,
        ),
    )

    total_documents = 0
    total_chunks = 0
    total_indexed = 0
    collection_name = settings.QDRANT_COLLECTION

    for raw_directory in settings.ingest_source_dirs:
        source_directory = resolve_source_directory(raw_directory)
        if not source_directory.exists():
            print(f"Skipped missing source directory: {source_directory}")
            continue

        stats = ingest_service.ingest_directory(source_directory)
        total_documents += stats.documents_loaded
        total_chunks += stats.chunks_created
        total_indexed += stats.chunks_indexed
        collection_name = stats.collection_name

        print(f"Source directory: {display_source_directory(source_directory)}")
        print(f"  Loaded documents: {stats.documents_loaded}")
        print(f"  Created chunks: {stats.chunks_created}")
        print(f"  Indexed chunks: {stats.chunks_indexed}")

    print(f"Loaded documents: {total_documents}")
    print(f"Created chunks: {total_chunks}")
    print(f"Indexed chunks: {total_indexed}")
    print(f"Collection: {collection_name}")


if __name__ == "__main__":
    main()
