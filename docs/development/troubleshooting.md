# Troubleshooting Guide

Common issues and solutions for Resume Agent development.

## Database Issues

### Connection Errors

**Problem:** Cannot connect to database

**Solutions:**
1. Verify database is running:
   ```bash
   docker compose ps
   ```

2. Check database credentials in `.env`:
   ```env
   POSTGRES_HOST=postgres  # Use 'postgres' in Docker, 'localhost' manually
   POSTGRES_PORT=5432
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_password
   ```

3. Test connection:
   ```bash
   docker compose exec postgres psql -U postgres -d resume_agent
   ```

### Migration Errors

**Problem:** Migrations fail or are out of sync

**Solutions:**
1. Check current migration status:
   ```bash
   alembic current
   ```

2. Check migration history:
   ```bash
   alembic history
   ```

3. Reset database (development only):
   ```bash
   # Drop and recreate database
   docker compose down -v
   docker compose up -d
   alembic upgrade head
   ```

4. Create new migration:
   ```bash
   alembic revision --autogenerate -m "description"
   ```

## Authentication Issues

### Token Errors

**Problem:** "Invalid authentication credentials"

**Solutions:**
1. Check token is included in request:
   ```http
   Authorization: Bearer <token>
   ```

2. Verify token hasn't expired (access tokens expire after 15 minutes)

3. Refresh the token:
   ```http
   POST /v1/auth/refresh
   {
     "refresh_token": "<refresh_token>"
   }
   ```

### Permission Errors

**Problem:** "User does not have required permission"

**Solutions:**
1. Check user roles:
   ```python
   user = await get_user(user_id)
   print(user.get_role_names())
   ```

2. Verify permissions are assigned to roles

3. Check RBAC cache is loaded:
   ```python
   from src.auth.cache import rbac_cache
   print(rbac_cache.is_loaded)
   ```

4. Refresh cache if needed:
   ```python
   from src.auth import refresh_rbac_cache
   await refresh_rbac_cache(session)
   ```

## Docker Issues

### Container Won't Start

**Problem:** Docker container fails to start

**Solutions:**
1. Check logs:
   ```bash
   docker compose logs backend
   ```

2. Rebuild containers:
   ```bash
   docker compose up --build
   ```

3. Check port conflicts:
   ```bash
   lsof -i :8000  # Check if port is in use
   ```

### Hot Reload Not Working

**Problem:** Code changes don't reload

**Solutions:**
1. Verify volume mounts in `docker-compose.dev.yml`

2. Check file permissions

3. Restart container:
   ```bash
   docker compose restart backend-dev
   ```

## Environment Variables

### Missing Variables

**Problem:** Application fails with missing environment variable error

**Solutions:**
1. Check `.env` file exists:
   ```bash
   ls backend/.env
   ```

2. Verify all required variables are set:
   ```env
   JWT_SECRET=required
   POSTGRES_PASSWORD=required
   ```

3. Restart application after changing `.env`

## Import Errors

### Module Not Found

**Problem:** `ModuleNotFoundError` or `ImportError`

**Solutions:**
1. Verify Python path:
   ```python
   import sys
   print(sys.path)
   ```

2. Check imports use correct paths:
   ```python
   from src.auth import User  # Correct
   from auth import User  # Wrong
   ```

3. Install dependencies:
   ```bash
   pipenv install
   ```

## Test Issues

### Tests Fail

**Problem:** Tests fail unexpectedly

**Solutions:**
1. Run tests with verbose output:
   ```bash
   pytest -v
   ```

2. Run specific test:
   ```bash
   pytest tests/test_specific.py::test_function -v
   ```

3. Check test database setup

4. Verify fixtures are working

### Database in Tests

**Problem:** Tests interfere with each other

**Solutions:**
1. Use test database:
   ```python
   @pytest.fixture
   async def test_db():
       # Use separate test database
       pass
   ```

2. Clean up after tests:
   ```python
   @pytest.fixture(autouse=True)
   async def cleanup():
       yield
       # Cleanup code
   ```

## Performance Issues

### Slow Queries

**Problem:** Database queries are slow

**Solutions:**
1. Check database indexes:
   ```sql
   \d+ table_name  -- Show indexes
   ```

2. Use query logging:
   ```python
   # In database/connection.py
   engine = create_async_engine(..., echo=True)
   ```

3. Optimize queries:
   - Use `selectinload` for relationships
   - Avoid N+1 queries
   - Use database indexes

### Cache Issues

**Problem:** RBAC cache not working

**Solutions:**
1. Check cache is loaded:
   ```python
   from src.auth.cache import rbac_cache
   print(rbac_cache.is_loaded)
   ```

2. Manually refresh cache:
   ```python
   from src.auth import refresh_rbac_cache
   await refresh_rbac_cache(session)
   ```

3. Check cache invalidation is working

## Logging

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### View Application Logs

```bash
# Docker
docker compose logs -f backend

# Manual
# Logs appear in console when running uvicorn
```

## Common Error Messages

### "Invalid email or password"

- Check email and password are correct
- Verify user exists in database
- Check password hashing

### "User account is inactive"

- Check `user.is_active` is `True`
- Activate user account

### "Email already registered"

- User with this email already exists
- Use different email or login instead

### "Token has expired"

- Access token expired (15 minutes)
- Use refresh token to get new access token

## Getting Help

If you can't resolve an issue:

1. Check [API Examples](../api/examples.md)
2. Review [Architecture Documentation](../architecture/overview.md)
3. Check application logs
4. Open an issue on the repository with:
   - Error message
   - Steps to reproduce
   - Environment details
   - Relevant logs

## Related Documentation

- [Development Setup](setup.md) - Environment setup
- [Testing Guide](testing.md) - Testing practices
- [Coding Standards](coding-standards.md) - Code guidelines

