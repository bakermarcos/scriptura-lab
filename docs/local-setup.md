# Local Setup

## 1. Environment

Copy `.env.example` to `.env` and adjust values if needed.

## 2. Ollama

Install Ollama locally, then pull the required models:

```bash
ollama pull qwen2.5:7b
ollama pull bge-m3
```

If `bge-m3` is not available locally, use `nomic-embed-text` as the embedding model.

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

## 6. Web

```bash
cd apps/web
npm install
npm run dev
```

