"""Health check response models."""

from datetime import datetime

from pydantic import ConfigDict, Field

from ..models import CustomBaseModel
from .constants import DatabaseStatus, HealthStatus


class HealthStatusResponse(CustomBaseModel):
    """Health status response model."""

    status: HealthStatus = Field(
        ...,
        description="Health status of the service",
    )
    timestamp: datetime = Field(
        ...,
        description="Current server timestamp in ISO 8601 format (UTC)",
        examples=["2024-01-01T00:00:00Z"],
    )
    version: str = Field(
        ...,
        description="API version",
        examples=["1.0.0"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": HealthStatus.HEALTHY,
                "timestamp": "2024-01-01T00:00:00Z",
                "version": "1.0.0",
            }
        }
    )


class HealthDetail(CustomBaseModel):
    """Detailed health check response model."""

    status: HealthStatus = Field(
        ...,
        description="Overall health status of the service",
    )
    timestamp: datetime = Field(
        ...,
        description="Current server timestamp in ISO 8601 format (UTC)",
        examples=["2024-01-01T00:00:00Z"],
    )
    version: str = Field(
        ...,
        description="API version",
        examples=["1.0.0"],
    )
    database: DatabaseStatus = Field(
        ...,
        description="Database connection status",
    )
    uptime_seconds: float = Field(
        ...,
        description="Application uptime in seconds",
        examples=[3600.5],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": HealthStatus.HEALTHY,
                "timestamp": "2024-01-01T00:00:00Z",
                "version": "1.0.0",
                "database": DatabaseStatus.CONNECTED,
                "uptime_seconds": 3600.5,
            }
        }
    )
