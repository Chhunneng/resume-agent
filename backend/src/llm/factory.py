"""Build LangChain chat model from provider and user config."""

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI

from src.llm.constants import (
    DEEPSEEK_BASE_URL,
    DEFAULT_MODELS,
    PROVIDER_DEEPSEEK,
    PROVIDER_OPENAI,
    SUPPORTED_PROVIDERS,
)


def get_chat_model(
    provider: str,
    api_key: str,
    model_name: str | None = None,
) -> BaseChatModel:
    """
    Return a LangChain chat model for the given provider and API key.

    Args:
        provider: One of openai, deepseek (extensible to gemini).
        api_key: Decrypted API key for the provider.
        model_name: Optional model override (e.g. gpt-4o, deepseek-chat).

    Returns:
        Configured chat model instance.

    Raises:
        ValueError: If provider is not supported.
    """
    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError(
            f"Unsupported provider: {provider}. Supported: {sorted(SUPPORTED_PROVIDERS)}"
        )

    model = model_name or DEFAULT_MODELS.get(provider, "gpt-4o-mini")

    if provider == PROVIDER_OPENAI:
        return ChatOpenAI(
            model=model,
            openai_api_key=api_key,
            temperature=0.2,
        )
    if provider == PROVIDER_DEEPSEEK:
        return ChatOpenAI(
            model=model,
            openai_api_key=api_key,
            openai_api_base=DEEPSEEK_BASE_URL,
            temperature=0.2,
        )
    raise ValueError(f"No factory for provider: {provider}")
