"""Authentication dependencies for FastAPI routes."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database.connection import get_db_session

from .jwt import TokenType, verify_token
from .models import User
from .permissions import (
    has_all_permissions,
    has_any_permission,
    has_any_role_name,
    has_permission,
    has_role_name,
)

# HTTP Bearer token security scheme
security = HTTPBearer()


def _raise_auth_error(detail: str = "Invalid authentication credentials") -> None:
    """
    Raise HTTP 401 authentication error.

    Args:
        detail: Error detail message.

    Raises:
        HTTPException: With 401 status code.
    """
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def _raise_forbidden_error(detail: str) -> None:
    """
    Raise HTTP 403 forbidden error.

    Args:
        detail: Error detail message.

    Raises:
        HTTPException: With 403 status code.
    """
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail,
    )


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> User:
    """
    Dependency to get the current authenticated user from JWT token.

    Loads user with roles and permissions eagerly loaded.

    Args:
        credentials: HTTP Bearer token credentials.
        session: Database session.

    Returns:
        Current authenticated user with roles loaded.

    Raises:
        HTTPException: If token is invalid or user not found.
    """
    token = credentials.credentials

    try:
        payload = verify_token(token, token_type=TokenType.ACCESS)
        user_id = int(payload.get("sub"))
    except (ValueError, KeyError):
        _raise_auth_error()

    # Get user from database with roles loaded (permissions come from cache)
    result = await session.exec(
        select(User).where(User.id == user_id).options(selectinload(User.roles)),
    )
    user = result.scalar_one_or_none()

    if user is None:
        _raise_auth_error("User not found")

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Dependency to get the current active user.

    Args:
        current_user: Current authenticated user.

    Returns:
        Current active user.

    Raises:
        HTTPException: If user is not active.
    """
    if not current_user.is_active:
        _raise_forbidden_error("Inactive user")

    return current_user


def require_role(required_role: str):
    """
    Dependency factory for role-based access control.

    Args:
        required_role: Required role name.

    Returns:
        Dependency function that checks if user has the required role.
    """

    async def role_checker(
        current_user: Annotated[User, Depends(get_current_active_user)],
    ) -> User:
        """
        Check if user has the required role.

        Args:
            current_user: Current active user.

        Returns:
            Current user if authorized.

        Raises:
            HTTPException: If user doesn't have the required role.
        """
        if not has_role_name(current_user, required_role):
            _raise_forbidden_error(f"User does not have required role: {required_role}")

        return current_user

    return role_checker


def require_any_role(required_roles: list[str]):
    """
    Dependency factory for role-based access control with multiple allowed roles.

    Args:
        required_roles: List of allowed role names.

    Returns:
        Dependency function that checks if user has any of the required roles.
    """

    async def role_checker(
        current_user: Annotated[User, Depends(get_current_active_user)],
    ) -> User:
        """
        Check if user has any of the required roles.

        Args:
            current_user: Current active user.

        Returns:
            Current user if authorized.

        Raises:
            HTTPException: If user doesn't have any of the required roles.
        """
        if not has_any_role_name(current_user, required_roles):
            _raise_forbidden_error(
                f"User does not have any of the required roles: {required_roles}",
            )

        return current_user

    return role_checker


def require_permission(resource: str, action: str):
    """
    Dependency factory for permission-based access control.

    Args:
        resource: Resource name (e.g., "user", "post").
        action: Action name (e.g., "read", "write", "delete").

    Returns:
        Dependency function that checks if user has the required permission.
    """

    async def permission_checker(
        current_user: Annotated[User, Depends(get_current_active_user)],
    ) -> User:
        """
        Check if user has the required permission.

        Args:
            current_user: Current active user.

        Returns:
            Current user if authorized.

        Raises:
            HTTPException: If user doesn't have the required permission.
        """
        if not has_permission(current_user, resource, action):
            _raise_forbidden_error(
                f"User does not have required permission: {resource}:{action}",
            )

        return current_user

    return permission_checker


def require_any_permission(permissions: list[tuple[str, str]]):
    """
    Dependency factory for permission-based access control with multiple allowed permissions.

    Args:
        permissions: List of (resource, action) tuples.

    Returns:
        Dependency function that checks if user has any of the required permissions.
    """

    async def permission_checker(
        current_user: Annotated[User, Depends(get_current_active_user)],
    ) -> User:
        """
        Check if user has any of the required permissions.

        Args:
            current_user: Current active user.

        Returns:
            Current user if authorized.

        Raises:
            HTTPException: If user doesn't have any of the required permissions.
        """
        if not has_any_permission(current_user, permissions):
            _raise_forbidden_error(
                "User does not have any of the required permissions",
            )

        return current_user

    return permission_checker


def require_all_permissions(permissions: list[tuple[str, str]]):
    """
    Dependency factory for permission-based access control requiring all permissions.

    Args:
        permissions: List of (resource, action) tuples.

    Returns:
        Dependency function that checks if user has all of the required permissions.
    """

    async def permission_checker(
        current_user: Annotated[User, Depends(get_current_active_user)],
    ) -> User:
        """
        Check if user has all of the required permissions.

        Args:
            current_user: Current active user.

        Returns:
            Current user if authorized.

        Raises:
            HTTPException: If user doesn't have all of the required permissions.
        """
        if not has_all_permissions(current_user, permissions):
            _raise_forbidden_error(
                "User does not have all of the required permissions",
            )

        return current_user

    return permission_checker
