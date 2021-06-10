import re

from .context import ReplacementContext

__all__ = ("Match",)


class Match:
    """
    Contains information about current match. Passed to every handler function.
    """

    __slots__ = (
        "match",
        "severity",
        "context",
    )

    def __init__(
        self, *, match: re.Match[str], severity: int, context: ReplacementContext
    ) -> None:
        self.match = match
        self.severity = severity
        self.context = context

    @property
    def original(self) -> str:
        """Original text that is being replaced"""

        return self.match[0]

    def __repr__(self) -> str:
        return f"<{type(self).__name__} match={self.match} severity={self.severity} context={self.context}>"
