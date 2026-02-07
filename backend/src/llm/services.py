"""LLM config CRUD: encrypt and store user API keys."""

from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.llm.constants import SUPPORTED_PROVIDERS
from src.llm.encryption import encrypt_api_key
from src.llm.models import UserLLMConfig
from src.llm.schemas import LLMConfigStatus


def validate_provider(provider: str) -> None:
    """Raise ValueError if provider not supported."""
    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError(
            f"Unsupported provider: {provider}. Supported: {sorted(SUPPORTED_PROVIDERS)}"
        )


async def upsert_llm_config(
    session: AsyncSession,
    user_id: int,
    provider: str,
    api_key: str,
) -> UserLLMConfig:
    """Encrypt and save or update UserLLMConfig for the user and provider."""
    validate_provider(provider)
    encrypted = encrypt_api_key(api_key)
    if not encrypted:
        raise ValueError(
            "API key encryption not configured; set LLM_CONFIG_ENCRYPTION_KEY in environment"
        )

    result = await session.exec(
        select(UserLLMConfig).where(
            UserLLMConfig.user_id == user_id,
            UserLLMConfig.provider == provider,
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        existing.api_key_encrypted = encrypted
        existing.is_active = True
        session.add(existing)
        return existing
    config = UserLLMConfig(
        user_id=user_id,
        provider=provider,
        api_key_encrypted=encrypted,
        is_active=True,
    )
    session.add(config)
    return config


async def list_llm_config_status(
    session: AsyncSession,
    user_id: int,
) -> list[LLMConfigStatus]:
    """Return status (configured, model_name) for each provider for the user."""
    result = await session.exec(
        select(UserLLMConfig).where(
            UserLLMConfig.user_id == user_id,
            UserLLMConfig.is_active.is_(True),
        )
    )
    configs = list(result.scalars().all())
    by_provider = {c.provider: c for c in configs}
    return [
        LLMConfigStatus(
            provider=p,
            configured=p in by_provider,
            model_name=by_provider[p].model_name if p in by_provider else None,
        )
        for p in sorted(SUPPORTED_PROVIDERS)
    ]
