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

Install Ollama locally. If it is not already running, start it in a separate
terminal:

```bash
ollama serve
```

Then pull the required models:

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

If `docker compose` is not available in your local Docker installation, use:

```bash
docker-compose up -d
```

## 4. API

Recommended root workflow:

```bash
make install
make api
```

Manual workflow:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e "apps/api[dev]"
cd apps/api
../../.venv/bin/uvicorn app.main:app --reload --port 8000
```

## 5. Ingestion

From the repository root:

```bash
make ingest
```

Ingestion uses the configured `EMBEDDING_PROVIDER`. If you change embedding
provider or model, use a fresh `QDRANT_COLLECTION` or recreate the existing
collection before ingesting again.

## 6. Web

Recommended root workflow:

```bash
make web
```

Manual workflow:

```bash
cd apps/web
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173).

The web app reads `WEB_API_BASE_URL` from the repository root `.env`.

```env
WEB_API_BASE_URL=http://localhost:8000
```

Restart the Vite dev server after changing this value.

## 7. Validation

```bash
make build-web
make test
```

Manual UI checks:

- initial empty state;
- API, LLM, and embeddings status;
- suggested question submission;
- loading, error, and retry states;
- answer rendering;
- source cards;
- 375px, 768px, and desktop layouts.

## Troubleshooting

- `unknown shorthand flag: 'd' in -d`: your Docker CLI may not support the
  `docker compose` plugin. Try `docker-compose up -d`.
- `Could not reach Ollama at http://localhost:11434`: start Ollama with
  `ollama serve`, then pull the configured models.
- API is online but chat fails after changing embedding models: re-ingest into a
  fresh Qdrant collection because vector dimensions must match.
