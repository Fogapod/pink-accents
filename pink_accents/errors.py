__all__ = (
    "AccentError",
    "ConfigurationError",
    "RegexError",
    "BadPattern",
    "BadHandler",
    "BadSeverity",
)


class AccentError(Exception):
    """Base exception for all accent errors"""


class ConfigurationError(AccentError):
    """Base exception for all configuration errors"""


class BadPattern(ConfigurationError):
    """Something is wrong with replacement pattern"""


class RegexError(BadPattern):
    """Regex did not compile"""


class BadHandler(ConfigurationError):
    """Something is wrong with replacement handler"""


class BadSeverity(ConfigurationError):
    """Severity value check failed"""
