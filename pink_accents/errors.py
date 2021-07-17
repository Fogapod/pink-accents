__all__ = (
    "AccentError",
    "RegexError",
    "BadPattern",
    "BadHandler",
)


class AccentError(Exception):
    """Base exception for all accent errors"""


class BadPattern(AccentError):
    """Something is wrong with replacement pattern"""


class RegexError(BadPattern):
    """Regex did not compile"""


class BadHandler(AccentError):
    """Something is wrong with replacement handler"""
