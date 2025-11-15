import logging
import os
import subprocess
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import close_db, init_db
from .datetime import get_current_utc_datetime
from .health.constants import HealthStatus
from .health.schemas import HealthStatusResponse
from .routes.v1 import router as v1_router

logger = logging.getLogger(__name__)


async def check_migrations() -> None:
    """Check migration status in development mode."""
    if os.getenv("DEBUG", "False").lower() != "true":
        return

    try:
        result = subprocess.run(
            ["alembic", "current"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except subprocess.TimeoutExpired:
        logger.warning("Migration check timed out")
        return
    except FileNotFoundError:
        logger.warning("Alembic not found in PATH, skipping migration check")
        return
    except Exception as e:
        logger.warning(f"Error checking migrations: {e}")
        return

    if result.returncode != 0:
        logger.warning(f"Could not check migration status: {result.stderr}")
        return

    current_version = result.stdout.strip()
    if current_version:
        logger.info(f"Current database migration version: {current_version}")
    else:
        logger.warning("No migrations have been applied yet")


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    """Lifespan context manager for application startup and shutdown."""
    # Startup
    await init_db()
    # Check migrations in development mode (non-blocking)
    await check_migrations()
    yield
    # Shutdown
    await close_db()


app = FastAPI(
    title="Resume Agent API",
    description="API for Resume Agent application",
    version="1.0.0",
    lifespan=lifespan,
)

# Include v1 API routes
app.include_router(v1_router)


@app.get(
    "/",
    tags=["root"],
    summary="Root endpoint",
    description="Returns a welcome message indicating the API is running.",
    responses={
        200: {
            "description": "API is running successfully",
            "content": {
                "application/json": {
                    "example": {"message": "Resume Agent API is running successfully"}
                }
            },
        }
    },
)
def read_root() -> dict[str, str]:
    """
    Root endpoint.

    Returns a simple message indicating the API is running.
    """
    return {"message": "Resume Agent API is running successfully"}


@app.get(
    "/health",
    response_model=HealthStatusResponse,
    tags=["health"],
    summary="Root health check",
    description="Returns a simple health status indicating if the API is running. This is a root-level health endpoint.",
    responses={
        200: {
            "description": "Service is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "timestamp": "2025-11-15T18:16:27.687224Z",
                        "version": "1.0.0",
                    }
                }
            },
        }
    },
)
async def health_check() -> HealthStatusResponse:
    """
    Root-level health check endpoint.

    Returns a simple status indicating the API is running.
    This endpoint does not check database connectivity.
    For detailed health checks, use /v1/health/detailed.
    """
    return HealthStatusResponse(
        status=HealthStatus.HEALTHY,
        timestamp=get_current_utc_datetime(),
        version="1.0.0",
    )
