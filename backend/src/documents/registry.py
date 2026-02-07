"""Parser registry: map file extension to parser instance."""

from pathlib import Path

from src.documents.constants import ALLOWED_EXTENSIONS, EXTENSION_TO_MIME
from src.documents.parsers.base import DocumentParser
from src.documents.parsers.pdf_parser import PDFParser
from src.documents.parsers.word_parser import WordParser

_PARSERS: dict[str, DocumentParser] = {
    "pdf": PDFParser(),
    "docx": WordParser(),
}


def get_parser(extension: str) -> DocumentParser | None:
    """
    Return the parser for the given file extension (lowercase, no dot).

    Returns None if the extension is not supported.
    """
    ext = extension.lower().lstrip(".")
    return _PARSERS.get(ext)


def parse_document(file_path: Path, extension: str | None = None) -> str:
    """
    Extract text from a document file.

    Args:
        file_path: Path to the file.
        extension: File extension (e.g. 'pdf', 'docx'). If None, inferred from path.

    Returns:
        Extracted text.

    Raises:
        ValueError: If extension is not allowed or no parser is available.
    """
    ext = (extension or file_path.suffix).lower().lstrip(".")
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}. Allowed: {sorted(ALLOWED_EXTENSIONS)}")
    parser = get_parser(ext)
    if not parser:
        raise ValueError(f"No parser for extension: {ext}")
    mime = EXTENSION_TO_MIME.get(ext)
    return parser.parse(file_path, mime_type=mime)
