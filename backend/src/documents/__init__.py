"""Document parsing: extract text from PDF, Word, etc."""

from src.documents.registry import get_parser, parse_document

__all__ = ["get_parser", "parse_document"]
