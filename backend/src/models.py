"""Global base models for the application."""

from datetime import datetime
from typing import Any

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict

from .datetime import format_datetime_iso


def datetime_to_utc_str(dt: datetime) -> str:
    """
    Convert datetime to UTC string format.

    Args:
        dt: Datetime object to format.

    Returns:
        ISO 8601 formatted string in UTC with Z suffix (e.g., "2024-01-01T00:00:00Z").
    """
    return format_datetime_iso(dt)


class CustomBaseModel(BaseModel):
    """
    Custom base model for all Pydantic models in the application.

    Provides:
    - Standardized datetime serialization to UTC format with Z suffix
    - Serializable dict method for JSON-safe serialization
    - Common configuration for all models

    All datetime fields are automatically serialized to UTC string format
    when using model_dump(mode="json") or serializable_dict().
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        """
        Override model_dump to ensure datetime fields are serialized correctly.

        When mode="json" is used, datetime fields are converted to UTC strings.
        """
        result = super().model_dump(**kwargs)
        mode = kwargs.get("mode", "python")

        if mode == "json":
            # Convert datetime fields to UTC strings
            for key, value in result.items():
                if isinstance(value, datetime):
                    result[key] = datetime_to_utc_str(value)

        return result

    def serializable_dict(self, **kwargs) -> dict:
        """
        Return a dict which contains only serializable fields.

        This method ensures all fields are JSON-serializable, including
        datetime objects which are converted to strings.

        Args:
            **kwargs: Additional arguments passed to model_dump().

        Returns:
            Dictionary with all serializable fields.
        """
        default_dict = self.model_dump(mode="json", **kwargs)
        return jsonable_encoder(default_dict)
