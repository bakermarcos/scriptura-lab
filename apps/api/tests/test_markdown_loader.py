from pathlib import Path

import pytest

from app.services.ingestion.markdown_loader import MarkdownLoader


def test_markdown_loader_extracts_frontmatter_body_and_extra_metadata(tmp_path: Path) -> None:
    source_file = tmp_path / "sample.md"
    source_file.write_text(
        """---
id: sample-note
title: Sample note
type: study_note
language: pt-BR
license: project-created
reference: John 1
status: approved
use_in_rag: true
lemma: logos
---

Primeiro parágrafo.

Segundo parágrafo.
""",
        encoding="utf-8",
    )

    document = MarkdownLoader().load_file(source_file)

    assert document.id == "sample-note"
    assert document.title == "Sample note"
    assert document.reference == "John 1"
    assert document.use_in_rag is True
    assert document.body == "Primeiro parágrafo.\n\nSegundo parágrafo."
    assert document.metadata == {"lemma": "logos"}


def test_markdown_loader_raises_when_required_fields_are_missing(tmp_path: Path) -> None:
    invalid_file = tmp_path / "invalid.md"
    invalid_file.write_text(
        """---
id: invalid-note
title: Missing fields
type: study_note
language: pt-BR
license: project-created
---

Conteúdo sem campos mínimos.
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="missing required fields"):
        MarkdownLoader().load_file(invalid_file)

