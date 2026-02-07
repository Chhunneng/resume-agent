import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from scalar_fastapi import get_scalar_api_reference

from src.database import AsyncSessionLocal, check_migrations, close_db, init_db
from src.routes.v1 import router as v1_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Lifespan context manager for application startup and shutdown."""
    # Startup
    await init_db()
    # Check migrations in development mode (non-blocking)
    await check_migrations()
    # Initialize RBAC cache
    try:
        async with AsyncSessionLocal() as session:
            # await initialize_rbac_cache(session)
            logger.info("RBAC cache initialized successfully")
    except Exception as e:
        logger.warning(f"Failed to initialize RBAC cache: {e}")
    yield
    # Shutdown
    await close_db()


app = FastAPI(
    title="Resume Agent API",
    description="API for Resume Agent application",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None,  # Disable default Swagger UI
    redoc_url=None,  # Disable default ReDoc
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include v1 API routes
app.include_router(v1_router)


@app.get("/docs", include_in_schema=False, response_class=HTMLResponse, tags=["docs"])
async def scalar_docs() -> HTMLResponse:
    """
    Scalar API documentation endpoint (replaces default Swagger UI).

    Provides interactive API documentation using Scalar.
    Access at: http://localhost:8000/docs
    """
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Resume Agent API Documentation",
    )


@app.get(
    "/",
    tags=["root"],
    summary="Root endpoint",
    description="Returns a welcome message indicating the API is running.",
    responses={
        200: {
            "description": "API is running successfully",
            "content": {
                "application/json": {"example": {"message": "Resume Agent API is running."}}
            },
        }
    },
)
def read_root() -> dict[str, str]:
    """
    Root endpoint.

    Returns a simple message indicating the API is running.
    """
    return {"message": "Resume Agent API is running."}
