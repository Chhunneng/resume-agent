"""Base protocol for document parsers."""

from pathlib import Path


class DocumentParser:
    """Protocol for extracting plain text from a document file."""

    def parse(self, file_path: Path, mime_type: str | None = None) -> str:
        """
        Extract text from the document at file_path.

        Args:
            file_path: Path to the file.
            mime_type: Optional MIME type hint.

        Returns:
            Extracted plain text.
        """
        raise NotImplementedError
