# Database Documentation

This document covers database setup, migrations, and management for Resume Agent.

## Database Setup

### PostgreSQL Configuration

Resume Agent uses PostgreSQL 16+ as the database.

### Connection Configuration

Database connection is configured via environment variables:

```env
POSTGRES_DB=resume_agent
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=postgres  # Use 'postgres' in Docker, 'localhost' manually
POSTGRES_PORT=5432
```

Or use `DATABASE_URL` directly:

```env
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database
```

## Database Models

### User Model

Stores user account information and authentication data.

**Key Fields:**
- `id`: Primary key
- `email`: Unique email address
- `password_hash`: Hashed password
- `is_active`: Account status
- `roles`: Many-to-many relationship with Role

### Role Model

Stores roles that can be assigned to users.

**Key Fields:**
- `id`: Primary key
- `name`: Unique role name
- `is_default`: Whether role is assigned to new users
- `permissions`: Many-to-many relationship with Permission

### Permission Model

Stores permissions that can be assigned to roles.

**Key Fields:**
- `id`: Primary key
- `name`: Unique permission name
- `resource`: Resource name (e.g., "user")
- `action`: Action name (e.g., "read", "write")

See [Database Schema](../../docs/architecture/database-schema.md) for complete schema documentation.

## Migrations

### Alembic Setup

Resume Agent uses Alembic for database migrations.

### Creating Migrations

Create a new migration:

```bash
alembic revision --autogenerate -m "description of changes"
```

This will:
1. Detect model changes
2. Generate migration file
3. Create migration in `alembic/versions/`

### Applying Migrations

Apply all pending migrations:

```bash
alembic upgrade head
```

Apply specific migration:

```bash
alembic upgrade <revision>
```

### Rolling Back Migrations

Rollback one migration:

```bash
alembic downgrade -1
```

Rollback to specific revision:

```bash
alembic downgrade <revision>
```

### Migration Status

Check current migration status:

```bash
alembic current
```

View migration history:

```bash
alembic history
```

### Migration Best Practices

1. **Review Generated Migrations**: Always review auto-generated migrations
2. **Test Migrations**: Test migrations on development database first
3. **Backup Before Migration**: Always backup production database before migration
4. **One Change Per Migration**: Keep migrations focused on one change
5. **Document Breaking Changes**: Document any breaking changes in migration

## Database Connection

### Async Session Management

Database sessions are managed using SQLAlchemy async sessions:

```python
from src.database import get_db_session

async def my_function():
    async with get_db_session() as session:
        # Use session
        result = await session.exec(select(User))
        users = result.scalars().all()
```

### Connection Pooling

Connection pooling is handled automatically by SQLAlchemy:

```python
engine = create_async_engine(
    database_url,
    pool_size=20,  # Maximum connections
    max_overflow=10,  # Additional connections
)
```

## Query Patterns

### Basic Queries

```python
from sqlalchemy import select
from src.auth.models import User

# Select all users
result = await session.exec(select(User))
users = result.scalars().all()

# Select user by ID
result = await session.exec(select(User).where(User.id == user_id))
user = result.scalar_one_or_none()

# Select user by email
result = await session.exec(select(User).where(User.email == email))
user = result.scalar_one_or_none()
```

### Eager Loading

Load relationships eagerly to avoid N+1 queries:

```python
from sqlalchemy.orm import selectinload

# Load user with roles
result = await session.exec(
    select(User)
    .where(User.id == user_id)
    .options(selectinload(User.roles))
)
user = result.scalar_one()
```

### Transactions

Use transactions for multiple operations:

```python
async with session.begin():
    user = User(email="user@example.com", ...)
    session.add(user)
    # Transaction commits automatically on success
    # Rolls back on exception
```

## Database Naming Conventions

### Tables

- Use `lower_case_snake` format
- Use singular form (e.g., `user`, not `users`)
- Group related tables with prefix (e.g., `payment_account`, `payment_bill`)

### Columns

- Use `snake_case` format
- Use `_at` suffix for datetime fields (e.g., `created_at`)
- Use `_date` suffix for date fields (e.g., `birth_date`)
- Use `{table}_id` for foreign keys (e.g., `user_id`)

### Indexes

- Format: `{column}_idx`
- Example: `email_idx`

### Constraints

- Unique: `{table}_{column}_key`
- Foreign key: `{table}_{column}_fkey`
- Primary key: `{table}_pkey`

## Backup and Restore

### Backup Database

```bash
# Using pg_dump
pg_dump -U postgres resume_agent > backup.sql

# Using Docker
docker compose exec postgres pg_dump -U postgres resume_agent > backup.sql
```

### Restore Database

```bash
# Using psql
psql -U postgres resume_agent < backup.sql

# Using Docker
docker compose exec -T postgres psql -U postgres resume_agent < backup.sql
```

### Automated Backups

See [Deployment Guide](../../docs/operations/deployment.md#database-backups) for automated backup setup.

## Performance Optimization

### Indexes

Add indexes for frequently queried columns:

```python
email: str = Field(unique=True, index=True)
```

### Query Optimization

1. Use `selectinload` for relationships
2. Avoid N+1 queries
3. Use database indexes
4. Limit result sets with pagination

### Connection Pooling

Configure connection pool size based on load:

```python
engine = create_async_engine(
    database_url,
    pool_size=20,
    max_overflow=10,
)
```

## Troubleshooting

### Connection Issues

1. Verify database is running
2. Check connection credentials
3. Verify network connectivity
4. Check firewall rules

### Migration Issues

1. Check migration status: `alembic current`
2. Review migration files
3. Test migrations on development database
4. Backup before applying migrations

### Performance Issues

1. Check database indexes
2. Analyze slow queries
3. Review connection pool settings
4. Optimize queries

## Related Documentation

- [Database Schema](../../docs/architecture/database-schema.md) - Complete schema
- [Auth System](auth-system.md) - Authentication models
- [Migrations Guide](../../docs/development/setup.md#database-migrations) - Migration workflow

