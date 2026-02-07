# RBAC Setup Guide

This guide explains how to set up roles and permissions in Resume Agent.

## Overview

Resume Agent uses Role-Based Access Control (RBAC) for authorization:

- **Roles**: Collections of permissions assigned to users
- **Permissions**: Specific actions on resources (e.g., `user:read`, `post:write`)
- **Default Roles**: Automatically assigned to new users

## Permission Format

Permissions use the format: `resource:action`

### Common Resources

- `user`: User management
- `post`: Post/content management
- `admin`: Administrative actions
- `resume`: Resume management
- `job`: Job application management

### Common Actions

- `read`: View resource
- `write`: Create/update resource
- `delete`: Delete resource
- `manage`: Full management (read, write, delete)

### Examples

- `user:read`: Can view users
- `user:write`: Can create/update users
- `user:delete`: Can delete users
- `user:manage`: Can do all user operations
- `post:read`: Can view posts
- `post:write`: Can create/update posts

## Setting Up Roles and Permissions

### Step 1: Create Permissions

First, create the permissions you need. Permissions are stored in the database.

**Example: Creating Permissions via Database**

```sql
INSERT INTO permission (name, description, resource, action) VALUES
('user:read', 'Read user information', 'user', 'read'),
('user:write', 'Create or update users', 'user', 'write'),
('user:delete', 'Delete users', 'user', 'delete'),
('post:read', 'Read posts', 'post', 'read'),
('post:write', 'Create or update posts', 'post', 'write');
```

**Example: Creating Permissions via Python**

```python
from src.database import AsyncSessionLocal
from src.auth.models import Permission

async def create_permissions():
    async with AsyncSessionLocal() as session:
        permissions = [
            Permission(
                name="user:read",
                description="Read user information",
                resource="user",
                action="read"
            ),
            Permission(
                name="user:write",
                description="Create or update users",
                resource="user",
                action="write"
            ),
            Permission(
                name="user:delete",
                description="Delete users",
                resource="user",
                action="delete"
            ),
        ]
        
        session.add_all(permissions)
        await session.commit()
```

### Step 2: Create Roles

Create roles and assign permissions to them.

**Example: Creating Roles via Database**

```sql
-- Create admin role
INSERT INTO role (name, description, is_default) VALUES
('admin', 'Administrator with full access', false);

-- Create user role (default)
INSERT INTO role (name, description, is_default) VALUES
('user', 'Regular user with basic access', true);

-- Assign permissions to admin role
INSERT INTO role_permission (role_id, permission_id)
SELECT r.id, p.id
FROM role r, permission p
WHERE r.name = 'admin'
AND p.name IN ('user:read', 'user:write', 'user:delete', 'post:read', 'post:write');

-- Assign permissions to user role
INSERT INTO role_permission (role_id, permission_id)
SELECT r.id, p.id
FROM role r, permission p
WHERE r.name = 'user'
AND p.name IN ('user:read', 'post:read');
```

**Example: Creating Roles via Python**

```python
from src.database import AsyncSessionLocal
from src.auth.models import Role, Permission
from sqlalchemy import select

async def create_roles():
    async with AsyncSessionLocal() as session:
        # Get permissions
        result = await session.exec(
            select(Permission).where(Permission.name.in_([
                'user:read', 'user:write', 'user:delete',
                'post:read', 'post:write'
            ]))
        )
        permissions = {p.name: p for p in result.scalars().all()}
        
        # Create admin role
        admin_role = Role(
            name='admin',
            description='Administrator with full access',
            is_default=False,
            permissions=[
                permissions['user:read'],
                permissions['user:write'],
                permissions['user:delete'],
                permissions['post:read'],
                permissions['post:write']
            ]
        )
        
        # Create user role (default)
        user_role = Role(
            name='user',
            description='Regular user with basic access',
            is_default=True,
            permissions=[
                permissions['user:read'],
                permissions['post:read']
            ]
        )
        
        session.add_all([admin_role, user_role])
        await session.commit()
```

### Step 3: Assign Roles to Users

Assign roles to existing users.

**Example: Assigning Roles via Database**

