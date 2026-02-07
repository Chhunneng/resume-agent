"""Authentication module."""

from .cache import rbac_cache
from .cache_manager import refresh_rbac_cache
from .dependencies import (
    get_current_active_user,
    get_current_user,
    require_all_permissions,
    require_any_permission,
    require_any_role,
    require_permission,
    require_role,
)
from .jwt import TokenType
from .models import Permission, Role, User
from .router import router

__all__ = [
    "router",
    "User",
    "Role",
    "Permission",
    "TokenType",
    "get_current_user",
    "get_current_active_user",
    "require_role",
    "require_any_role",
    "require_permission",
    "require_any_permission",
    "require_all_permissions",
    "rbac_cache",
    "refresh_rbac_cache",
]
