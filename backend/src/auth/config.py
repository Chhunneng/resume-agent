from datetime import timedelta

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthConfig(BaseSettings):
    """Authentication configuration loaded from environment variables."""

    jwt_alg: str = Field(default="HS256", alias="JWT_ALG")
    jwt_access_token_secret: str = Field(alias="JWT_ACCESS_TOKEN_SECRET")
    jwt_refresh_token_secret: str = Field(alias="JWT_REFRESH_TOKEN_SECRET")
    jwt_access_token_exp: timedelta = Field(
        default=timedelta(minutes=15), alias="JWT_ACCESS_TOKEN_EXP"
    )
    jwt_refresh_token_exp: timedelta = Field(
        default=timedelta(days=30),
        alias="JWT_REFRESH_TOKEN_EXP",
    )

    secure_cookies: bool = Field(default=True, alias="SECURE_COOKIES")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        validate_by_name=True,
        validate_by_alias=True,
        extra="ignore",
    )


auth_settings = AuthConfig()
