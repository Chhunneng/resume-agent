"""Unit tests for datetime utility functions."""

from datetime import UTC, date, datetime, time, timezone, timedelta

import pytest
from pytest_mock import MockerFixture

from src.datetime.exceptions import DateParseError, DateTimeParseError, TimeParseError
from src.datetime.utils import (
    format_date_iso,
    format_datetime_iso,
    format_time_iso,
    get_current_utc_datetime,
    now,
    parse_date_iso,
    parse_datetime_iso,
    parse_time_iso,
)


@pytest.mark.unit
class TestGetCurrentUtcDatetime:
    """Test get_current_utc_datetime function."""

    def test_returns_datetime_object(self, mocker: MockerFixture) -> None:
        """Test that function returns a datetime object."""
        mock_datetime = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
        mocker.patch("src.datetime.utils.datetime").now.return_value = mock_datetime

        result = get_current_utc_datetime()

        assert isinstance(result, datetime)

    def test_returns_utc_timezone(self, mocker: MockerFixture) -> None:
        """Test that returned datetime has UTC timezone."""
        mock_datetime = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
        mocker.patch("src.datetime.utils.datetime").now.return_value = mock_datetime

        result = get_current_utc_datetime()

        assert result.tzinfo == UTC

    def test_calls_datetime_now_with_utc(self, mocker: MockerFixture) -> None:
        """Test that datetime.now is called with UTC timezone."""
        mock_datetime_class = mocker.patch("src.datetime.utils.datetime")
        mock_datetime = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
        mock_datetime_class.now.return_value = mock_datetime

        get_current_utc_datetime()

        mock_datetime_class.now.assert_called_once_with(UTC)


@pytest.mark.unit
class TestNow:
    """Test now() convenience alias function."""

    def test_returns_datetime_object(self, mocker: MockerFixture) -> None:
        """Test that function returns a datetime object."""
        mock_datetime = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
        mocker.patch("src.datetime.utils.get_current_utc_datetime", return_value=mock_datetime)

        result = now()

        assert isinstance(result, datetime)

    def test_calls_get_current_utc_datetime(self, mocker: MockerFixture) -> None:
        """Test that now() calls get_current_utc_datetime()."""
        mock_get_datetime = mocker.patch("src.datetime.utils.get_current_utc_datetime")
        mock_datetime = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
        mock_get_datetime.return_value = mock_datetime

        now()

        mock_get_datetime.assert_called_once()


@pytest.mark.unit
class TestFormatDatetimeIso:
    """Test format_datetime_iso function."""

    @pytest.mark.parametrize(
        ("input_dt", "expected"),
        [
            (
                datetime(2024, 1, 1, 12, 30, 45, tzinfo=UTC),
                "2024-01-01T12:30:45Z",
            ),
            (
                datetime(2024, 12, 31, 23, 59, 59, tzinfo=UTC),
                "2024-12-31T23:59:59Z",
            ),
        ],
    )
    def test_formats_utc_datetime(self, input_dt: datetime, expected: str) -> None:
        """Test formatting datetime already in UTC."""
        result = format_datetime_iso(input_dt)

        assert result == expected

    def test_formats_naive_datetime_as_utc(self) -> None:
        """Test that naive datetime is treated as UTC."""
        naive_dt = datetime(2024, 1, 1, 12, 30, 45)

        result = format_datetime_iso(naive_dt)

        assert result == "2024-01-01T12:30:45Z"

    def test_converts_timezone_to_utc(self) -> None:
        """Test that non-UTC timezone is converted to UTC."""
        # Create datetime in EST (UTC-5)
        est = timezone(timedelta(hours=-5))
        est_dt = datetime(2024, 1, 1, 12, 30, 45, tzinfo=est)

        result = format_datetime_iso(est_dt)

        # Should convert to UTC (12:30 EST = 17:30 UTC)
        assert result == "2024-01-01T17:30:45Z"

    def test_converts_positive_timezone_to_utc(self) -> None:
        """Test that positive timezone offset is converted to UTC."""
        # Create datetime in JST (UTC+9)
        jst = timezone(timedelta(hours=9))
        jst_dt = datetime(2024, 1, 1, 12, 30, 45, tzinfo=jst)

        result = format_datetime_iso(jst_dt)

        # Should convert to UTC (12:30 JST = 03:30 UTC)
        assert result == "2024-01-01T03:30:45Z"


@pytest.mark.unit
class TestFormatDateIso:
    """Test format_date_iso function."""

    @pytest.mark.parametrize(
        ("input_date", "expected"),
        [
            (date(2024, 1, 1), "2024-01-01"),
            (date(2024, 12, 31), "2024-12-31"),
            (date(2024, 2, 29), "2024-02-29"),  # Leap year
        ],
    )
    def test_formats_date_correctly(self, input_date: date, expected: str) -> None:
        """Test formatting various dates."""
        result = format_date_iso(input_date)

        assert result == expected


@pytest.mark.unit
class TestFormatTimeIso:
    """Test format_time_iso function."""

    @pytest.mark.parametrize(
        ("input_time", "expected"),
        [
            (time(0, 0, 0), "00:00:00"),
            (time(12, 30, 45), "12:30:45"),
            (time(23, 59, 59), "23:59:59"),
        ],
    )
    def test_formats_time_correctly(self, input_time: time, expected: str) -> None:
        """Test formatting various times."""
        result = format_time_iso(input_time)

        assert result == expected


