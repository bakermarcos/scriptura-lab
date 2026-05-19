from typing import Any

from pydantic import BaseModel, Field


class SourceSummary(BaseModel):
    id: str
    title: str
    type: str
    language: str
    license: str
    reference: str | None = None


class SourcesResponse(BaseModel):
    sources: list[SourceSummary]


class SourceDocument(BaseModel):
    id: str
    title: str
    type: str
    language: str
    license: str
    status: str
    use_in_rag: bool
    body: str
    reference: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class SourceChunk(BaseModel):
    id: str
    source_id: str
    text: str
    title: str
    type: str
    language: str
    license: str
    status: str
    use_in_rag: bool
    reference: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class EmbeddedChunk(SourceChunk):
    vector: list[float]


class RetrievedChunk(BaseModel):
    id: str
    source_id: str
    text: str
    title: str
    type: str
    language: str
    license: str
    status: str
    use_in_rag: bool
    reference: str | None = None
    score: float

