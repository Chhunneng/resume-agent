"""Generate LaTeX from extracted text using LLM."""

from langchain_core.messages import HumanMessage, SystemMessage
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.llm.encryption import decrypt_api_key
from src.llm.factory import get_chat_model
from src.llm.models import UserLLMConfig
from src.llm.prompts import LATEX_SYSTEM_PROMPT, build_latex_user_prompt


async def get_user_llm_config(
    session: AsyncSession,
    user_id: int,
    provider: str,
) -> UserLLMConfig | None:
    """Load active UserLLMConfig for user and provider."""
    result = await session.exec(
        select(UserLLMConfig).where(
            UserLLMConfig.user_id == user_id,
            UserLLMConfig.provider == provider,
            UserLLMConfig.is_active.is_(True),
        )
    )
    return result.scalar_one_or_none()


def _strip_markdown_latex(raw: str) -> str:
    """Remove markdown code fences if present."""
    text = raw.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)
    return text.strip()


async def generate_latex_from_text(
    extracted_text: str,
    user_id: int,
    provider: str,
    session: AsyncSession,
) -> str:
    """
    Generate LaTeX resume from extracted text using user's LLM config.

    Args:
        extracted_text: Plain text from parsed document.
        user_id: Current user id (for loading API key).
        provider: openai or deepseek.
        session: DB session (for UserLLMConfig).

    Returns:
        Generated LaTeX string.

    Raises:
        ValueError: If no config for provider or decryption fails.
    """
    config = await get_user_llm_config(session, user_id, provider)
    if not config:
        raise ValueError(f"Configure API key for {provider} in settings")

    api_key = decrypt_api_key(config.api_key_encrypted)
    if not api_key:
        raise ValueError("Invalid or missing API key; please set it again in settings")

    model = get_chat_model(
        provider=provider,
        api_key=api_key,
        model_name=config.model_name,
    )
    messages = [
        SystemMessage(content=LATEX_SYSTEM_PROMPT),
        HumanMessage(content=build_latex_user_prompt(extracted_text)),
    ]
    response = await model.ainvoke(messages)
    content = response.content if hasattr(response, "content") else str(response)
    return _strip_markdown_latex(content)
