"""Authentication database models."""

from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

from src.database.base import AutoIDBaseModel


class RolePermission(SQLModel, table=True):
    """
    Role-Permission many-to-many relationship model.
    """

    __tablename__ = "role_permission"
    role_id: int = Field(foreign_key="role.id", primary_key=True, ondelete="CASCADE")
    permission_id: int = Field(foreign_key="permission.id", primary_key=True, ondelete="CASCADE")

    role: "Role" = Relationship(back_populates="permission_links")
    permission: "Permission" = Relationship(back_populates="role_links")


class Permission(AutoIDBaseModel, table=True):
    """
    Permission database model.

    Represents a permission that can be assigned to roles.
    Permissions are defined by resource and action (e.g., "user:read", "post:write").
    """

    __tablename__ = "permission"

    name: str = Field(
        index=True,
        max_length=100,
        nullable=False,
        unique=True,
    )
    description: str | None = Field(
        default=None,
        max_length=255,
        nullable=True,
    )
    resource: str = Field(
        max_length=50,
        nullable=False,
        description="Resource name (e.g., 'user', 'post', 'admin', 'resume')",
    )
    action: str = Field(
        max_length=50,
        nullable=False,
        description="Action name (e.g., 'read', 'create', 'update', 'delete', 'manage')",
    )

    # Many-to-many relationship with Role
    roles: list["Role"] = Relationship(
        back_populates="permissions",
        link_model=RolePermission,
    )

    role_links: list[RolePermission] = Relationship(
        back_populates="permission", passive_deletes="all"
    )


class UserRole(SQLModel, table=True):
    """
    User-Role many-to-many relationship model.
    """

    __tablename__ = "user_role"
    user_id: int = Field(foreign_key="user.id", primary_key=True, ondelete="CASCADE")
    role_id: int = Field(foreign_key="role.id", primary_key=True, ondelete="CASCADE")

    user: "User" = Relationship(back_populates="role_links")
    role: "Role" = Relationship(back_populates="user_links")


class Role(AutoIDBaseModel, table=True):
    """
    Role database model.

    Represents a role that can be assigned to users.
    Roles have permissions and can be marked as default for new users.
    """

    __tablename__ = "role"

    name: str = Field(
        index=True,
        max_length=50,
        nullable=False,
        unique=True,
    )
    description: str | None = Field(
        default=None,
        max_length=255,
        nullable=True,
    )
    is_default: bool = Field(
        default=False,
        description="Whether this role is assigned to new users by default",
    )

    # Many-to-many relationship with Permission
    permissions: list[Permission] = Relationship(
        back_populates="roles",
        link_model=RolePermission,
    )
    permission_links: list[RolePermission] = Relationship(
        back_populates="role", passive_deletes="all"
    )

    # Many-to-many relationship with User
    users: list["User"] = Relationship(
        back_populates="roles",
        link_model=UserRole,
    )
    user_links: list[UserRole] = Relationship(back_populates="role", passive_deletes="all")


class User(AutoIDBaseModel, table=True):
    """
    User database model.

    Represents a user in the system with authentication and profile information.
    Users can have multiple roles, and roles have permissions.
    """

    __tablename__ = "user"

    email: EmailStr = Field(
        sa_column=Column("email", String, unique=True, index=True, nullable=False)
    )
    password_hash: str = Field(sa_column=Column("password_hash", String(255), nullable=False))
    firstname: str = Field(sa_column=Column("firstname", String(100), nullable=False))
    lastname: str = Field(sa_column=Column("lastname", String(100), nullable=False))
    phone_number: str | None = Field(
        default=None, sa_column=Column("phone_number", String(20), nullable=True)
    )
    last_login: datetime | None = Field(default=None)
    is_active: bool = Field(default=True)
    street_address: str | None = Field(
        default=None, sa_column=Column("street_address", String(255), nullable=True)
    )
    city: str | None = Field(default=None, sa_column=Column("city", String(100), nullable=True))
    state: str | None = Field(default=None, sa_column=Column("state", String(100), nullable=True))
    zip_code: str | None = Field(
        default=None, sa_column=Column("zip_code", String(20), nullable=True)
    )
    country: str | None = Field(
        default=None, sa_column=Column("country", String(100), nullable=True)
    )

    # Many-to-many relationship with Role
    roles: list[Role] = Relationship(
        back_populates="users",
        link_model=UserRole,
    )
    role_links: list[UserRole] = Relationship(back_populates="user", passive_deletes="all")

    def get_role_names(self) -> list[str]:
        """
        Get list of role names for this user.

        Returns:
            List of role names.
        """
        return [role.name for role in self.roles]

    # def get_permissions(self) -> list[Permission]:
    #     """
    #     Get all permissions from all user's roles.

    #     Returns:
    #         List of unique permissions.
    #     """
    #     permissions_dict: dict[int, Permission] = {}
    #     for role in self.roles:
    #         for permission in role.permissions:
    #             permissions_dict[permission.id] = permission
    #     return list(permissions_dict.values())

    # def get_permission_strings(self) -> list[str]:
    #     """
    #     Get list of permission strings in format 'resource:action'.

    #     Returns:
    #         List of permission strings.
    #     """
    #     return [f"{perm.resource}:{perm.action}" for perm in self.get_permissions()]

    # def has_permission(self, resource: str, action: str) -> bool:
    #     """
    #     Check if user has a specific permission.

    #     Args:
    #         resource: Resource name.
    #         action: Action name.

    #     Returns:
    #         True if user has the permission, False otherwise.
    #     """
    #     for permission in self.get_permissions():
    #         if permission.resource == resource and permission.action == action:
    #             return True
    #     return False

    # def has_role_name(self, role_name: str) -> bool:
    #     """
    #     Check if user has a specific role by name.

    #     Args:
    #         role_name: Role name to check.

    #     Returns:
    #         True if user has the role, False otherwise.
    #     """
    #     return any(role.name == role_name for role in self.roles)

    # def get_permission_strings_cached(self) -> set[str]:
    #     """
    #     Get permission strings using cache (fast, Set-based).

    #     Returns:
    #         Set of permission strings.
    #     """
    #     from .cache import rbac_cache

    #     if not rbac_cache.is_loaded:
    #         # Cache not loaded, fallback to DB
    #         return set(self.get_permission_strings())

    #     role_names = {role.name for role in self.roles}
    #     return rbac_cache.get_user_permissions(role_names)

    # def has_permission_cached(self, resource: str, action: str) -> bool:
    #     """
    #     Check permission using cache (O(1) lookup).

    #     Args:
    #         resource: Resource name.
    #         action: Action name.

    #     Returns:
    #         True if user has permission.
    #     """
    #     from .cache import rbac_cache

    #     if not rbac_cache.is_loaded:
    #         # Cache not loaded, fallback to DB
    #         return self.has_permission(resource, action)

    #     role_names = {role.name for role in self.roles}
    #     return rbac_cache.has_permission(role_names, resource, action)
