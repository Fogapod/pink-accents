__all__ = (
    "AccentError",
    "ConfigurationError",
    "RegexError",
    "BadPatternError",
    "BadHandlerError",
    "BadSeverityError",
)


class AccentError(Exception):
    """Base exception for all accent errors"""


class ConfigurationError(AccentError):
    """Base exception for all configuration errors"""


class BadPatternError(ConfigurationError):
    """Something is wrong with replacement pattern"""


class RegexError(BadPatternError):
    """Regex did not compile"""


class BadHandlerError(ConfigurationError):
    """Something is wrong with replacement handler"""


class BadSeverityError(ConfigurationError):
    """Severity value check failed"""
