"""V1 API route handlers."""

from fastapi import APIRouter

from src.auth import router as auth_router
from src.health import router as health_router
from src.llm.router import router as llm_router
from src.resumes.router import router as resumes_router

# Create the main v1 router
router = APIRouter(prefix="/v1", tags=["v1"])

# Include all v1 sub-routers
router.include_router(health_router)
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(llm_router, prefix="/users/me")
router.include_router(resumes_router, prefix="/resumes", tags=["resumes"])
