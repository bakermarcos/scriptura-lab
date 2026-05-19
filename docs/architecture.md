# Architecture

Scriptura Lab v0.1 uses a local-first RAG pipeline:

1. React + Vite web app sends a question to the FastAPI backend.
2. FastAPI generates an embedding for the question using Ollama.
3. Qdrant returns the most relevant indexed chunks.
4. The backend builds a grounded prompt with those sources.
5. Ollama generates the final answer in Portuguese.
6. The API returns the answer together with the retrieved sources.

## Components

- `apps/web`: single-page chat UI
- `apps/api`: FastAPI app, ingestion pipeline, vector search, and Ollama integration
- `data/sample/sources`: project-created Markdown notes with frontmatter metadata
- `scripts/ingest`: ingestion entrypoint for local indexing
- `docker-compose.yml`: local Qdrant service

## Design constraints

- Local-first by default
- Source-grounded responses
- Explicit metadata for every indexed source
- No copyrighted modern Bible translations in the repository

