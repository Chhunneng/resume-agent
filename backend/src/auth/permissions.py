"""Permission checking utilities for role-based access control."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import User


def has_permission(user: "User", resource: str, action: str) -> bool:
    """
    Check if user has a specific permission (uses cache if available).

    Args:
        user: User model instance.
        resource: Resource name (e.g., "user", "post").
        action: Action name (e.g., "read", "write", "delete").

    Returns:
        True if user has the permission, False otherwise.
    """
    return user.has_permission_cached(resource, action)


def has_any_permission(user: "User", permissions: list[tuple[str, str]]) -> bool:
    """
    Check if user has any of the specified permissions (uses cache if available).

    Args:
        user: User model instance.
        permissions: List of (resource, action) tuples.

    Returns:
        True if user has any of the permissions, False otherwise.
    """
    return any(user.has_permission_cached(resource, action) for resource, action in permissions)


def has_all_permissions(user: "User", permissions: list[tuple[str, str]]) -> bool:
    """
    Check if user has all of the specified permissions (uses cache if available).

    Args:
        user: User model instance.
        permissions: List of (resource, action) tuples.

    Returns:
        True if user has all of the permissions, False otherwise.
    """
    return all(user.has_permission_cached(resource, action) for resource, action in permissions)


def has_role_name(user: "User", role_name: str) -> bool:
    """
    Check if user has a specific role by name.

    Args:
        user: User model instance.
        role_name: Role name to check.

    Returns:
        True if user has the role, False otherwise.
    """
    return user.has_role_name(role_name)


def has_any_role_name(user: "User", role_names: list[str]) -> bool:
    """
    Check if user has any of the specified roles.

    Args:
        user: User model instance.
        role_names: List of role names to check.

    Returns:
        True if user has any of the roles, False otherwise.
    """
    return any(user.has_role_name(role_name) for role_name in role_names)
