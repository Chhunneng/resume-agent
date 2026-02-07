"""PDF text extraction using pypdf."""

from pathlib import Path

from pypdf import PdfReader

from src.documents.parsers.base import DocumentParser


class PDFParser(DocumentParser):
    """Extract text from PDF files."""

    def parse(self, file_path: Path, mime_type: str | None = None) -> str:
        reader = PdfReader(str(file_path))
        parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                parts.append(text)
        return "\n\n".join(parts) if parts else ""
