"""Compile LaTeX to PDF using pdflatex (Overleaf-style server-side rendering)."""

import logging
import shutil
import subprocess
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)


def compile_latex_to_pdf(latex_content: str) -> bytes:
    """
    Compile LaTeX source to PDF using pdflatex.

    Requires pdflatex on PATH (e.g. from texlive). Uses a temp directory,
    runs pdflatex with non-interactive flags, returns PDF bytes.

    Raises:
        RuntimeError: If pdflatex is not installed or compilation fails.
    """
    if not (latex_content or "").strip():
        raise ValueError("LaTeX content is empty")

    pdflatex = shutil.which("pdflatex")
    if not pdflatex:
        raise RuntimeError(
            "pdflatex is not installed. Install texlive (e.g. apt-get install texlive-latex-base texlive-latex-extra) "
            "or use a Docker image that includes it."
        )

    with tempfile.TemporaryDirectory(prefix="latex_preview_") as tmpdir:
        path = Path(tmpdir)
        tex_file = path / "document.tex"
        tex_file.write_text(latex_content, encoding="utf-8")

        try:
            subprocess.run(
                [
                    pdflatex,
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    "-file-line-error",
                    "-output-directory",
                    str(path),
                    str(tex_file),
                ],
                capture_output=True,
                timeout=60,
                cwd=str(path),
                check=False,
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError("LaTeX compilation timed out (60s)") from None

        pdf_file = path / "document.pdf"
        if not pdf_file.exists():
            raise RuntimeError(
                "LaTeX compilation did not produce a PDF. Check that the LaTeX source is valid "
                "and that required packages are installed."
            )

        return pdf_file.read_bytes()
