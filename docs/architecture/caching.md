# Caching Strategy

This document describes the caching strategy used in Resume Agent.

## Overview

Resume Agent uses an in-memory cache for RBAC (Role-Based Access Control) to provide fast permission checks without database queries.

## Cache Architecture

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

- **O(1) Permission Lookups**: Fast set-based lookups instead of O(n) database queries
- **Reduced Database Load**: Permission checks don't hit the database
- **Automatic Invalidation**: Cache invalidates when roles/permissions change
- **Fast User Permission Checks**: No database queries needed

## Cache Lifecycle

### 1. Initialization

Cache loads on application startup:

```python
async def initialize_rbac_cache(session):
    await rbac_cache.load_from_db(session)
```

### 2. Usage

Permission checks use cache:

```python
def has_permission(user, resource, action):
    return user.has_permission_cached(resource, action)
```

### 3. Invalidation

Cache invalidates automatically on:
- Role insert/update/delete
- Permission insert/update/delete
- Role-permission relationship changes

### 4. Reload

Cache reloads on next access after invalidation.

## Cache Implementation

### Loading from Database

```python
async def load_from_db(session):
    # Load all roles with permissions
    roles = await session.exec(
        select(Role).options(selectinload(Role.permissions))
    )
    
    # Build cache structure
    for role in roles:
        role_name = role.name
        permissions = {f"{p.resource}:{p.action}" for p in role.permissions}
        self._role_permissions[role_name] = permissions
```

### Permission Lookup

```python
def has_permission(role_names, resource, action):
    permission_str = f"{resource}:{action}"
    user_permissions = self.get_user_permissions(role_names)
    return permission_str in user_permissions
```

### Cache Invalidation

```python
def invalidate():
    self._is_loaded = False
    self._role_permissions.clear()
    self._all_permissions.clear()
    # ... clear all cache structures
```

## Automatic Cache Invalidation

SQLAlchemy event listeners automatically invalidate cache:

```python
@event.listens_for(Role, "after_insert")
@event.listens_for(Role, "after_update")
@event.listens_for(Role, "after_delete")
def invalidate_on_role_change(*args, **kwargs):
    rbac_cache.invalidate()
```

## Performance Characteristics

### Without Cache

- Permission check: O(n) database query
- Multiple permission checks: Multiple database queries
- High database load

### With Cache

- Permission check: O(1) set lookup
- Multiple permission checks: O(1) each
- No database load for permission checks

## Cache Fallback

If cache is not loaded, the system falls back to database queries:

```python
def has_permission_cached(self, resource, action):
    if not rbac_cache.is_loaded:
        return self.has_permission(resource, action)  # DB fallback
    return rbac_cache.has_permission(role_names, resource, action)
```

## Manual Cache Management

### Refresh Cache

```python
from src.auth import refresh_rbac_cache

async with get_db_session() as session:
    await refresh_rbac_cache(session)
```

### Check Cache Status

```python
from src.auth.cache import rbac_cache

if rbac_cache.is_loaded:
    print("Cache is loaded")
```

## Best Practices

1. **Let Cache Auto-Invalidate**: Don't manually invalidate unless necessary
2. **Monitor Cache Status**: Check if cache is loaded in production
3. **Handle Cache Misses**: Always have database fallback
4. **Test Cache Behavior**: Ensure cache works correctly in tests

## Limitations

- **In-Memory Only**: Cache is lost on application restart
- **Single Instance**: Not shared across multiple instances
- **Memory Usage**: Cache uses memory (usually minimal)

## Future Improvements

Potential enhancements:

- Redis-based distributed cache
- Cache warming on startup
- Cache metrics and monitoring
- Cache size limits

## Related Documentation

- [Auth System Deep Dive](../../backend/docs/auth-system.md) - Authentication details
- [RBAC Setup Guide](../guides/rbac-setup.md) - Setting up roles and permissions
- [Authentication Architecture](authentication.md) - Auth flow

