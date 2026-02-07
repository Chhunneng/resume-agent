# Authentication System

## Overview

The Resume Agent authentication system provides secure, scalable authentication and authorization using:

- **JWT (JSON Web Tokens)** for stateless authentication
- **Role-Based Access Control (RBAC)** for flexible permission management
- **In-memory caching** for fast permission checks
- **Password hashing** using secure algorithms

## Key Features

- JWT-based authentication with access and refresh tokens
- Role-based access control (RBAC)
- Permission-based authorization
- Automatic cache invalidation on role/permission changes
- Fast O(1) permission lookups using in-memory cache
- Default roles for new users

## Architecture

### Components

1. **JWT Token Management** (`auth/jwt.py`)
   - Access token creation and verification
   - Refresh token creation and verification
   - Token expiration handling

2. **User Management** (`auth/models.py`)
   - User model with profile information
   - Password hashing and verification
   - User-role relationships

3. **Role and Permission System** (`auth/models.py`)
   - Role model with default role support
   - Permission model with resource:action format
   - Many-to-many relationships

4. **RBAC Cache** (`auth/cache.py`)
   - In-memory cache for roles and permissions
   - Fast permission lookups (O(1))
   - Automatic cache invalidation

5. **Permission Checking** (`auth/permissions.py`)
   - Permission validation utilities
   - Role checking utilities

6. **FastAPI Dependencies** (`auth/dependencies.py`)
   - `get_current_user`: Get authenticated user from JWT
   - `get_current_active_user`: Get active user only
   - `require_role`: Require specific role
   - `require_any_role`: Require any of multiple roles
   - `require_permission`: Require specific permission
   - `require_any_permission`: Require any of multiple permissions
   - `require_all_permissions`: Require all specified permissions

## JWT Token Structure

### Access Token

Access tokens are short-lived (default: 15 minutes) and contain:

```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "roles": ["user", "admin"],
  "type": "access",
  "iat": 1234567890,
  "exp": 1234568790
}
```

**Fields:**
- `sub`: User ID (subject)
- `email`: User email address
- `roles`: List of role names assigned to user
- `type`: Token type ("access")
- `iat`: Issued at timestamp
- `exp`: Expiration timestamp

### Refresh Token

Refresh tokens are long-lived (default: 30 days) and contain:

```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "type": "refresh",
  "iat": 1234567890,
  "exp": 1234567890
}
```

**Fields:**
- `sub`: User ID (subject)
- `email`: User email address
- `type`: Token type ("refresh")
- `iat`: Issued at timestamp
- `exp`: Expiration timestamp

**Note:** Refresh tokens do NOT contain roles. Roles are loaded from the database when refreshing access tokens.

## Database Models

### User Model

```python
class User(BaseModel, table=True):
    id: int
    email: str  # Unique
    password_hash: str
    firstname: str
    lastname: str
    phone_number: str | None
    registration_date: datetime
    last_login: datetime | None
    is_active: bool
    street_address: str | None
    city: str | None
    state: str | None
    zip_code: str | None
    country: str | None
    roles: list[Role]  # Many-to-many relationship
```

### Role Model

```python
class Role(BaseModel, table=True):
    id: int
    name: str  # Unique
    description: str | None
    is_default: bool  # Assigned to new users
    permissions: list[Permission]  # Many-to-many relationship
    users: list[User]  # Many-to-many relationship
```

### Permission Model

```python
class Permission(BaseModel, table=True):
    id: int
    name: str  # Unique
    description: str | None
    resource: str  # e.g., "user", "post", "admin"
    action: str  # e.g., "read", "write", "delete", "manage"
    roles: list[Role]  # Many-to-many relationship
```

### Relationships

- **User ↔ Role**: Many-to-many (via `user_role` junction table)
- **Role ↔ Permission**: Many-to-many (via `role_permission` junction table)

## RBAC Cache System

The RBAC cache provides fast permission lookups by caching all roles and permissions in memory.

### Cache Structure

```python
{
    "role_permissions": {
        "admin": {"user:read", "user:write", "user:delete", ...},
        "user": {"user:read", "post:read", ...}
    },
    "all_permissions": {"user:read", "user:write", ...},
    "role_names": {"admin", "user", "moderator"},
    "default_roles": {"user"},
    "permission_to_roles": {
        "user:read": {"admin", "user"},
        "user:write": {"admin"}
    }
}
```

### Cache Benefits

- **O(1) permission lookups** instead of O(n) database queries
- **Automatic invalidation** when roles/permissions change
- **Fast user permission checks** without database access

### Cache Lifecycle

1. **Initialization**: Cache loads on application startup
2. **Usage**: Permission checks use cache (O(1) lookup)
3. **Invalidation**: Cache invalidates automatically on:
   - Role insert/update/delete
   - Permission insert/update/delete
   - Role-permission relationship changes
