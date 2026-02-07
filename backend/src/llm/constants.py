"""LLM provider identifiers; extensible for Gemini etc."""

PROVIDER_OPENAI = "openai"
PROVIDER_DEEPSEEK = "deepseek"
# PROVIDER_GEMINI = "gemini"  # future

SUPPORTED_PROVIDERS = {PROVIDER_OPENAI, PROVIDER_DEEPSEEK}

DEFAULT_MODELS: dict[str, str] = {
    PROVIDER_OPENAI: "gpt-4o-mini",
    PROVIDER_DEEPSEEK: "deepseek-chat",
}

# DeepSeek API is OpenAI-compatible
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
