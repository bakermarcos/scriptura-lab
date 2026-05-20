from fastapi import APIRouter, HTTPException

from app.core.config import get_settings
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.models.base import ModelProviderError
from app.services.models.factory import build_embedding_adapter, build_generation_adapter
from app.services.rag.answer_service import AnswerService
from app.services.rag.prompt_builder import PromptBuilder
from app.services.rag.retriever import Retriever
from app.services.vector.qdrant_store import QdrantStore

router = APIRouter(prefix="/chat", tags=["chat"])


def build_answer_service() -> AnswerService:
    settings = get_settings()
    store = QdrantStore(
        url=settings.QDRANT_URL,
        collection_name=settings.QDRANT_COLLECTION,
    )
    embeddings = build_embedding_adapter(settings)
    retriever = Retriever(
        embedding_service=embeddings,
        store=store,
    )
    llm_client = build_generation_adapter(settings)
    return AnswerService(
        retriever=retriever,
        prompt_builder=PromptBuilder(),
        llm_client=llm_client,
        default_response_language=settings.DEFAULT_RESPONSE_LANGUAGE,
        default_source_languages=settings.default_source_languages,
    )


@router.post("", response_model=ChatResponse)
def post_chat(request: ChatRequest) -> ChatResponse:
    try:
        return build_answer_service().answer_question(
            question=request.question,
            response_language=request.response_language,
            source_languages=request.source_languages,
        )
    except ModelProviderError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
