"""JWT token creation and verification utilities."""

from enum import Enum
from typing import Any

import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError, InvalidTokenError

from src.datetime.utils import get_current_utc_datetime

from .config import auth_settings


class TokenType(str, Enum):
    """JWT token type enumeration."""

    ACCESS = "access"
    REFRESH = "refresh"


def create_access_token(
    user_id: int,
    email: str,
    roles: list[str],
) -> str:
    """
    Create a JWT access token.

    Args:
        user_id: User ID to include in token.
        email: User email to include in token.
        roles: List of user role names to include in token.

    Returns:
        Encoded JWT access token.
    """
    now = get_current_utc_datetime()
    expire = now + auth_settings.jwt_access_token_exp

    payload: dict[str, Any] = {
        "sub": str(user_id),  # Subject (user ID)
        "email": email,
        "roles": roles,
        "type": TokenType.ACCESS.value,
        "iat": now,  # Issued at
        "exp": expire,  # Expiration
    }

    return jwt.encode(
        payload,
        auth_settings.jwt_access_token_secret,
        algorithm=auth_settings.jwt_alg,
    )


def create_refresh_token(
    user_id: int,
    email: str,
) -> str:
    """
    Create a JWT refresh token.

    Args:
        user_id: User ID to include in token.
        email: User email to include in token.

    Returns:
        Encoded JWT refresh token.
    """
    now = get_current_utc_datetime()
    expire = now + auth_settings.jwt_refresh_token_exp

    payload: dict[str, Any] = {
        "sub": str(user_id),  # Subject (user ID)
        "email": email,
        "type": TokenType.REFRESH.value,
        "iat": now,  # Issued at
        "exp": expire,  # Expiration
    }

    return jwt.encode(
        payload,
        auth_settings.jwt_refresh_token_secret,
        algorithm=auth_settings.jwt_alg,
    )


def verify_token(token: str, token_type: TokenType = TokenType.ACCESS) -> dict[str, Any]:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token to verify.
        token_type: Type of token (TokenType.ACCESS or TokenType.REFRESH).

    Returns:
        Decoded token payload.

    Raises:
        ValueError: If token is invalid or expired.
    """
    if token_type == TokenType.ACCESS:
        secret = auth_settings.jwt_access_token_secret
    elif token_type == TokenType.REFRESH:
        secret = auth_settings.jwt_refresh_token_secret
    else:
        raise ValueError(f"Invalid token type: {token_type}")

    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=[auth_settings.jwt_alg],
        )

        # Verify token type
        if payload.get("type") != token_type.value:
            raise ValueError(f"Invalid token type. Expected {token_type.value}")

        return payload
    except ExpiredSignatureError as e:
        raise ValueError("Token has expired") from e
    except DecodeError as e:
        raise ValueError("Invalid token format") from e
    except InvalidTokenError as e:
        raise ValueError("Invalid token") from e
