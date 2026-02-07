# Coding Standards

This document outlines the coding standards and conventions for Resume Agent.

## General Principles

- **Write clear, readable code**: Code is read more often than written
- **Follow existing patterns**: Consistency is key
- **Keep functions small**: Single responsibility principle
- **Use descriptive names**: Variable and function names should be self-explanatory
- **Document complex logic**: Add comments where needed

## Python Standards

### Code Style

- Follow **PEP 8** style guide
- Use **Ruff** for linting and formatting
- Maximum line length: **88 characters** (Black default)
- Use **type hints** for all function signatures

### Naming Conventions

- **Functions and variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private attributes**: `_leading_underscore`

### File Structure

- **Directories**: `lowercase_with_underscores`
- **Files**: `lowercase_with_underscores.py`
- **Modules**: One class/function per file when possible

### Type Hints

Always use type hints:

```python
def process_user(user_id: int, email: str) -> dict[str, str]:
    """Process user data."""
    return {"id": user_id, "email": email}
```

### Docstrings

Use Google-style docstrings:

```python
def create_user(email: str, password: str) -> User:
    """
    Create a new user.

    Args:
        email: User email address
        password: User password

    Returns:
        Created user instance

    Raises:
        ValueError: If email already exists
    """
    # Implementation
```

### Error Handling

- Use specific exception types
- Handle errors at the beginning of functions (early returns)
- Use guard clauses to avoid deep nesting

```python
def get_user(user_id: int) -> User:
    if not user_id:
        raise ValueError("User ID is required")
    
    user = await session.get(User, user_id)
    if not user:
        raise NotFoundError(f"User {user_id} not found")
    
    return user
```

### Async/Await

- Use `async def` for asynchronous functions
- Use `await` for async operations
- Don't mix sync and async unnecessarily

```python
async def get_user(user_id: int) -> User:
    result = await session.exec(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
```

## TypeScript Standards

### Code Style

- Use **TypeScript** for all code
- Follow **ESLint** and **Prettier** configurations
- Maximum line length: **100 characters**
- Use **interfaces** over types (avoid enums)

### Naming Conventions

- **Functions and variables**: `camelCase`
- **Components**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Files**: `kebab-case.tsx` or `kebab-case.ts`

### Type Definitions

Always define types:

```typescript
interface User {
  id: number;
  email: string;
  firstname: string;
  lastname: string;
}

function getUser(id: number): Promise<User> {
  // Implementation
}
```

### Components

- Use functional components
- Use hooks for state management
- Keep components small and focused

```typescript
interface UserCardProps {
  user: User;
  onEdit: (user: User) => void;
}

export function UserCard({ user, onEdit }: UserCardProps) {
  return (
    <div>
      <h3>{user.firstname} {user.lastname}</h3>
      <button onClick={() => onEdit(user)}>Edit</button>
    </div>
  );
}
```

## Database Standards

### Naming Conventions

- **Tables**: `lower_case_snake`, singular (e.g., `user`, `post`)
- **Columns**: `snake_case`
- **Foreign keys**: `{table}_id` (e.g., `user_id`, `post_id`)
- **Timestamps**: `{action}_at` (e.g., `created_at`, `updated_at`)

### Models

- Use SQLModel for models
- Define relationships clearly
- Use proper indexes

```python
class User(BaseModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    roles: list[Role] = Relationship(back_populates="users")
```

## API Standards

### Endpoint Naming

- Use RESTful conventions
- Use plural nouns: `/v1/users`, `/v1/posts`
- Use HTTP methods correctly: GET, POST, PUT, DELETE

### Response Format

- Consistent response structure
- Use appropriate HTTP status codes
- Include error details

### Documentation

- Document all endpoints
- Include request/response examples
- Document authentication requirements

## Testing Standards

### Test Naming

- Use descriptive test names
- Follow pattern: `test_{what}_{condition}_{expected_result}`

```python
def test_login_with_valid_credentials_returns_tokens():
    # Test implementation
```

### Test Structure

- Arrange: Set up test data
- Act: Execute the code
- Assert: Verify results

```python
def test_create_user():
    # Arrange
    email = "user@example.com"
    password = "secure_password"
    
    # Act
    user = create_user(email, password)
    
    # Assert
    assert user.email == email
    assert user.id is not None
```

## Git Standards

### Commit Messages

Follow [Conventional Commits](../../CONTRIBUTING.md):

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

### Branch Naming

- Feature: `feature/feature-name`
- Bug fix: `fix/bug-description`
- Documentation: `docs/documentation-update`

## Code Review Guidelines

### What to Review

- Code correctness and logic
- Adherence to coding standards
- Test coverage
- Documentation updates
- Performance considerations

### Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No security issues introduced
- [ ] Performance is acceptable

## Tools

### Python

- **Ruff**: Linting and formatting
- **Pytest**: Testing
- **Mypy**: Type checking (optional)

### TypeScript

- **ESLint**: Linting
- **Prettier**: Formatting
- **TypeScript**: Type checking

## Related Documentation

- [Testing Guide](testing.md) - Testing standards
- [Contributing Guidelines](../../CONTRIBUTING.md) - Contribution process
- [Development Setup](setup.md) - Environment setup

