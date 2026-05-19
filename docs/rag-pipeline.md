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

## Safe fallback

If no relevant chunk is found, or if retrieval quality is too low, the API returns:

`Não encontrei base suficiente nas fontes disponíveis para responder com segurança.`
