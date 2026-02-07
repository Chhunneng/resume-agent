"""RBAC caching service for fast permission checks."""

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import Role


class RBACCache:
    """
    In-memory cache for roles and permissions.

    Uses Sets for O(1) permission lookups instead of O(n) list searches.
    """

    def __init__(self):
        # Cache structure:
        # role_permissions: {role_name: set(permission_strings)}
        # all_permissions: set(all_permission_strings)
        # role_names: set(all_role_names)
        # default_roles: set(default_role_names)
        # permission_to_roles: {permission_string: set(role_names)} - reverse lookup
        self._role_permissions: dict[str, set[str]] = {}
        self._all_permissions: set[str] = set()
        self._role_names: set[str] = set()
        self._default_roles: set[str] = set()
        self._permission_to_roles: dict[str, set[str]] = {}
        self._is_loaded = False

    async def load_from_db(self, session: AsyncSession) -> None:
        """
        Load all roles and permissions from database into cache.

        Args:
            session: Database session.
        """
        # Load all roles with permissions
        result = await session.exec(
            select(Role).options(selectinload(Role.permissions)),
        )
        roles = result.scalars().all()

        # Reset cache
        self._role_permissions.clear()
        self._all_permissions.clear()
        self._role_names.clear()
        self._default_roles.clear()
        self._permission_to_roles.clear()

        for role in roles:
            role_name = role.name
            self._role_names.add(role_name)

            if role.is_default:
                self._default_roles.add(role_name)

            # Get permission strings for this role
            permission_strings = {f"{perm.resource}:{perm.action}" for perm in role.permissions}

            self._role_permissions[role_name] = permission_strings
            self._all_permissions.update(permission_strings)

            # Build reverse lookup: permission -> roles
            for perm_str in permission_strings:
                if perm_str not in self._permission_to_roles:
                    self._permission_to_roles[perm_str] = set()
                self._permission_to_roles[perm_str].add(role_name)

        self._is_loaded = True

    def get_user_permissions(self, role_names: set[str]) -> set[str]:
        """
        Get all permissions for given roles (Set-based, O(1) lookup).

        Args:
            role_names: Set of role names.

        Returns:
            Set of permission strings.
        """
        permissions = set()
        for role_name in role_names:
            if role_name in self._role_permissions:
                permissions.update(self._role_permissions[role_name])
        return permissions

    def has_permission(
        self,
        role_names: set[str],
        resource: str,
        action: str,
    ) -> bool:
        """
        Check if roles have specific permission (O(1) lookup).

        Args:
            role_names: Set of role names.
            resource: Resource name.
            action: Action name.

        Returns:
            True if any role has the permission.
        """
        permission_str = f"{resource}:{action}"
        user_permissions = self.get_user_permissions(role_names)
        return permission_str in user_permissions

    def get_default_roles(self) -> set[str]:
        """
        Get set of default role names.

        Returns:
            Set of default role names.
        """
        return self._default_roles.copy()

    def invalidate(self) -> None:
        """Invalidate cache - will reload on next access."""
        self._is_loaded = False
        self._role_permissions.clear()
        self._all_permissions.clear()
        self._role_names.clear()
        self._default_roles.clear()
        self._permission_to_roles.clear()

    @property
    def is_loaded(self) -> bool:
        """
        Check if cache is loaded.

        Returns:
            True if cache is loaded, False otherwise.
        """
        return self._is_loaded


# Global cache instance
rbac_cache = RBACCache()
