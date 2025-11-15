"""Custom exception classes for the application."""


class DateTimeParseError(ValueError):
    """Raised when a datetime string cannot be parsed."""

    pass


class DateParseError(ValueError):
    """Raised when a date string cannot be parsed."""

    pass


class TimeParseError(ValueError):
    """Raised when a time string cannot be parsed."""

    pass
