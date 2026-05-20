# Web UI

The v0.2 web app is an editorial study workspace for the existing RAG API. It
does not change the backend contract; it improves how the user asks questions,
sees system status, follows the RAG flow, reads answers, and audits retrieved
sources.

## Stack

- React 18
- Vite
- TypeScript
- Mantine 7 for accessible component primitives
- `lucide-react` for icons
- `@fontsource/newsreader` for headings
- `@fontsource/source-sans-3` for interface text

## Layout

The app is organized as:

1. sticky top bar with brand, `v0.2` badge, and compact service status;
2. editorial hero card;
3. visible RAG trail: question, embeddings, Qdrant, prompt, model;
4. query panel with visible label, suggestions, loading state, and preserved input;
5. answer panel with empty, loading, error, and result states;
6. source section with dense cards, score indicator, metadata, and excerpt.

## API Contract

The UI still depends on the same public API helpers:

```ts
sendChat(question)
getHealth()
getLlmHealth()
getEmbeddingHealth()
```

The endpoints are unchanged:

- `GET /health`
- `GET /health/llm`
- `GET /health/embeddings`
- `POST /chat`

## Configuration

The web build reads `WEB_API_BASE_URL` from the repository root `.env`.

```env
WEB_API_BASE_URL=http://localhost:8000
```

The value is embedded by Vite at build/dev-server startup. Restart `make web`
after changing it.

## Accessibility and Responsiveness

The v0.2 CSS defines semantic tokens for surface, text, accent, border, danger,
and success colors. It also includes:

- visible focus outlines;
- 44px minimum target sizing for primary interactive controls;
- mobile, tablet, and desktop breakpoints;
- no horizontal overflow at 375px, 768px, and 1280px;
- `prefers-reduced-motion` handling.

## Validation

Run:

```bash
make build-web
make test
```

For manual validation, run the API and web app, then test:

- initial empty state;
- API, LLM, and embeddings status pills;
- suggested questions;
- loading state while a question is submitted;
- answer rendering;
- source cards;
- retry/error behavior when the API is offline.

The default backend retrieval language list includes `pt-BR`, `en`, `grc`, and
`hbo`, so bundled project notes, English KJV excerpts, Greek excerpts, and Hebrew
excerpts can all be retrieved unless a request overrides `source_languages`.
