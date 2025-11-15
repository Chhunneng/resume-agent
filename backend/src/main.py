import logging
import os
import subprocess
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import close_db, init_db

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


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Resume Agent API is running successfully"}
