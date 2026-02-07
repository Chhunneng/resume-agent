"""Main application configuration."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Main application configuration loaded from environment variables."""

    # Application configuration
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    debug: bool = Field(default=False, alias="DEBUG")

    # Uploads (resume files)
    uploads_dir: str = Field(default="uploads", alias="UPLOADS_DIR")

    # LLM config encryption (for user API keys)
    llm_config_encryption_key: str = Field(
        default="",
        alias="LLM_CONFIG_ENCRYPTION_KEY",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        validate_by_name=True,
        validate_by_alias=True,
        extra="ignore",
    )


# Global application configuration instance
settings = Config()
