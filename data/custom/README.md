# Custom Sources

Add local or project-specific Markdown sources in `sources/`.

The default ingestion command includes this directory:

```bash
make ingest
```

## Template

Create a file such as `data/custom/sources/my-note.md`:

```markdown
---
id: my-note
title: My Study Note
type: study_note
language: pt-BR
license: project-created
reference: John 1
source_url: optional-url
attribution: optional attribution text
use_in_rag: true
status: approved
---

Write the source content here.
```

Required fields:

- `id`
- `title`
- `type`
- `language`
- `license`
- `status`
- `use_in_rag`

Use `status: approved` and `use_in_rag: true` only when the document is cleared
for storage, indexing, retrieval, excerpt display, and LLM context use.
