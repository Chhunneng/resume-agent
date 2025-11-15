"""V1 API route handlers."""

from fastapi import APIRouter

from src.health import router as health_router

# Create the main v1 router
router = APIRouter(prefix="/v1", tags=["v1"])

# Include all v1 sub-routers
router.include_router(health_router)
