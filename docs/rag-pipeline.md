# RAG Pipeline

## Ingestion flow

1. Load Markdown files from `data/sample/sources`.
2. Parse YAML frontmatter and Markdown body.
3. Chunk the content into paragraph-based segments.
4. Generate embeddings for each chunk with the configured embedding provider.
5. Upsert chunks and metadata into Qdrant.

## Answer flow

1. Receive the user question.
2. Generate an embedding for the question.
3. Search Qdrant for relevant chunks, filtering for approved, `use_in_rag` sources.
4. Build a prompt that includes the retrieved source excerpts.
5. Ask the configured LLM provider to answer only from the provided context.
6. Return the answer and the retrieved sources to the frontend.

## Web inspection flow

The v0.2 web UI exposes the same conceptual pipeline to the user:

1. `Pergunta`: the controlled question input.
2. `Embeddings`: vector creation by the configured embedding provider.
3. `Qdrant`: source chunk retrieval.
4. `Prompt`: grounded context assembly.
5. `Modelo`: answer generation by the configured LLM provider.

The UI also renders the recovered sources separately from the answer so the user
can inspect score, title, type, language, reference, and excerpt.

## Safe fallback

If no relevant chunk is found, or if retrieval quality is too low, the API returns:

`Não encontrei base suficiente nas fontes disponíveis para responder com segurança.`

If provider health checks fail, the web UI keeps the question text available and
shows retry actions instead of clearing user input.