```sql
-- Assign admin role to user
INSERT INTO user_role (user_id, role_id)
SELECT u.id, r.id
FROM user u, role r
WHERE u.email = 'admin@example.com'
AND r.name = 'admin';
```

**Example: Assigning Roles via Python**

```python
from src.database import AsyncSessionLocal
from src.auth.models import User, Role
from sqlalchemy import select

async def assign_role_to_user(user_email: str, role_name: str):
    async with AsyncSessionLocal() as session:
        # Get user
        result = await session.exec(
            select(User).where(User.email == user_email)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise ValueError(f"User {user_email} not found")
        
        # Get role
        result = await session.exec(
            select(Role).where(Role.name == role_name)
        )
        role = result.scalar_one_or_none()
        
        if not role:
            raise ValueError(f"Role {role_name} not found")
        
        # Assign role
        if role not in user.roles:
            user.roles.append(role)
            await session.commit()
```

## Default Roles

Roles marked with `is_default=True` are automatically assigned to new users during registration.

### Setting a Role as Default

**Via Database:**

```sql
UPDATE role SET is_default = true WHERE name = 'user';
```

**Via Python:**

```python
from src.database import AsyncSessionLocal
from src.auth.models import Role
from sqlalchemy import select

async def set_default_role(role_name: str):
    async with AsyncSessionLocal() as session:
        result = await session.exec(
            select(Role).where(Role.name == role_name)
        )
        role = result.scalar_one_or_none()
        
        if role:
            role.is_default = True
            await session.commit()
```

## Using Roles and Permissions in Code

### Check User Role

```python
from fastapi import Depends
from src.auth import get_current_active_user, require_role, User

@router.get("/admin-only")
async def admin_route(
    current_user: User = Depends(require_role("admin"))
):
    return {"message": "Admin access granted"}
```

### Check User Permission

```python
from src.auth import require_permission

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_permission("user", "delete"))
):
    # Delete user logic
    return {"message": f"User {user_id} deleted"}
```

### Check Multiple Permissions

```python
from src.auth import require_any_permission, require_all_permissions

# Require any of the permissions
@router.get("/content")
async def get_content(
    current_user: User = Depends(
        require_any_permission([
            ("content", "read"),
            ("content", "write")
        ])
    )
):
    return {"content": "..."}

# Require all permissions
@router.post("/users")
async def create_user(
    current_user: User = Depends(
        require_all_permissions([
            ("user", "read"),
            ("user", "write")
        ])
    )
):
    # Create user logic
    return {"message": "User created"}
```

## Cache Management

The RBAC system uses an in-memory cache for fast permission checks. The cache automatically invalidates when roles or permissions change.

### Manual Cache Refresh

If you need to manually refresh the cache:

```python
from src.auth import refresh_rbac_cache
from src.database import get_db_session

async with get_db_session() as session:
    await refresh_rbac_cache(session)
```

## Common Role Patterns

### Admin Role

Full access to all resources:

```python
admin_permissions = [
    ("user", "manage"),
    ("post", "manage"),
    ("admin", "manage")
]
```

### Moderator Role

Can read and write, but not delete:

```python
moderator_permissions = [
    ("user", "read"),
    ("post", "read"),
    ("post", "write")
]
```

### User Role

Basic read-only access:

```python
user_permissions = [
    ("user", "read"),
    ("post", "read")
]
```

## Best Practices

1. **Use Permissions, Not Roles**: Check permissions in code, not roles
2. **Default Roles**: Always have at least one default role for new users
3. **Least Privilege**: Give users only the permissions they need
4. **Document Permissions**: Document what each permission allows
5. **Test Permissions**: Test that permission checks work correctly

## Troubleshooting

### Cache Not Updating

If permission changes aren't taking effect:

1. Check that cache invalidation is working
2. Manually refresh the cache
3. Restart the application

### Permissions Not Working

1. Verify permissions exist in database
2. Check that roles have the correct permissions
3. Verify users have the correct roles
4. Check cache is loaded

## Related Documentation

- [Auth System Deep Dive](../../backend/docs/auth-system.md) - Technical details
- [Authentication Guide](authentication.md) - Using authentication
- [Caching Strategy](../architecture/caching.md) - How caching works
- [Database Schema](../architecture/database-schema.md) - Database structure

