"""Unit tests for models module."""

from datetime import UTC, datetime

import pytest
from pytest_mock import MockerFixture

from src.models import CustomBaseModel, datetime_to_utc_str


@pytest.mark.unit
class TestDatetimeToUtcStr:
    """Test datetime_to_utc_str function."""

    def test_converts_utc_datetime_to_string(self) -> None:
        """Test converting UTC datetime to ISO string."""
        dt = datetime(2024, 1, 1, 12, 30, 45, tzinfo=UTC)

        result = datetime_to_utc_str(dt)

        assert result == "2024-01-01T12:30:45Z"

    def test_returns_string_type(self) -> None:
        """Test that function returns a string."""
        dt = datetime(2024, 1, 1, 12, 30, 45, tzinfo=UTC)

        result = datetime_to_utc_str(dt)

        assert isinstance(result, str)

    def test_calls_format_datetime_iso(self, mocker: MockerFixture) -> None:
        """Test that function calls format_datetime_iso."""
        mock_format = mocker.patch("src.models.format_datetime_iso", return_value="2024-01-01T12:30:45Z")
        dt = datetime(2024, 1, 1, 12, 30, 45, tzinfo=UTC)

        datetime_to_utc_str(dt)

        mock_format.assert_called_once_with(dt)


@pytest.mark.unit
class TestCustomBaseModel:
    """Test CustomBaseModel class."""

    class SampleModel(CustomBaseModel):
        """Sample model for testing CustomBaseModel."""

        name: str
        created_at: datetime
        value: int

    def test_model_dump_with_python_mode_keeps_datetime(self) -> None:
        """Test that model_dump with python mode keeps datetime objects."""
        dt = datetime(2024, 1, 1, 12, 30, 45, tzinfo=UTC)
        model = self.SampleModel(name="test", created_at=dt, value=42)

        result = model.model_dump(mode="python")

        assert isinstance(result["created_at"], datetime)
        assert result["created_at"] == dt

    def test_model_dump_with_json_mode_converts_datetime(self) -> None:
        """Test that model_dump with json mode converts datetime to string."""
        dt = datetime(2024, 1, 1, 12, 30, 45, tzinfo=UTC)
        model = self.SampleModel(name="test", created_at=dt, value=42)

        result = model.model_dump(mode="json")

        assert isinstance(result["created_at"], str)
        assert result["created_at"] == "2024-01-01T12:30:45Z"

    def test_model_dump_default_mode_keeps_datetime(self) -> None:
        """Test that model_dump without mode keeps datetime objects."""
        dt = datetime(2024, 1, 1, 12, 30, 45, tzinfo=UTC)
        model = self.SampleModel(name="test", created_at=dt, value=42)

        result = model.model_dump()

        assert isinstance(result["created_at"], datetime)
        assert result["created_at"] == dt

    def test_model_dump_preserves_non_datetime_fields(self) -> None:
        """Test that non-datetime fields are preserved correctly."""
        dt = datetime(2024, 1, 1, 12, 30, 45, tzinfo=UTC)
        model = self.SampleModel(name="test", created_at=dt, value=42)

        result = model.model_dump(mode="json")

        assert result["name"] == "test"
        assert result["value"] == 42

    def test_serializable_dict_converts_datetime_to_string(self) -> None:
        """Test that serializable_dict converts datetime to string."""
        dt = datetime(2024, 1, 1, 12, 30, 45, tzinfo=UTC)
        model = self.SampleModel(name="test", created_at=dt, value=42)

        result = model.serializable_dict()

        assert isinstance(result["created_at"], str)
        assert result["created_at"] == "2024-01-01T12:30:45Z"

    def test_serializable_dict_returns_dict(self) -> None:
        """Test that serializable_dict returns a dictionary."""
        dt = datetime(2024, 1, 1, 12, 30, 45, tzinfo=UTC)
        model = self.SampleModel(name="test", created_at=dt, value=42)

        result = model.serializable_dict()

        assert isinstance(result, dict)

    def test_serializable_dict_preserves_all_fields(self) -> None:
        """Test that serializable_dict preserves all model fields."""
        dt = datetime(2024, 1, 1, 12, 30, 45, tzinfo=UTC)
        model = self.SampleModel(name="test", created_at=dt, value=42)

        result = model.serializable_dict()

        assert "name" in result
        assert "created_at" in result
        assert "value" in result
        assert len(result) == 3

    def test_model_with_multiple_datetime_fields(self) -> None:
        """Test model with multiple datetime fields."""

        class MultiDateTimeModel(CustomBaseModel):
            """Model with multiple datetime fields."""

            created_at: datetime
            updated_at: datetime
            name: str

        created = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
        updated = datetime(2024, 1, 2, 12, 0, 0, tzinfo=UTC)
        model = MultiDateTimeModel(created_at=created, updated_at=updated, name="test")

        result = model.model_dump(mode="json")

        assert isinstance(result["created_at"], str)
        assert isinstance(result["updated_at"], str)
        assert result["created_at"] == "2024-01-01T12:00:00Z"
        assert result["updated_at"] == "2024-01-02T12:00:00Z"

