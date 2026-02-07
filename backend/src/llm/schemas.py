"""Schemas for LLM config API."""

from pydantic import BaseModel, Field


class LLMConfigSetRequest(BaseModel):
    """Request to set or update API key for a provider."""

    provider: str = Field(..., description="Provider id: openai, deepseek")
    api_key: str = Field(..., min_length=1, description="API key (stored encrypted)")


class LLMConfigStatus(BaseModel):
    """Status of one provider: configured or not (no key value)."""

    provider: str
    configured: bool
    model_name: str | None = None


class LLMConfigListResponse(BaseModel):
    """List of provider statuses for current user."""

    configs: list[LLMConfigStatus]