4. **Reload**: Cache reloads on next access after invalidation

## API Endpoints

### Authentication Endpoints

All endpoints are under `/v1/auth/`:

#### Register

```http
POST /v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password",
  "firstname": "John",
  "lastname": "Doe",
  "phone_number": "+1234567890",
  "street_address": "123 Main St",
  "city": "New York",
  "state": "NY",
  "zip_code": "10001",
  "country": "USA"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

#### Login

```http
POST /v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

#### Refresh Token

```http
POST /v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ..."
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

#### Get Current User

```http
GET /v1/auth/me
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "firstname": "John",
  "lastname": "Doe",
  "phone_number": "+1234567890",
  "registration_date": "2024-01-01T00:00:00Z",
  "last_login": "2024-01-02T00:00:00Z",
  "is_active": true,
  "street_address": "123 Main St",
  "city": "New York",
  "state": "NY",
  "zip_code": "10001",
  "country": "USA"
}
```

## Using Authentication in Routes

### Basic Authentication

Require a user to be authenticated:

```python
from fastapi import APIRouter, Depends
from src.auth import get_current_active_user, User

router = APIRouter()

@router.get("/protected")
async def protected_route(
    current_user: User = Depends(get_current_active_user)
):
    return {"message": f"Hello, {current_user.email}!"}
```

### Role-Based Access Control

Require a specific role:

```python
from src.auth import require_role, User

@router.get("/admin-only")
async def admin_route(
    current_user: User = Depends(require_role("admin"))
):
    return {"message": "Admin access granted"}
```

Require any of multiple roles:

```python
from src.auth import require_any_role

@router.get("/moderator-or-admin")
async def moderator_route(
    current_user: User = Depends(require_any_role(["admin", "moderator"]))
):
    return {"message": "Moderator or admin access granted"}
```

### Permission-Based Access Control

Require a specific permission:

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

Require any of multiple permissions:

```python
from src.auth import require_any_permission

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
```

Require all specified permissions:

```python
from src.auth import require_all_permissions

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

## Configuration

### Environment Variables

Authentication configuration is loaded from environment variables:

```env
# JWT Configuration
JWT_ALG=HS256                    # JWT algorithm (default: HS256)
JWT_SECRET=your_secret_key       # Secret for access tokens (required)
JWT_EXP=00:15:00.000000                       # Access token expiration in minutes (default: 15)

# Refresh Token Configuration
JWT_REFRESH_TOKEN_EXP=30d,00:00:00.000000                     # Refresh token expiration in days (default: 30)

# Cookie Configuration
SECURE_COOKIES=true              # Use secure cookies (default: true)
```

### Security Best Practices

1. **Use strong secrets**: Generate strong, random secrets for JWT tokens
2. **Keep tokens short-lived**: Access tokens should expire quickly (15 minutes)
3. **Use HTTPS**: Always use HTTPS in production
4. **Rotate secrets**: Regularly rotate JWT secrets
5. **Validate tokens**: Always validate tokens on the server side

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

## Default Roles

New users are automatically assigned default roles. Roles marked with `is_default=True` are assigned to new users during registration.

To set up default roles:

1. Create roles in the database
2. Mark roles as default (`is_default=True`)
3. Assign permissions to roles
4. New users will automatically receive these roles

## Cache Management

### Manual Cache Refresh

If you need to manually refresh the cache:

```python
from src.auth import refresh_rbac_cache
from src.database import get_db_session

async with get_db_session() as session:
    await refresh_rbac_cache(session)
```

### Cache Status

Check if cache is loaded:

```python
from src.auth.cache import rbac_cache

if rbac_cache.is_loaded:
    print("Cache is loaded")
else:
    print("Cache needs to be loaded")
```

## Error Handling

### Authentication Errors

- **401 Unauthorized**: Invalid or missing token
- **403 Forbidden**: User lacks required role/permission or user is inactive

### Common Error Responses

```json
{
  "detail": "Invalid email or password"
}
```

```json
{
  "detail": "User does not have required role: admin"
}
```

```json
{
  "detail": "User does not have required permission: user:delete"
}
```

```json
{
  "detail": "User account is inactive"
}
```

## Testing

See [Testing Guide](testing.md) for information on testing authentication.

## Related Documentation

- [Authentication Guide](../../docs/guides/authentication.md) - User-facing auth guide
- [RBAC Setup Guide](../../docs/guides/rbac-setup.md) - Setting up roles and permissions
- [Authentication Architecture](../../docs/architecture/authentication.md) - Auth flow diagrams
- [API Authentication Documentation](../../docs/api/authentication.md) - API endpoint details

