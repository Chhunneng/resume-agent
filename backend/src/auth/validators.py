"""Authentication validation helpers that raise HTTPException on failure."""

from fastapi import HTTPException, status

from .models import User
from .password import verify_password


def validate_user_for_auth(
    user: User | None,
    password: str | None = None,
) -> User:
    """
    Validate user for authentication.

    Args:
        user: User model instance or None.
        password: Plain text password to verify (optional).

    Returns:
        Validated user instance.

    Raises:
        HTTPException: If user is invalid, password is wrong, or user is inactive.
    """
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if password and not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user
