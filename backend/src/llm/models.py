"""User LLM provider config: store encrypted API keys per provider."""

from sqlalchemy import Column, ForeignKey, Text
from sqlmodel import Field

from src.database.base import AutoIDBaseModel


class UserLLMConfig(AutoIDBaseModel, table=True):
    """
    User's LLM API key and optional model name per provider.

    Provider examples: openai, deepseek; extensible to gemini.
    """

    __tablename__ = "user_llm_config"

    user_id: int = Field(
        sa_column=Column(
            "user_id",
            ForeignKey("user.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
    )
    provider: str = Field(max_length=50, index=True)
    api_key_encrypted: str = Field(sa_column=Column(Text, nullable=False))
    model_name: str | None = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)
