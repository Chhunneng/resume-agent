"""Resumes API: upload, list, get, generate LaTeX, update, preview PDF."""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import Response
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import get_current_active_user
from src.auth.models import User
from src.database.connection import get_db_session
from src.resumes import latex_compile
from src.resumes import services as resume_services
from src.resumes.models import Resume
from src.resumes.schemas import (
    GenerateLatexRequest,
    GenerateLatexResponse,
    PreviewPdfRequest,
    ResumeCreateResponse,
    ResumeDetailResponse,
    ResumeListItem,
    ResumeListResponse,
    ResumeUpdateRequest,
)

router = APIRouter()


def _resume_to_list_item(r: Resume) -> ResumeListItem:
    return ResumeListItem(
        id=r.id,
        title=r.title,
        source_file_name=r.source_file_name,
        source_file_type=r.source_file_type,
        has_latex=bool((r.latex_content or "").strip()),
        created_at=r.created_at,
    )


@router.post(
    "/upload",
    response_model=ResumeCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload resume",
)
async def upload_resume(
    file: UploadFile,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db_session),
):
    try:
        resume = await resume_services.upload_resume(session, current_user.id, file)
        await session.commit()
        await session.refresh(resume)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    return ResumeCreateResponse(
        id=resume.id,
        title=resume.title,
        source_file_name=resume.source_file_name,
        source_file_type=resume.source_file_type,
        created_at=resume.created_at,
    )


@router.post(
    "/{resume_id}/generate-latex",
    response_model=GenerateLatexResponse,
    summary="Generate LaTeX from extracted text",
)
async def generate_latex(
    resume_id: int,
    body: GenerateLatexRequest,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db_session),
):
    try:
        latex = await resume_services.generate_latex(
            session, resume_id, current_user.id, body.provider
        )
        await session.commit()
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    return GenerateLatexResponse(latex_content=latex)


@router.get(
    "",
    response_model=ResumeListResponse,
    summary="List resumes",
)
async def list_resumes(
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db_session),
):
    items = await resume_services.list_resumes(session, current_user.id)
    return ResumeListResponse(items=[_resume_to_list_item(r) for r in items])


@router.get(
    "/{resume_id}",
    response_model=ResumeDetailResponse,
    summary="Get resume",
)
async def get_resume(
    resume_id: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db_session),
):
    resume = await resume_services.get_resume(session, resume_id, current_user.id)
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    return ResumeDetailResponse(
        id=resume.id,
        title=resume.title,
        source_file_name=resume.source_file_name,
        source_file_type=resume.source_file_type,
        extracted_text=resume.extracted_text,
        latex_content=resume.latex_content,
        created_at=resume.created_at,
        updated_at=resume.updated_at,
    )


@router.post(
    "/preview-pdf",
    response_class=Response,
    summary="Compile LaTeX to PDF (Overleaf-style preview)",
)
async def preview_pdf(
    body: PreviewPdfRequest,
    current_user: User = Depends(get_current_active_user),
):
    """Compile LaTeX to PDF and return the binary. Requires pdflatex on the server."""
    try:
        pdf_bytes = latex_compile.compile_latex_to_pdf(body.latex_content)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        ) from e
    return Response(content=pdf_bytes, media_type="application/pdf")


@router.patch(
    "/{resume_id}",
    response_model=ResumeDetailResponse,
    summary="Update resume (title or latex_content)",
)
async def update_resume(
    resume_id: int,
    body: ResumeUpdateRequest,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db_session),
):
    resume = await resume_services.update_resume(
        session,
        resume_id,
        current_user.id,
        title=body.title,
        latex_content=body.latex_content,
    )
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    await session.commit()
    await session.refresh(resume)
    return ResumeDetailResponse(
        id=resume.id,
        title=resume.title,
        source_file_name=resume.source_file_name,
        source_file_type=resume.source_file_type,
        extracted_text=resume.extracted_text,
        latex_content=resume.latex_content,
        created_at=resume.created_at,
        updated_at=resume.updated_at,
    )
