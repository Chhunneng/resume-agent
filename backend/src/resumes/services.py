"""Resume upload, parse, generate LaTeX, list, get, update."""

import uuid
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import settings
from src.documents import parse_document
from src.documents.constants import ALLOWED_EXTENSIONS
from src.llm import latex_service as llm_latex
from src.resumes.models import Resume


def _uploads_dir() -> Path:
    d = Path(settings.uploads_dir)
    d.mkdir(parents=True, exist_ok=True)
    return d


def _allowed_extension(filename: str) -> str | None:
    ext = (Path(filename).suffix or "").lower().lstrip(".")
    return ext if ext in ALLOWED_EXTENSIONS else None


async def upload_resume(
    session: AsyncSession,
    user_id: int,
    file: UploadFile,
) -> Resume:
    """Save file to disk, parse text, create Resume record."""
    ext = _allowed_extension(file.filename or "")
    if not ext:
        raise ValueError(f"Unsupported file type. Allowed: {sorted(ALLOWED_EXTENSIONS)}")

    uploads = _uploads_dir()
    user_dir = uploads / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)
    safe_name = f"{uuid.uuid4().hex}.{ext}"
    file_path = user_dir / safe_name

    contents = await file.read()
    file_path.write_bytes(contents)

    try:
        extracted_text = parse_document(file_path, extension=ext)
    except Exception as e:
        file_path.unlink(missing_ok=True)
        raise ValueError(f"Failed to parse document: {e}") from e

    relative_path = str(file_path.relative_to(uploads))
    title = (Path(file.filename or "Untitled").stem or "Untitled Resume")[:255]
    resume = Resume(
        user_id=user_id,
        title=title,
        source_file_name=file.filename or safe_name,
        source_file_path=relative_path,
        source_file_type=ext,
        extracted_text=extracted_text,
    )
    session.add(resume)
    return resume


async def generate_latex(
    session: AsyncSession,
    resume_id: int,
    user_id: int,
    provider: str,
) -> str:
    """Generate LaTeX for resume; update and return latex_content."""
    resume = await _get_resume_for_user(session, resume_id, user_id)
    if not resume:
        raise ValueError("Resume not found")
    if not (resume.extracted_text or "").strip():
        raise ValueError("No extracted text; re-upload the file")

    latex = await llm_latex.generate_latex_from_text(
        extracted_text=resume.extracted_text,
        user_id=user_id,
        provider=provider,
        session=session,
    )
    resume.latex_content = latex
    session.add(resume)
    return latex


async def list_resumes(
    session: AsyncSession,
    user_id: int,
) -> list[Resume]:
    """List resumes for user."""
    result = await session.exec(
        select(Resume).where(Resume.user_id == user_id).order_by(Resume.created_at.desc())
    )
    return list(result.scalars().all())


async def get_resume(
    session: AsyncSession,
    resume_id: int,
    user_id: int,
) -> Resume | None:
    """Get one resume by id for user."""
    return await _get_resume_for_user(session, resume_id, user_id)


async def update_resume(
    session: AsyncSession,
    resume_id: int,
    user_id: int,
    title: str | None = None,
    latex_content: str | None = None,
) -> Resume | None:
    """Update title and/or latex_content."""
    resume = await _get_resume_for_user(session, resume_id, user_id)
    if not resume:
        return None
    if title is not None:
        resume.title = title[:255]
    if latex_content is not None:
        resume.latex_content = latex_content
    session.add(resume)
    return resume


async def _get_resume_for_user(
    session: AsyncSession,
    resume_id: int,
    user_id: int,
) -> Resume | None:
    result = await session.exec(
        select(Resume).where(Resume.id == resume_id, Resume.user_id == user_id)
    )
    return result.scalar_one_or_none()
