from fastapi import APIRouter, HTTPException

from app.core.config import get_settings
from app.schemas.source import SourcesResponse
from app.services.vector.qdrant_store import QdrantStore

router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("", response_model=SourcesResponse)
def get_sources() -> SourcesResponse:
    settings = get_settings()
    store = QdrantStore(
        url=settings.QDRANT_URL,
        collection_name=settings.QDRANT_COLLECTION,
    )

    try:
        sources = store.list_sources()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return SourcesResponse(sources=sources)

