"""Pytest configuration and fixtures for async testing."""

import sys
from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import ASGITransport, AsyncClient
from pytest_mock import MockerFixture

# Set up Python path at module level so it's available when test modules are imported
# Get the backend directory (parent of tests directory) and resolve to absolute path
_backend_dir = Path(__file__).parent.parent.resolve()
_backend_dir_str = str(_backend_dir)

# Add to Python path if not already there (check both absolute and relative)
if _backend_dir_str not in sys.path:
    sys.path.insert(0, _backend_dir_str)
# Also add relative path in case pytest uses relative paths
_backend_dir_relative = str(Path(__file__).parent.parent)
if _backend_dir_relative not in sys.path and _backend_dir_relative != _backend_dir_str:
    sys.path.insert(0, _backend_dir_relative)


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Async test client fixture for FastAPI app.

    Uses httpx.AsyncClient with ASGITransport to properly handle
    async operations and prevent event loop errors when testing
    with async database connections.
    """
    # Import app here to avoid import errors when conftest.py is loaded
    from src.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture
def mock_datetime_now(mocker: MockerFixture) -> datetime:
    """
    Fixture for mocking current UTC datetime.

    Returns a fixed datetime object that can be used in tests.
    """
    fixed_datetime = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
    mocker.patch("datetime.datetime.now", return_value=fixed_datetime)
    return fixed_datetime


@pytest.fixture
def mock_time_time(mocker: MockerFixture) -> float:
    """
    Fixture for mocking time.time().

    Returns a fixed timestamp that can be used in tests.
    """
    fixed_time = 1000.0
    mocker.patch("time.time", return_value=fixed_time)
    return fixed_time


@pytest.fixture
def mock_db_engine_connected(mocker: MockerFixture) -> MagicMock:
    """
    Fixture for mocking a connected database engine.

    Returns a mock engine that simulates successful database connection.
    """
    mock_conn = AsyncMock()
    mock_conn.exec = AsyncMock()
    mock_engine = MagicMock()
    mock_engine.begin = MagicMock(return_value=AsyncMock())
    mock_engine.begin.return_value.__aenter__ = AsyncMock(return_value=mock_conn)
    mock_engine.begin.return_value.__aexit__ = AsyncMock(return_value=False)
    return mock_engine


@pytest.fixture
def mock_db_engine_disconnected(mocker: MockerFixture) -> MagicMock:
    """
    Fixture for mocking a disconnected database engine.

    Returns a mock engine that simulates database connection failure.
    """
    mock_engine = MagicMock()
    mock_engine.begin = MagicMock(side_effect=Exception("Database connection failed"))
    return mock_engine

