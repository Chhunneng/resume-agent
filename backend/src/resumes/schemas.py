"""Schemas for resumes API."""

from datetime import datetime

from pydantic import BaseModel, Field


class ResumeCreateResponse(BaseModel):
    """Response after uploading a resume."""

    id: int
    title: str
    source_file_name: str
    source_file_type: str
    created_at: datetime


class ResumeListItem(BaseModel):
    """One resume in list."""

    id: int
    title: str
    source_file_name: str
    source_file_type: str
    has_latex: bool
    created_at: datetime


class ResumeListResponse(BaseModel):
    """List of user's resumes."""

    items: list[ResumeListItem]


class ResumeDetailResponse(BaseModel):
    """Full resume for detail/editor."""

    id: int
    title: str
    source_file_name: str
    source_file_type: str
    extracted_text: str | None
    latex_content: str | None
    created_at: datetime
    updated_at: datetime


class GenerateLatexRequest(BaseModel):
    """Request body for generate LaTeX."""

    provider: str = Field(..., description="openai or deepseek")


class GenerateLatexResponse(BaseModel):
    """Response with generated LaTeX."""

    latex_content: str


class ResumeUpdateRequest(BaseModel):
    """Optional fields for PATCH."""

    title: str | None = None
    latex_content: str | None = None


class PreviewPdfRequest(BaseModel):
    """Request body for compiling LaTeX to PDF preview."""

    latex_content: str = Field(..., min_length=1, description="LaTeX source to compile")
