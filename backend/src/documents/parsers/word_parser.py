"""Word document text extraction using python-docx."""

from pathlib import Path

from docx import Document

from src.documents.parsers.base import DocumentParser


class WordParser(DocumentParser):
    """Extract text from Word (.docx) files."""

    def parse(self, file_path: Path, mime_type: str | None = None) -> str:
        doc = Document(str(file_path))
        parts = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(parts) if parts else ""
