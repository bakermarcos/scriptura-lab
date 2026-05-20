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
- ingest configured source directories, including `data/open/sources` and
  `data/custom/sources`.

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

## Ingestion Sources

The default source directories are configured by `INGEST_SOURCE_DIRS`:

```env
INGEST_SOURCE_DIRS=data/sample/sources,data/open/sources,data/custom/sources
```

Use `data/custom/sources` for new local documents. See
`data/custom/README.md` for the required frontmatter template.
