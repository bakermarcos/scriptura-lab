# Open Source Corpus

This directory contains the first open corpus seed for Scriptura Lab.

Files inside `sources/` are valid RAG Markdown documents and are indexed by the
default ingestion command:

```bash
make ingest
```

The current seed is intentionally small. It includes public-domain KJV excerpts,
short original-language excerpts, and a source catalog document that records
license and attribution notes for open Bible resources.

## Included Sources

| Source | Files | License metadata |
| --- | --- | --- |
| Project Gutenberg KJV | `kjv-*.md` | `public-domain-us` |
| SBL Greek New Testament | `sblgnt-*.md` | `CC-BY-4.0` |
| Open Scriptures Hebrew Bible / WLC | `oshb-*.md` | `public-domain-wlc` plus OSHB attribution metadata |
| Open resource catalog | `open-source-catalog.md` | `project-created` |

## Policy

Do not add full external corpora here until the project has:

1. a downloader/importer that preserves attribution metadata;
2. license review for the exact files being imported;
3. tests for required frontmatter fields;
4. a decision about whether the data should be vendored or downloaded locally.

Use `data/custom/sources/` for local documents that should not be treated as part
of the bundled open corpus.
