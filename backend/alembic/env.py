"""
Alembic environment configuration for database migrations.

This file configures Alembic to work with async database connections using asyncpg.
Since our application uses asyncpg for async database operations, we configure
Alembic to use the same async driver instead of requiring psycopg2-binary.

Reference: https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic
"""
import asyncio
from logging.config import fileConfig
from typing import Any
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine
from alembic import context

# Import your database configuration and SQLModel
import sys
from pathlib import Path

# Add the backend directory to the path so we can import our modules
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from src.database import db_settings, metadata
from sqlmodel import SQLModel

# Import all models here so Alembic can discover them for autogenerate
# When you create new models, import them here (e.g., from src.models import User)
# SQLModel.metadata automatically collects all registered SQLModel models
# Use the custom metadata with naming conventions
from src.auth.models import (  # noqa: F401
    Permission,
    Role,
    RolePermission,
    User,
    UserRole,
)
from src.resumes.models import Resume  # noqa: F401
from src.llm.models import UserLLMConfig  # noqa: F401
# from src.database.base import BaseModel  # noqa: F401

target_metadata = metadata

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_url() -> str:
    """
    Get database URL from configuration.
    
    Returns the async database URL with +asyncpg driver.
    We keep +asyncpg because we're using async migrations.
    
    Returns:
        str: Database URL in format: postgresql+asyncpg://user:pass@host:port/db
    """
    # Keep +asyncpg for async migrations - no need to remove it anymore
    return db_settings.get_database_url()


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine.
    By skipping the Engine creation, we don't even need a DBAPI to be available.
    
    Offline mode is used when you want to generate SQL scripts without
    connecting to the database. Calls to context.exec() here emit the
    given string to the script output.

    Reference: https://alembic.sqlalchemy.org/en/latest/offline.html
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Run migrations with the given connection.
    
    This function is called by the async migration runner with a database
    connection. It configures Alembic's context and runs the migrations
    within a transaction.
    
    Args:
        connection: The database connection (can be sync or async, but we use
                    run_sync() to adapt it for Alembic's sync API)
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Run migrations using async database engine.
    
    This function creates an async engine using asyncpg and runs migrations
    asynchronously. We use connection.run_sync() to bridge Alembic's synchronous
    API with our async database connection.
    
    Reference: https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic
    """
    # Get the database URL directly from our settings
    # This URL already includes +asyncpg driver
    database_url = get_url()
    
    # Create async engine using asyncpg driver
    # We use NullPool to avoid connection pooling issues during migrations
    connectable = create_async_engine(
        database_url,
        poolclass=pool.NullPool,
    )

    # Run migrations within an async connection
    # connection.run_sync() allows us to run sync Alembic code in an async context
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    # Clean up the engine
    await connectable.dispose()


def get_programmatic_connection() -> Any | None:
    """
    Check if a connection was provided programmatically.
    
    When Alembic is called from code (programmatic API), a connection can be
    passed via config.attributes["connection"]. This allows sharing a connection
    instead of creating a new one.
    
    Returns:
        Connection object if found, None otherwise
    
    Reference: https://alembic.sqlalchemy.org/en/latest/cookbook.html#connection-sharing
    """
    return config.attributes.get("connection", None)


async def run_migrations_with_provided_async_connection(connection: AsyncConnection) -> None:
    """
    Run migrations using a provided async connection.
    
    This function handles async connections that are passed programmatically.
    It uses connection.run_sync() to bridge Alembic's synchronous API with
    the async connection.
    
    Args:
        connection: An async database connection provided programmatically
    
    Reference: https://alembic.sqlalchemy.org/en/latest/cookbook.html#connection-sharing
    """
    await connection.run_sync(do_run_migrations)


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    
    Supports both command-line and programmatic API usage:
    - Command-line: Creates its own connection (normal usage)
    - Programmatic: Uses connection passed via config.attributes["connection"]
    
    This function is called by Alembic when you run commands like:
    - alembic upgrade head (command-line)
    - Or programmatically: config.attributes["connection"] = my_connection; command.upgrade(config, "head")
    
    Reference: https://alembic.sqlalchemy.org/en/latest/cookbook.html#connection-sharing
    """
    # Check if a connection was provided programmatically
    provided_connection = get_programmatic_connection()
    
    if provided_connection is None:
        # No connection provided - create our own (command-line usage)
        asyncio.run(run_async_migrations())
    else:
        # Connection provided programmatically - use it
        # Check if it's an async connection (has run_sync method)
        if hasattr(provided_connection, "run_sync"):
            # It's an async connection - run migrations in async context
            asyncio.run(run_migrations_with_provided_async_connection(provided_connection))
        else:
            # It's a sync connection - use it directly
            do_run_migrations(provided_connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
