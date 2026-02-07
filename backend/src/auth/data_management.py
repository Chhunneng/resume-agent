"""Data export/import utilities for roles and permissions."""

import json
from pathlib import Path

from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from .cache_manager import refresh_rbac_cache
from .models import Permission, Role, role_permission, user_role


async def export_roles_permissions(
    session: AsyncSession,
    output_path: Path | str,
) -> None:
    """
    Export all roles and permissions to JSON file.

    Args:
        session: Database session.
        output_path: Path to output JSON file.
    """
    # Load all roles with permissions
    result = await session.exec(
        select(Role).options(selectinload(Role.permissions)),
    )
    roles = result.scalars().all()

    # Load all permissions
    perm_result = await session.exec(select(Permission))
    permissions = perm_result.scalars().all()

    # Build export data
    export_data = {
        "permissions": [
            {
                "name": perm.name,
                "resource": perm.resource,
                "action": perm.action,
                "description": perm.description,
            }
            for perm in permissions
        ],
        "roles": [
            {
                "name": role.name,
                "description": role.description,
                "is_default": role.is_default,
                "permissions": [f"{perm.resource}:{perm.action}" for perm in role.permissions],
            }
            for role in roles
        ],
    }

    # Write to file
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    print(
        f"Exported {len(permissions)} permissions and {len(roles)} roles to {output_path}",
    )


async def _clear_existing_data(session: AsyncSession) -> None:
    """
    Clear existing roles and permissions from database.

    Args:
        session: Database session.
    """
    await session.exec(delete(role_permission))
    await session.exec(delete(user_role))
    await session.exec(delete(Role))
    await session.exec(delete(Permission))
    await session.commit()


async def _load_permission_by_string(
    session: AsyncSession,
    permission_string: str,
) -> Permission | None:
    """
    Load permission from database by resource:action string.

    Args:
        session: Database session.
        permission_string: Permission string in format "resource:action".

    Returns:
        Permission object if found, None otherwise.
    """
    resource, action = permission_string.split(":")
    result = await session.exec(
        select(Permission).where(
            Permission.resource == resource,
            Permission.action == action,
        ),
    )
    return result.scalar_one_or_none()


async def _import_permissions(
    session: AsyncSession,
    permissions_data: list[dict],
) -> dict[str, Permission]:
    """
    Import permissions from data.

    Args:
        session: Database session.
        permissions_data: List of permission dictionaries.

    Returns:
        Dictionary mapping permission names to Permission objects.
    """
    permission_map: dict[str, Permission] = {}

    for perm_data in permissions_data:
        # Check if permission exists
        result = await session.exec(
            select(Permission).where(Permission.name == perm_data["name"]),
        )
        existing = result.scalar_one_or_none()

        if existing:
            # Update existing
            existing.resource = perm_data["resource"]
            existing.action = perm_data["action"]
            existing.description = perm_data.get("description")
            permission_map[perm_data["name"]] = existing
        else:
            # Create new
            new_perm = Permission(
                name=perm_data["name"],
                resource=perm_data["resource"],
                action=perm_data["action"],
                description=perm_data.get("description"),
            )
            session.add(new_perm)
            permission_map[perm_data["name"]] = new_perm

    await session.commit()
    return permission_map


async def _import_roles(
    session: AsyncSession,
    roles_data: list[dict],
) -> None:
    """
    Import roles from data.

    Args:
        session: Database session.
        roles_data: List of role dictionaries.
    """
    for role_data in roles_data:
        # Check if role exists
        result = await session.exec(
            select(Role).where(Role.name == role_data["name"]),
        )
        existing = result.scalar_one_or_none()

        # Get permissions for this role
        role_permissions = []
        for perm_str in role_data.get("permissions", []):
            perm = await _load_permission_by_string(session, perm_str)
            if perm:
                role_permissions.append(perm)

        if existing:
            # Update existing
            existing.description = role_data.get("description")
            existing.is_default = role_data.get("is_default", False)
            existing.permissions = role_permissions
        else:
            # Create new
            new_role = Role(
                name=role_data["name"],
                description=role_data.get("description"),
                is_default=role_data.get("is_default", False),
                permissions=role_permissions,
            )
            session.add(new_role)

    await session.commit()


async def import_roles_permissions(
    session: AsyncSession,
    input_path: Path | str,
    clear_existing: bool = False,
) -> None:
    """
    Import roles and permissions from JSON file.

    Args:
        session: Database session.
        input_path: Path to input JSON file.
        clear_existing: If True, clear existing roles/permissions first.
    """
    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Import file not found: {input_path}")

    with open(input_path, encoding="utf-8") as f:
        import_data = json.load(f)

    # Clear existing if requested
    if clear_existing:
        await _clear_existing_data(session)

    # Import permissions first
    await _import_permissions(session, import_data.get("permissions", []))

    # Import roles
    await _import_roles(session, import_data.get("roles", []))

    # Refresh cache
    await refresh_rbac_cache(session)

    print(f"Imported roles and permissions from {input_path}")
