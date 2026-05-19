# Local Setup

## 1. Environment

Copy `.env.example` to `.env` and adjust values if needed.

Default local provider settings:

```env
LLM_PROVIDER=ollama
LLM_MODEL=qwen2.5:7b
EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=bge-m3
```

Optional OpenAI provider settings:

```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-5.5
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-small
OPENAI_API_KEY=your-api-key-here
```

See [model-providers.md](model-providers.md) for adapter details.

## 2. Ollama

Install Ollama locally, then pull the required models:

```bash
ollama pull qwen2.5:7b
ollama pull bge-m3
```

If `bge-m3` is not available locally, use `nomic-embed-text` as the embedding model.

If both `LLM_PROVIDER` and `EMBEDDING_PROVIDER` are set to `openai`, Ollama is not
required for the model layer.

## 3. Qdrant

```bash
docker compose up -d
```

## 4. API

```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --reload --port 8000
```

## 5. Ingestion

From the repository root:

```bash
python scripts/ingest/ingest_sample_data.py
```

Ingestion uses the configured `EMBEDDING_PROVIDER`. If you change embedding
provider or model, use a fresh `QDRANT_COLLECTION` or recreate the existing
collection before ingesting again.

## 6. Web

```bash
cd apps/web
npm install
npm run dev
```
