"""add resume and user_llm_config tables

Revision ID: a1b2c3d4e5f6
Revises: c41a486a51c6
Create Date: 2026-02-07 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "c41a486a51c6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "resume",
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("source_file_name", sa.String(length=512), nullable=False),
        sa.Column("source_file_path", sa.String(length=1024), nullable=False),
        sa.Column("source_file_type", sa.String(length=20), nullable=False),
        sa.Column("extracted_text", sa.Text(), nullable=True),
        sa.Column("latex_content", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], name=op.f("resume_user_id_fkey"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("resume_pkey")),
    )
    op.create_index(op.f("resume_created_at_idx"), "resume", ["created_at"], unique=False)
    op.create_index(op.f("resume_user_id_idx"), "resume", ["user_id"], unique=False)

    op.create_table(
        "user_llm_config",
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("provider", sa.String(length=50), nullable=False),
        sa.Column("api_key_encrypted", sa.Text(), nullable=False),
        sa.Column("model_name", sa.String(length=100), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], name=op.f("user_llm_config_user_id_fkey"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("user_llm_config_pkey")),
    )
    op.create_index(op.f("user_llm_config_created_at_idx"), "user_llm_config", ["created_at"], unique=False)
    op.create_index(op.f("user_llm_config_provider_idx"), "user_llm_config", ["provider"], unique=False)
    op.create_index(op.f("user_llm_config_user_id_idx"), "user_llm_config", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("user_llm_config_user_id_idx"), table_name="user_llm_config")
    op.drop_index(op.f("user_llm_config_provider_idx"), table_name="user_llm_config")
    op.drop_index(op.f("user_llm_config_created_at_idx"), table_name="user_llm_config")
    op.drop_table("user_llm_config")
    op.drop_index(op.f("resume_user_id_idx"), table_name="resume")
    op.drop_index(op.f("resume_created_at_idx"), table_name="resume")
    op.drop_table("resume")