@pytest.mark.unit
class TestParseDatetimeIso:
    """Test parse_datetime_iso function."""

    @pytest.mark.parametrize(
        ("input_str", "expected_dt"),
        [
            (
                "2024-01-01T12:30:45Z",
                datetime(2024, 1, 1, 12, 30, 45, tzinfo=UTC),
            ),
            (
                "2024-12-31T23:59:59Z",
                datetime(2024, 12, 31, 23, 59, 59, tzinfo=UTC),
            ),
        ],
    )
    def test_parses_utc_with_z_suffix(self, input_str: str, expected_dt: datetime) -> None:
        """Test parsing datetime string with Z suffix."""
        result = parse_datetime_iso(input_str)

        assert result == expected_dt
        assert result.tzinfo == UTC

    @pytest.mark.parametrize(
        ("input_str", "expected_dt"),
        [
            (
                "2024-01-01T12:30:45+00:00",
                datetime(2024, 1, 1, 12, 30, 45, tzinfo=UTC),
            ),
            (
                "2024-01-01T12:30:45-05:00",
                datetime(2024, 1, 1, 17, 30, 45, tzinfo=UTC),  # Converted to UTC
            ),
        ],
    )
    def test_parses_with_timezone_offset(self, input_str: str, expected_dt: datetime) -> None:
        """Test parsing datetime string with timezone offset."""
        result = parse_datetime_iso(input_str)

        assert result == expected_dt
        assert result.tzinfo == UTC

    def test_parses_naive_datetime_as_utc(self) -> None:
        """Test that naive datetime string is treated as UTC."""
        result = parse_datetime_iso("2024-01-01T12:30:45")

        assert result == datetime(2024, 1, 1, 12, 30, 45, tzinfo=UTC)
        assert result.tzinfo == UTC

    def test_raises_error_on_invalid_format(self) -> None:
        """Test that invalid datetime string raises DateTimeParseError."""
        with pytest.raises(DateTimeParseError):
            parse_datetime_iso("invalid-datetime")

    def test_raises_error_on_empty_string(self) -> None:
        """Test that empty string raises DateTimeParseError."""
        with pytest.raises(DateTimeParseError):
            parse_datetime_iso("")


@pytest.mark.unit
class TestParseDateIso:
    """Test parse_date_iso function."""

    @pytest.mark.parametrize(
        ("input_str", "expected_date"),
        [
            ("2024-01-01", date(2024, 1, 1)),
            ("2024-12-31", date(2024, 12, 31)),
            ("2024-02-29", date(2024, 2, 29)),  # Leap year
        ],
    )
    def test_parses_valid_date_string(self, input_str: str, expected_date: date) -> None:
        """Test parsing valid date strings."""
        result = parse_date_iso(input_str)

        assert result == expected_date
        assert isinstance(result, date)

    def test_raises_error_on_invalid_format(self) -> None:
        """Test that invalid date string raises DateParseError."""
        with pytest.raises(DateParseError):
            parse_date_iso("invalid-date")

    def test_raises_error_on_wrong_format(self) -> None:
        """Test that wrong format raises DateParseError."""
        with pytest.raises(DateParseError):
            parse_date_iso("01/01/2024")

    def test_raises_error_on_invalid_date(self) -> None:
        """Test that invalid date value raises DateParseError."""
        with pytest.raises(DateParseError):
            parse_date_iso("2024-13-01")  # Invalid month

    def test_raises_error_on_empty_string(self) -> None:
        """Test that empty string raises DateParseError."""
        with pytest.raises(DateParseError):
            parse_date_iso("")


@pytest.mark.unit
class TestParseTimeIso:
    """Test parse_time_iso function."""

    @pytest.mark.parametrize(
        ("input_str", "expected_time"),
        [
            ("00:00:00", time(0, 0, 0)),
            ("12:30:45", time(12, 30, 45)),
            ("23:59:59", time(23, 59, 59)),
        ],
    )
    def test_parses_valid_time_string(self, input_str: str, expected_time: time) -> None:
        """Test parsing valid time strings."""
        result = parse_time_iso(input_str)

        assert result == expected_time
        assert isinstance(result, time)

    def test_raises_error_on_invalid_format(self) -> None:
        """Test that invalid time string raises TimeParseError."""
        with pytest.raises(TimeParseError):
            parse_time_iso("invalid-time")

    def test_raises_error_on_wrong_format(self) -> None:
        """Test that wrong format raises TimeParseError."""
        with pytest.raises(TimeParseError):
            parse_time_iso("12:30 PM")

    def test_raises_error_on_invalid_time(self) -> None:
        """Test that invalid time value raises TimeParseError."""
        with pytest.raises(TimeParseError):
            parse_time_iso("25:00:00")  # Invalid hour

    def test_raises_error_on_empty_string(self) -> None:
        """Test that empty string raises TimeParseError."""
        with pytest.raises(TimeParseError):
            parse_time_iso("")

