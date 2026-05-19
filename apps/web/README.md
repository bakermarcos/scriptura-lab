# Scriptura Lab Web

React frontend for the Scriptura Lab RAG workspace.

## What It Does

The v0.2 UI presents the study flow as an inspectable workspace:

- compact service health for API, LLM, and embeddings;
- editorial question panel with suggestions;
- answer panel with empty, loading, error, and result states;
- visible RAG trail from question to model response;
- source cards with score, metadata, reference, and excerpt.

The web app does not call model providers directly. It only talks to the
FastAPI backend.

## Local Run

From the repository root:

```bash
make install
make web
```

Or from this directory:

```bash
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173).

## API Configuration

Set `WEB_API_BASE_URL` in the repository root `.env`:

```env
WEB_API_BASE_URL=http://localhost:8000
```

Restart the Vite dev server after changing this value.

## Build

```bash
npm run build
```

The root equivalent is:

```bash
make build-web
```

## Design Notes

Mantine is used for component primitives and accessibility behavior. The visual
identity lives in `src/styles.css` so the app keeps a distinct editorial look
instead of a generic toolkit appearance.
