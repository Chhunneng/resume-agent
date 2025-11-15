"""Constants for health check module."""

from enum import Enum


class HealthStatus(str, Enum):
    """Health status enumeration."""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class DatabaseStatus(str, Enum):
    """Database connection status enumeration."""

    CONNECTED = "connected"
    DISCONNECTED = "disconnected"

