# Data Policy

Scriptura Lab only indexes sources that are explicitly approved for use.

For v0.2, the repository includes project-created sample notes and a small open
corpus seed with explicit license and attribution metadata.

No modern copyrighted Bible translation should be added without explicit permission for:

- storage;
- indexing;
- semantic retrieval;
- excerpt display;
- use as LLM context;
- redistribution when applicable.

Public RAG sources must have:

1. traceable origin;
2. compatible license;
3. metadata;
4. approval status;
5. attribution information.

## Candidate Public Sources

These sources are candidates for future downloader/importer work. Do not ingest
them automatically until the specific files, license terms, attribution text, and
redistribution constraints have been reviewed.

| Source | Use case | License note |
| --- | --- | --- |
| [SBL Greek New Testament](https://www.sblgnt.com/license/) | Greek New Testament text | Published license with attribution requirements |
| [Open Scriptures Hebrew Bible](https://hb.openscriptures.org/) | Hebrew text and morphology | Open Scriptures morphology resources use CC BY 4.0 attribution terms |
| [Project Gutenberg KJV](https://www.gutenberg.org/ebooks/10) | Public-domain-in-the-US English Bible text | Public domain in the United States |
| [unfoldingWord resources](https://www.unfoldingword.org/license/) | Open biblical translation resources | Open licenses vary by resource and require review |

## Bundled Open Corpus Seed

Bundled open files live in `data/open/sources`.

The initial seed includes:

- short KJV excerpts from Project Gutenberg, marked `public-domain-us`;
- a short SBLGNT John 1 excerpt, marked `CC-BY-4.0`;
- a short OSHB/WLC Genesis 1 excerpt, marked `public-domain-wlc`;
- a project-created open source catalog note.

Do not expand this directory with full corpora until the import process preserves
license, attribution, source URL, language, reference, and approval metadata.

## Required Frontmatter

Every imported Markdown source should include enough metadata to audit usage:

```yaml
id: stable-source-id
title: Human-readable title
type: study_note
language: pt-BR
license: license-id-or-url
status: approved
use_in_rag: true
reference: optional biblical reference
source_url: https://example.org/source
attribution: Required attribution text
```

`status: approved` and `use_in_rag: true` should be explicit. Sources that are
still under review can live in the repository only if they are not ingested by
default and do not violate redistribution terms.
