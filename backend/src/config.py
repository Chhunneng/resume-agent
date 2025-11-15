"""Main application configuration."""

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Main application configuration loaded from environment variables."""

    # Application configuration
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        populate_by_name = True
        extra = "ignore"  # Ignore extra environment variables not defined in the model


# Global application configuration instance
settings = Config()
