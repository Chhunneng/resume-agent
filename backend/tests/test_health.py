"""Example tests demonstrating async test client usage."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient) -> None:
    """Test the /health endpoint returns a successful response."""
    response = await client.get("/health")

    assert response.status_code == 200

    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "version" in data
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient) -> None:
    """Test the root endpoint returns a welcome message."""
    response = await client.get("/")

    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "Resume Agent API is running successfully" in data["message"]

