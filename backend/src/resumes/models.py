"""Resume database model."""

from sqlalchemy import Column, ForeignKey, Text
from sqlmodel import Field

from src.database.base import AutoIDBaseModel


class Resume(AutoIDBaseModel, table=True):
    """
    Resume record: source file metadata, extracted text, generated LaTeX.

    Enables tracking resumes per user and future JD analysis.
    """

    __tablename__ = "resume"

    user_id: int = Field(
        sa_column=Column(
            "user_id",
            ForeignKey("user.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
    )
    title: str = Field(max_length=255, default="Untitled Resume")
    source_file_name: str = Field(max_length=512)
    source_file_path: str = Field(max_length=1024)
    source_file_type: str = Field(max_length=20)
    extracted_text: str | None = Field(default=None, sa_column=Column(Text, nullable=True))
    latex_content: str | None = Field(default=None, sa_column=Column(Text, nullable=True))
