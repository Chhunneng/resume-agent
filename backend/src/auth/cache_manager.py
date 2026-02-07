"""Cache manager with auto-refresh on DB changes."""

from sqlalchemy import event
from sqlmodel.ext.asyncio.session import AsyncSession

from .cache import rbac_cache


def setup_cache_invalidation() -> None:
    """
    Setup automatic cache invalidation on role/permission changes.

    This function sets up SQLAlchemy event listeners that automatically
    invalidate the cache whenever roles or permissions are modified.
    """
    from .models import Permission, Role, RolePermission

    @event.listens_for(Role, "after_insert")
    @event.listens_for(Role, "after_update")
    @event.listens_for(Role, "after_delete")
    def invalidate_on_role_change(*_args, **_kwargs):
        """Invalidate cache when role is inserted, updated, or deleted."""
        rbac_cache.invalidate()

    @event.listens_for(Permission, "after_insert")
    @event.listens_for(Permission, "after_update")
    @event.listens_for(Permission, "after_delete")
    def invalidate_on_permission_change(*_args, **_kwargs):
        """Invalidate cache when permission is inserted, updated, or deleted."""
        rbac_cache.invalidate()

    @event.listens_for(RolePermission, "after_insert")
    @event.listens_for(RolePermission, "after_delete")
    def invalidate_on_role_permission_change(*_args, **_kwargs):
        """Invalidate cache when role-permission relationship changes."""
        rbac_cache.invalidate()


async def initialize_rbac_cache(session: AsyncSession) -> None:
    """
    Initialize RBAC cache on application startup.

    Args:
        session: Database session.
    """
    await rbac_cache.load_from_db(session)


async def refresh_rbac_cache(session: AsyncSession) -> None:
    """
    Refresh RBAC cache from database.

    Args:
        session: Database session.
    """
    await rbac_cache.load_from_db(session)


# Setup event listeners on module import
setup_cache_invalidation()
