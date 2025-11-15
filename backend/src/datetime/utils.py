"""
Standard datetime utilities for consistent date/time handling across the application.

IMPORTANT: This application uses UTC (Coordinated Universal Time) as the default timezone
for all datetime operations. All datetime objects should be in UTC unless explicitly
converted for display purposes.

All datetime functions in this module:
- Return datetime objects in UTC timezone
- Convert input datetimes to UTC if they have timezone info
- Assume UTC for naive (timezone-less) datetime objects
"""

from datetime import UTC, date, datetime, time

from .exceptions import DateParseError, DateTimeParseError, TimeParseError

# Default timezone constant - UTC is the standard for this application
DEFAULT_TIMEZONE = UTC

# Standard format constants
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"  # ISO 8601 with timezone
DATETIME_FORMAT_UTC = "%Y-%m-%dT%H:%M:%SZ"  # ISO 8601 UTC (Z suffix)
DATE_FORMAT = "%Y-%m-%d"  # ISO date format
TIME_FORMAT = "%H:%M:%S"  # ISO time format


def get_current_utc_datetime() -> datetime:
    """
    Get current UTC datetime.

    This is the standard function to get the current time in the application.
    All timestamps should use UTC as the default timezone.

    Returns:
        Current datetime in UTC timezone.

    Example:
        >>> dt = get_current_utc_datetime()
        >>> isinstance(dt, datetime)
        True
        >>> dt.tzinfo == UTC
        True
    """
    return datetime.now(DEFAULT_TIMEZONE)


# Convenience alias - shorter name for common use case
def now() -> datetime:
    """
    Get current UTC datetime (convenience alias).

    This is a shorter alias for get_current_utc_datetime().
    Use this when you need the current time in UTC (application default).

    Returns:
        Current datetime in UTC timezone.

    Example:
        >>> dt = now()
        >>> dt.tzinfo == UTC
        True
    """
    return get_current_utc_datetime()


def format_datetime_iso(dt: datetime) -> str:
    """
    Format datetime to ISO 8601 string with UTC timezone (Z suffix).

    All datetimes are normalized to UTC before formatting, as UTC is the default
    timezone for this application.

    Args:
        dt: Datetime object to format. If naive (no timezone), assumes UTC.
            If has timezone, converts to UTC.

    Returns:
        ISO 8601 formatted string in UTC (e.g., "2024-01-01T00:00:00Z").

    Example:
        >>> dt = datetime(2024, 1, 1, 0, 0, 0, tzinfo=UTC)
        >>> format_datetime_iso(dt)
        '2024-01-01T00:00:00Z'
    """
    if dt.tzinfo is None:
        # If no timezone info, assume UTC (application default)
        dt = dt.replace(tzinfo=DEFAULT_TIMEZONE)
    elif dt.tzinfo != DEFAULT_TIMEZONE:
        # Convert to UTC if not already (application default)
        dt = dt.astimezone(DEFAULT_TIMEZONE)

    return dt.strftime(DATETIME_FORMAT_UTC)


def format_date_iso(d: date) -> str:
    """
    Format date to ISO 8601 string.

    Args:
        d: Date object to format.

    Returns:
        ISO formatted date string (e.g., "2024-01-01").

    Example:
        >>> d = date(2024, 1, 1)
        >>> format_date_iso(d)
        '2024-01-01'
    """
    return d.strftime(DATE_FORMAT)


def format_time_iso(t: time) -> str:
    """
    Format time to ISO 8601 string.

    Args:
        t: Time object to format.

    Returns:
        ISO formatted time string (e.g., "00:00:00").

    Example:
        >>> t = time(12, 30, 45)
        >>> format_time_iso(t)
        '12:30:45'
    """
    return t.strftime(TIME_FORMAT)


def parse_datetime_iso(dt_str: str) -> datetime:
    """
    Parse ISO 8601 datetime string to datetime object.

    All parsed datetimes are normalized to UTC, as UTC is the default timezone
    for this application.

    Supports formats:
    - "2024-01-01T00:00:00Z" (UTC with Z)
    - "2024-01-01T00:00:00+00:00" (with timezone offset, converted to UTC)
    - "2024-01-01T00:00:00" (naive, assumed UTC per application default)

    Args:
        dt_str: ISO 8601 formatted datetime string.

    Returns:
        Datetime object in UTC timezone (application default).

    Raises:
        ValueError: If the string cannot be parsed.

    Example:
        >>> dt = parse_datetime_iso("2024-01-01T00:00:00Z")
        >>> isinstance(dt, datetime)
        True
        >>> dt.tzinfo == UTC
        True
    """
    # Try parsing with Z suffix first
    if dt_str.endswith("Z"):
        dt_str = dt_str[:-1] + "+00:00"

    # Try parsing with timezone
    try:
        dt = datetime.fromisoformat(dt_str)
    except ValueError as e:
        raise DateTimeParseError from e

    # Ensure UTC timezone (application default)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=DEFAULT_TIMEZONE)
    else:
        dt = dt.astimezone(DEFAULT_TIMEZONE)

    return dt


def parse_date_iso(date_str: str) -> date:
    """
    Parse ISO 8601 date string to date object.

    Args:
        date_str: ISO formatted date string (e.g., "2024-01-01").

    Returns:
        Date object.

    Raises:
        ValueError: If the string cannot be parsed.

    Example:
        >>> d = parse_date_iso("2024-01-01")
        >>> isinstance(d, date)
        True
    """
    try:
        return datetime.strptime(date_str, DATE_FORMAT).date()
    except ValueError as e:
        raise DateParseError from e


def parse_time_iso(time_str: str) -> time:
    """
    Parse ISO 8601 time string to time object.

    Args:
        time_str: ISO formatted time string (e.g., "12:30:45").

    Returns:
        Time object.

    Raises:
        ValueError: If the string cannot be parsed.

    Example:
        >>> t = parse_time_iso("12:30:45")
        >>> isinstance(t, time)
        True
    """
    try:
        return datetime.strptime(time_str, TIME_FORMAT).time()
    except ValueError as e:
        raise TimeParseError from e
