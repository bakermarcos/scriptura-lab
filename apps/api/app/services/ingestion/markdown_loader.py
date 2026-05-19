from pathlib import Path

import frontmatter

from app.schemas.source import SourceDocument


class MarkdownLoader:
    REQUIRED_FIELDS = {
        "id",
        "title",
        "type",
        "language",
        "license",
        "status",
        "use_in_rag",
    }

    def load_directory(self, directory: Path) -> list[SourceDocument]:
        documents: list[SourceDocument] = []
        for path in sorted(directory.glob("*.md")):
            documents.append(self.load_file(path))
        return documents

    def load_file(self, path: Path) -> SourceDocument:
        post = frontmatter.load(path)
        metadata = dict(post.metadata)
        missing_fields = sorted(self.REQUIRED_FIELDS - metadata.keys())
        if missing_fields:
            raise ValueError(
                f"Markdown file {path.name} is missing required fields: {', '.join(missing_fields)}"
            )

        body = post.content.strip()
        if not body:
            raise ValueError(f"Markdown file {path.name} has no body content.")

        reserved_keys = {
            "id",
            "title",
            "type",
            "language",
            "license",
            "status",
            "use_in_rag",
            "reference",
        }
        extra_metadata = {
            key: value
            for key, value in metadata.items()
            if key not in reserved_keys
        }

        return SourceDocument(
            id=str(metadata["id"]),
            title=str(metadata["title"]),
            type=str(metadata["type"]),
            language=str(metadata["language"]),
            license=str(metadata["license"]),
            status=str(metadata["status"]),
            use_in_rag=bool(metadata["use_in_rag"]),
            reference=metadata.get("reference"),
            body=body,
            metadata=extra_metadata,
        )

