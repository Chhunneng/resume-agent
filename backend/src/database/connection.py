"""
Database connection management.

Database Naming Conventions:
- Tables: lower_case_snake, singular form (e.g., post, post_like, user_playlist)
- Group similar tables with module prefix (e.g., payment_account, payment_bill)
- Fields:
  - Use _at suffix for datetime fields (e.g., created_at, updated_at)
  - Use _date suffix for date fields (e.g., birth_date, expiry_date)
  - Stay consistent across tables (e.g., profile_id, creator_id, post_id)
- Indexes: %(column_0_label)s_idx
- Unique constraints: %(table_name)s_%(column_0_name)s_key
- Check constraints: %(table_name)s_%(constraint_name)s_check
- Foreign keys: %(table_name)s_%(column_0_name)s_fkey
- Primary keys: %(table_name)s_pkey
"""

from collections.abc import AsyncGenerator

from sqlalchemy import MetaData, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from .config import db_settings

# PostgreSQL naming conventions for database keys
POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

# Create metadata with naming conventions
metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)

# Configure SQLModel to use the custom metadata
SQLModel.metadata = metadata

# Create async engine
engine = create_async_engine(
    db_settings.get_database_url(),
    echo=False,  # Set to True for SQL query logging
    future=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function to get database session.

    Use this in FastAPI route dependencies.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database connection."""
    # Test connection
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))


async def close_db() -> None:
    """Close database connections."""
    await engine.dispose()

