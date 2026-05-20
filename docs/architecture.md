# Architecture

Scriptura Lab uses a local-first RAG pipeline with configurable model providers:

1. React + Vite web app sends a question to the FastAPI backend.
2. FastAPI generates an embedding for the question using the configured embedding adapter.
3. Qdrant returns the most relevant indexed chunks.
4. The backend builds a grounded prompt with those sources.
5. The configured LLM adapter generates the final answer in Portuguese.
6. The API returns the answer together with the retrieved sources.

## Components

- `apps/web`: single-page editorial study workspace
- `apps/api`: FastAPI app, ingestion pipeline, vector search, and model provider adapters
- `data/sample/sources`: project-created Markdown notes with frontmatter metadata
- `data/open/sources`: small approved open corpus seed for RAG
- `data/custom/sources`: user-added local documents
- `scripts/ingest`: ingestion entrypoint for local indexing
- `docker-compose.yml`: local Qdrant service

## Design constraints

- Local-first by default
- Source-grounded responses
- Explicit metadata for every indexed source
- No copyrighted modern Bible translations in the repository
- Stable public API contract between web and API

## Web workspace

The v0.2 web app keeps the backend API contract stable and improves presentation:

- sticky top bar with brand, version badge, and compact service status;
- visible service checks for API, generation provider, and embedding provider;
- controlled question input with suggestions and preserved text on error;
- RAG trail that mirrors the backend flow: question, embeddings, Qdrant, prompt, model;
- answer panel with empty, loading, error, retry, and result states;
- source cards with score, type, language, reference, and excerpt.

The web app does not import provider-specific clients and does not call Ollama or
OpenAI directly. Provider selection stays in the backend.

## Model provider harness

The backend separates model usage into two roles:

- generation: prompt in, answer text out
- embeddings: text in, vector out

The factory lives in `apps/api/app/services/models/factory.py`.
Provider-specific adapters live in `apps/api/app/services/models/`,
`apps/api/app/services/llm/`, and `apps/api/app/services/embeddings/`.

## Public API boundary

The frontend currently relies on:

- `GET /health`
- `GET /health/llm`
- `GET /health/embeddings`
- `GET /sources`
- `POST /chat`

Changing these response shapes should be treated as a public interface change and
paired with TypeScript type updates in `apps/web/src/types/chat.ts`.
