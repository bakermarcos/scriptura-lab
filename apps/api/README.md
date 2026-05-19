# Scriptura Lab API

FastAPI backend for the local-first Scriptura Lab RAG MVP.

## Responsibilities

- load and validate Markdown sources;
- chunk approved sources;
- generate embeddings through the configured embedding adapter;
- store and query vectors in Qdrant;
- build grounded prompts;
- generate answers through the configured LLM adapter;
- expose health checks consumed by the web app.

## Local Run

From the repository root:

```bash
make install
make api
```

Open [http://localhost:8000/docs](http://localhost:8000/docs).

## Public Endpoints

| Endpoint | Method | Purpose |
| --- | --- | --- |
| `/health` | `GET` | API status |
| `/health/llm` | `GET` | configured generation provider status |
| `/health/embeddings` | `GET` | configured embedding provider status |
| `/sources` | `GET` | indexed source summaries |
| `/chat` | `POST` | RAG answer generation |

The web UI depends on these response shapes, so changes should be coordinated
with `apps/web/src/types/chat.ts`.
