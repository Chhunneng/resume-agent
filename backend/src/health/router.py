"""Health check endpoints."""

import time

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy import text

from ..database import engine
from ..datetime import get_current_utc_datetime
from .constants import DatabaseStatus, HealthStatus
from .schemas import HealthDetail, HealthStatusResponse

router = APIRouter(prefix="/health", tags=["health"])

# Store application start time for uptime calculation
APP_START_TIME = time.time()


@router.get(
    "",
    response_model=HealthStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Basic health check",
    description="Returns a simple health status indicating if the API is running.",
    responses={
        200: {
            "description": "Service is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "timestamp": "2024-01-01T00:00:00Z",
                        "version": "1.0.0",
                    }
                }
            },
        }
    },
)
async def health_check() -> HealthStatusResponse:
    """
    Basic health check endpoint.

    Returns a simple status indicating the API is running.
    This endpoint does not check database connectivity.
    """
    return HealthStatusResponse(
        status=HealthStatus.HEALTHY,
        timestamp=get_current_utc_datetime(),
        version="1.0.0",
    )


@router.get(
    "/detailed",
    response_model=HealthDetail,
    status_code=status.HTTP_200_OK,
    summary="Detailed health check",
    description="Returns detailed health information including database connectivity and uptime.",
    responses={
        200: {
            "description": "Service health details",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "timestamp": "2024-01-01T00:00:00Z",
                        "version": "1.0.0",
                        "database": "connected",
                        "uptime_seconds": 3600.5,
                    }
                }
            },
        },
        503: {
            "description": "Service is unhealthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "unhealthy",
                        "timestamp": "2024-01-01T00:00:00Z",
                        "version": "1.0.0",
                        "database": "disconnected",
                        "uptime_seconds": 3600.5,
                    }
                }
            },
        },
    },
)
async def health_check_detailed() -> JSONResponse:
    """
    Detailed health check endpoint.

    Checks:
    - Database connectivity
    - Application uptime

    Returns 503 status if any component is unhealthy.
    """
    uptime_seconds = time.time() - APP_START_TIME

    # Check database connectivity
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        database_status = DatabaseStatus.CONNECTED
        overall_status = HealthStatus.HEALTHY
        http_status = status.HTTP_200_OK
    except Exception:
        database_status = DatabaseStatus.DISCONNECTED
        overall_status = HealthStatus.UNHEALTHY
        http_status = status.HTTP_503_SERVICE_UNAVAILABLE

    health_detail = HealthDetail(
        status=overall_status,
        timestamp=get_current_utc_datetime(),
        version="1.0.0",
        database=database_status,
        uptime_seconds=round(uptime_seconds, 2),
    )

    return JSONResponse(
        content=health_detail.model_dump(mode="json"),
        status_code=http_status,
    )
