# Backend Testing Guide

This guide covers testing practices specific to the Resume Agent backend.

## Test Structure

### Test Organization

```
backend/tests/
├── conftest.py              # Shared fixtures
├── test_health.py           # Health check tests
└── src/
    ├── conftest.py          # Source-specific fixtures
    ├── test_models.py       # Model tests
    ├── datetime/
    │   └── test_utils.py   # Utility tests
    └── health/
        └── test_router.py  # Router tests
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=src --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/src/test_models.py
```

### Run Specific Test

```bash
pytest tests/src/test_models.py::test_user_creation
```

## Test Fixtures

### Database Fixtures

```python
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
async def db_session():
    """Create a test database session."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async_session = sessionmaker(engine, class_=AsyncSession)
    
    async with async_session() as session:
        yield session
    
    await engine.dispose()
```

### User Fixtures

```python
from src.auth.models import User
from src.auth.password import hash_password

@pytest.fixture
async def test_user(db_session: AsyncSession):
    """Create a test user."""
    user = User(
        email="test@example.com",
        password_hash=hash_password("password123"),
        firstname="Test",
        lastname="User",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user
```

## Testing Models

### User Model Tests

```python
import pytest
from src.auth.models import User

@pytest.mark.asyncio
async def test_user_creation(db_session: AsyncSession):
    """Test creating a user."""
    user = User(
        email="user@example.com",
        password_hash="hash",
        firstname="John",
        lastname="Doe"
    )
    db_session.add(user)
    await db_session.commit()
    
    assert user.id is not None
    assert user.email == "user@example.com"
    assert user.is_active is True
```

### Role and Permission Tests

```python
from src.auth.models import Role, Permission

@pytest.mark.asyncio
async def test_role_with_permissions(db_session: AsyncSession):
    """Test role with permissions."""
    permission = Permission(
        name="user:read",
        resource="user",
        action="read"
    )
    role = Role(
        name="user",
        permissions=[permission]
    )
    
    db_session.add_all([permission, role])
    await db_session.commit()
    
    assert len(role.permissions) == 1
    assert role.permissions[0].name == "user:read"
```

## Testing API Endpoints

### FastAPI TestClient

```python
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

### Authentication Tests

```python
def test_register_user():
    """Test user registration."""
    response = client.post("/v1/auth/register", json={
        "email": "user@example.com",
        "password": "password123",
        "firstname": "John",
        "lastname": "Doe"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_login_user():
    """Test user login."""
    # First register
    client.post("/v1/auth/register", json={
        "email": "user@example.com",
        "password": "password123",
        "firstname": "John",
        "lastname": "Doe"
    })
    
    # Then login
    response = client.post("/v1/auth/login", json={
        "email": "user@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### Protected Endpoint Tests

```python
def test_protected_endpoint_requires_auth():
    """Test that protected endpoints require authentication."""
    response = client.get("/v1/auth/me")
    assert response.status_code == 401

def test_protected_endpoint_with_token():
    """Test protected endpoint with valid token."""
    # Register and get token
    register_response = client.post("/v1/auth/register", json={
        "email": "user@example.com",
        "password": "password123",
        "firstname": "John",
        "lastname": "Doe"
    })
    token = register_response.json()["access_token"]
    
    # Use token
    response = client.get(
        "/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"
```

## Testing Utilities

### Password Hashing Tests

```python
from src.auth.password import hash_password, verify_password

def test_hash_password():
    """Test password hashing."""
    password = "password123"
    hashed = hash_password(password)
    
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)
```

### JWT Token Tests

```python
from src.auth.jwt import create_access_token, verify_token, TokenType

def test_create_and_verify_token():
    """Test JWT token creation and verification."""
    token = create_access_token(
        user_id=1,
        email="user@example.com",
        roles=["user"]
    )
    
    payload = verify_token(token, TokenType.ACCESS)
    assert payload["sub"] == "1"
    assert payload["email"] == "user@example.com"
    assert payload["roles"] == ["user"]
```

## Testing Permissions

### Permission Check Tests

```python
from src.auth.permissions import has_permission

@pytest.mark.asyncio
async def test_user_permission_check(test_user: User):
    """Test user permission checking."""
    # Add role with permission
    role = Role(name="user", permissions=[
        Permission(name="user:read", resource="user", action="read")
    ])
    test_user.roles.append(role)
    
    assert has_permission(test_user, "user", "read")
    assert not has_permission(test_user, "user", "write")
```

## Async Testing

### Async Function Tests

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    result = await some_async_function()
    assert result is not None
```

## Best Practices

1. **Use Fixtures**: Share common setup code
2. **Test Edge Cases**: Don't just test happy path
3. **Keep Tests Fast**: Use in-memory database for tests
4. **Clear Test Names**: Describe what is being tested
5. **Isolate Tests**: Each test should be independent

## Coverage Goals

- Aim for **80%+ coverage** for critical paths
- Focus on business logic
- Test error cases

## Related Documentation

- [Testing Guide](../../docs/development/testing.md) - General testing guide
- [Coding Standards](../../docs/development/coding-standards.md) - Code standards

