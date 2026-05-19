import re

from app.schemas.source import SourceChunk, SourceDocument


class TextChunker:
    def __init__(self, target_chars: int = 1000, min_chunk_chars: int = 800) -> None:
        self.target_chars = target_chars
        self.min_chunk_chars = min_chunk_chars

    def chunk_document(self, document: SourceDocument) -> list[SourceChunk]:
        paragraphs = self._split_paragraphs(document.body)
        buffer: list[str] = []
        chunks: list[str] = []

        for paragraph in paragraphs:
            if len(paragraph) > self.target_chars:
                if buffer:
                    chunks.append("\n\n".join(buffer))
                    buffer = []
                chunks.extend(self._split_long_paragraph(paragraph))
                continue

            candidate = "\n\n".join([*buffer, paragraph]).strip()
            if buffer and len(candidate) > self.target_chars:
                chunks.append("\n\n".join(buffer))
                buffer = [paragraph]
                continue

            buffer.append(paragraph)
            if len("\n\n".join(buffer)) >= self.min_chunk_chars:
                chunks.append("\n\n".join(buffer))
                buffer = []

        if buffer:
            chunks.append("\n\n".join(buffer))

        return [
            SourceChunk(
                id=f"{document.id}::chunk-{index}",
                source_id=document.id,
                text=chunk_text,
                title=document.title,
                type=document.type,
                language=document.language,
                license=document.license,
                status=document.status,
                use_in_rag=document.use_in_rag,
                reference=document.reference,
                metadata=document.metadata,
            )
            for index, chunk_text in enumerate(chunks)
        ]

    def _split_paragraphs(self, body: str) -> list[str]:
        paragraphs = [part.strip() for part in re.split(r"\n\s*\n", body) if part.strip()]
        return paragraphs or [body.strip()]

    def _split_long_paragraph(self, paragraph: str) -> list[str]:
        chunks: list[str] = []
        start = 0
        while start < len(paragraph):
            end = start + self.target_chars
            chunks.append(paragraph[start:end].strip())
            start = end
        return [chunk for chunk in chunks if chunk]

