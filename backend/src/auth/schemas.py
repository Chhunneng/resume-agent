"""Authentication request and response schemas."""

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field

if TYPE_CHECKING:
    from .models import User

from src.models import CustomBaseModel


class RegisterRequest(CustomBaseModel):
    """Request schema for user registration."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password (min 8 characters)")
    firstname: str = Field(..., min_length=1, max_length=100, description="User first name")
    lastname: str = Field(..., min_length=1, max_length=100, description="User last name")
    phone_number: str | None = Field(
        default=None,
        max_length=20,
        description="User phone number",
    )
    street_address: str | None = Field(
        default=None,
        max_length=255,
        description="Street address",
    )
    city: str | None = Field(
        default=None,
        max_length=100,
        description="City",
    )
    state: str | None = Field(
        default=None,
        max_length=100,
        description="State or province",
    )
    zip_code: str | None = Field(
        default=None,
        max_length=20,
        description="ZIP or postal code",
    )
    country: str | None = Field(
        default=None,
        max_length=100,
        description="Country",
    )


class LoginRequest(CustomBaseModel):
    """Request schema for user login."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class RefreshTokenRequest(CustomBaseModel):
    """Request schema for token refresh."""

    refresh_token: str = Field(..., description="Refresh token")


class TokenResponse(CustomBaseModel):
    """Response schema for authentication tokens."""

    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")


class AccessTokenResponse(CustomBaseModel):
    """Response schema for refreshed access token."""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class UserResponse(CustomBaseModel):
    """Response schema for user information."""

    id: int
    email: str
    firstname: str
    lastname: str
    phone_number: str | None
    registration_date: datetime
    last_login: datetime | None
    is_active: bool
    roles: list[str]
    street_address: str | None
    city: str | None
    state: str | None
    zip_code: str | None
    country: str | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_user(cls, user: "User") -> "UserResponse":
        """
        Create UserResponse from User model.

        Args:
            user: User database model instance.

        Returns:
            UserResponse instance.
        """
        return cls(
            id=user.id,
            email=user.email,
            firstname=user.firstname,
            lastname=user.lastname,
            phone_number=user.phone_number,
            registration_date=user.created_at,
            last_login=user.last_login,
            is_active=user.is_active,
            roles=user.get_role_names(),
            street_address=user.street_address,
            city=user.city,
            state=user.state,
            zip_code=user.zip_code,
            country=user.country,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
