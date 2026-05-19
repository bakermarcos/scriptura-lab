from fastapi import APIRouter, HTTPException

from app.core.config import get_settings
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.embeddings.ollama_embeddings import OllamaEmbeddingService
from app.services.llm.ollama_client import OllamaClient, OllamaConnectionError
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
    embeddings = OllamaEmbeddingService(
        base_url=settings.OLLAMA_BASE_URL,
        model=settings.EMBEDDING_MODEL,
    )
    retriever = Retriever(
        embedding_service=embeddings,
        store=store,
    )
    llm_client = OllamaClient(
        base_url=settings.OLLAMA_BASE_URL,
        model=settings.LLM_MODEL,
    )
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
    except OllamaConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

