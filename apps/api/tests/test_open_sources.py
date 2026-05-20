from pathlib import Path

from app.core.config import Settings
from app.services.ingestion.markdown_loader import MarkdownLoader


ROOT_DIR = Path(__file__).resolve().parents[3]


def test_bundled_open_sources_are_loadable() -> None:
    documents = MarkdownLoader().load_directory(ROOT_DIR / "data" / "open" / "sources")

    assert len(documents) == 5
    assert {document.id for document in documents} >= {
        "kjv-complete",
        "sblgnt-complete",
        "oshb-wlc-complete",
        "unfoldingword-open-bible-stories-complete",
    }
    assert all(document.status == "approved" for document in documents)
    assert all(document.use_in_rag for document in documents)


def test_settings_parse_ingest_source_dirs_and_default_languages() -> None:
    settings = Settings(
        INGEST_SOURCE_DIRS="data/sample/sources, data/open/sources, data/custom/sources",
        DEFAULT_SOURCE_LANGUAGES="pt-BR, en, grc, hbo",
    )

    assert settings.ingest_source_dirs == [
        "data/sample/sources",
        "data/open/sources",
        "data/custom/sources",
    ]
    assert settings.default_source_languages == ["pt-BR", "en", "grc", "hbo"]
