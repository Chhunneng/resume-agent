# Testing Guide

This guide covers testing practices and guidelines for Resume Agent.

## Testing Philosophy

- **Write tests for new features**: Every new feature should have tests
- **Test behavior, not implementation**: Focus on what the code does, not how
- **Keep tests simple**: Tests should be easy to understand and maintain
- **Test edge cases**: Don't just test the happy path

## Test Structure

### Test Organization

Tests are organized in the `tests/` directory:

```
tests/
├── conftest.py          # Shared fixtures
├── test_health.py      # Health check tests
└── src/
    ├── conftest.py      # Source-specific fixtures
    ├── test_models.py   # Model tests
    └── datetime/
        └── test_utils.py # Utility tests
```

### Test Naming

Follow the pattern: `test_{what}_{condition}_{expected_result}`

```python
def test_login_with_valid_credentials_returns_tokens():
    """Test that login with valid credentials returns access and refresh tokens."""
    pass

def test_login_with_invalid_password_raises_error():
    """Test that login with invalid password raises authentication error."""
    pass
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_auth.py
```

### Run Specific Test

```bash
pytest tests/test_auth.py::test_login_with_valid_credentials
```

### Run with Verbose Output

```bash
pytest -v
```

### Run with Coverage

```bash
pytest --cov=src --cov-report=html
```

### Stop on First Failure

```bash
pytest -x
```

## Test Fixtures

### Database Fixtures

Use fixtures for database setup:

```python
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture
async def db_session():
    """Create a test database session."""
    # Setup
    session = create_test_session()
    yield session
    # Teardown
    await session.close()
```

### User Fixtures

```python
@pytest.fixture
async def test_user(db_session: AsyncSession):
    """Create a test user."""
    user = User(
        email="test@example.com",
        password_hash=hash_password("password"),
        firstname="Test",
        lastname="User"
    )
    db_session.add(user)
    await db_session.commit()
    return user
```

## Writing Tests

### Test Structure

Follow the Arrange-Act-Assert pattern:

```python
async def test_create_user(db_session: AsyncSession):
    # Arrange
    email = "user@example.com"
    password = "secure_password"
    
    # Act
    user = await create_user(db_session, email, password)
    
    # Assert
    assert user.email == email
    assert user.id is not None
    assert user.password_hash != password  # Should be hashed
```

### Testing Async Functions

Use `pytest.mark.asyncio`:

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result is not None
```

### Testing API Endpoints

Use FastAPI's TestClient:

```python
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

### Testing Authentication

```python
def test_protected_endpoint_requires_auth():
    response = client.get("/v1/protected")
    assert response.status_code == 401

def test_protected_endpoint_with_token():
    # Get token
    login_response = client.post("/v1/auth/login", json={
        "email": "user@example.com",
        "password": "password"
    })
    token = login_response.json()["access_token"]
    
    # Use token
    response = client.get(
        "/v1/protected",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
```

### Testing Permissions

```python
async def test_user_without_permission_denied():
    user = create_user_with_role("user")  # No admin permission
    response = client.delete(
        "/v1/users/1",
        headers={"Authorization": f"Bearer {get_token(user)}"}
    )
    assert response.status_code == 403

async def test_user_with_permission_allowed():
    user = create_user_with_role("admin")  # Has admin permission
    response = client.delete(
        "/v1/users/1",
        headers={"Authorization": f"Bearer {get_token(user)}"}
    )
    assert response.status_code == 200
```

## Test Coverage

### Coverage Goals

- Aim for **80%+ coverage** for critical paths
- Focus on business logic, not boilerplate
- Test error cases and edge cases

### View Coverage Report

```bash
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

## Mocking

### Mock External Services

```python
from unittest.mock import patch, AsyncMock

@patch('src.external_service.api_call')
async def test_function_with_external_call(mock_api):
    mock_api.return_value = {"result": "success"}
    
    result = await function_that_calls_api()
    
    assert result == {"result": "success"}
    mock_api.assert_called_once()
```

### Mock Database

```python
from unittest.mock import AsyncMock

@pytest.fixture
def mock_db_session():
    session = AsyncMock()
    session.exec.return_value.scalar_one.return_value = User(...)
    return session
```

## Best Practices

### 1. Test Independence

- Each test should be independent
- Don't rely on test execution order
- Clean up after each test

### 2. Use Fixtures

- Share common setup code via fixtures
- Keep fixtures focused and reusable

### 3. Test Edge Cases

- Empty inputs
- Null values
- Boundary conditions
- Error conditions

### 4. Keep Tests Fast

- Use in-memory database for tests
- Mock slow operations
- Avoid unnecessary setup

### 5. Clear Test Names

- Test names should describe what is being tested
- Include expected outcome in name

## Common Test Patterns

### Testing Models

```python
def test_user_model():
    user = User(
        email="test@example.com",
        password_hash="hash",
        firstname="Test",
        lastname="User"
    )
    assert user.email == "test@example.com"
    assert user.get_role_names() == []
```

### Testing Utilities

```python
def test_hash_password():
    password = "password123"
    hashed = hash_password(password)
    
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)
```

### Testing Dependencies

```python
async def test_get_current_user_with_valid_token():
    token = create_access_token(user_id=1, email="user@example.com")
    user = await get_current_user(token)
    
    assert user.id == 1
    assert user.email == "user@example.com"
```

## Continuous Integration

Tests run automatically on:
- Pull requests
- Commits to main branch
- Scheduled runs

## Related Documentation

- [Coding Standards](coding-standards.md) - Code style guidelines
- [Development Setup](setup.md) - Environment setup
- [Backend Testing](../../backend/docs/testing.md) - Backend-specific testing

