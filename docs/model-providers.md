# Model Providers

Scriptura Lab v0.2 uses a small model harness so the RAG pipeline does not depend
directly on one vendor or runtime.

The application has two model roles:

- `LLM_PROVIDER`: generates the final answer from the grounded prompt.
- `EMBEDDING_PROVIDER`: creates vectors for ingestion and retrieval.

Each role has a provider and a model:

```env
LLM_PROVIDER=ollama
LLM_MODEL=qwen2.5:7b
EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=bge-m3
```

Supported providers in v0.2:

| Provider | Generation | Embeddings | Local |
| --- | --- | --- | --- |
| `ollama` | yes | yes | yes |
| `openai` | yes | yes | no |

## Default: Ollama

Ollama remains the default provider for both generation and embeddings.

```env
LLM_PROVIDER=ollama
LLM_MODEL=qwen2.5:7b
EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=bge-m3
OLLAMA_BASE_URL=http://localhost:11434
```

Install the models:

```bash
ollama pull qwen2.5:7b
ollama pull bge-m3
```

## Optional: OpenAI

OpenAI can be used for generation, embeddings, or both.

```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-5.5
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-small
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=your-api-key-here
```

You can also mix providers:

```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-5.5
EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=bge-m3
```

When changing `EMBEDDING_PROVIDER` or `EMBEDDING_MODEL`, re-ingest the sources into
a Qdrant collection that matches the new vector size. The simplest local option
is to change `QDRANT_COLLECTION` before re-running ingestion.

## Adapter Contract

Generation adapters implement:

```python
check_availability() -> None
generate(prompt: str) -> str
```

Embedding adapters implement:

```python
check_availability() -> None
embed(text: str) -> list[float]
```

Adapters live under:

```txt
apps/api/app/services/models/
```

The factory functions are:

```python
build_generation_adapter(settings)
build_embedding_adapter(settings)
```

Routes, ingestion, retrieval, and answer generation should depend on these
contracts instead of importing provider-specific clients directly.

## Health Checks

The API exposes provider health through stable endpoints used by the web UI:

- `GET /health/llm`
- `GET /health/embeddings`

Each endpoint returns the configured provider, model, status, and optional error.
The web app displays this information as compact status pills so local Ollama
failures and optional OpenAI configuration issues are visible before a question
is submitted.
