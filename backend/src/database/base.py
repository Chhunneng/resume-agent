"""Base SQLModel with common fields for all database models."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, func
from sqlmodel import Field, SQLModel

from src.datetime.utils import get_current_utc_datetime


class BaseModel(SQLModel):
    """
    Base SQLModel with created_at and updated_at timestamps.

    All database models should inherit from this class to automatically
    get created_at and updated_at fields with proper UTC timestamps.

    The created_at field is set automatically when a record is created.
    The updated_at field is updated automatically whenever a record is modified.
    """

    created_at: datetime | None = Field(
        default_factory=get_current_utc_datetime,
        index=True,
        nullable=False,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": func.now()},
    )

    updated_at: datetime | None = Field(
        default_factory=get_current_utc_datetime,
        nullable=False,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": func.now(),
        },
    )


class AutoIDBaseModel(BaseModel, table=False):
    """
    Base model with autoincrementing integer primary key.

    Database models inheriting from this base will have an `id` column (int, primary key).
    """

    id: int | None = Field(default=None, primary_key=True)


class UUIDBaseModel(BaseModel, table=False):
    """
    Base model with UUID primary key.

    Database models inheriting from this base will have an `id` column (UUID, primary key).
    """

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
    )
