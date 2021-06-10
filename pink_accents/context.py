from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .accent import Accent

__all__ = ("ReplacementContext",)


class ReplacementContext:
    """
    Instance of this class is passed to every handler function as a part of Match.

    `id` is an arbitrary identificator of translation source. For example, user id.
    Passed value depends on implementation and might be not set at all (None).

    `state` can be used to store arbitrary accent state. Since every accent get their
    own instance of this context, accent is free to store any information there.

    `source` is original string passed to Accent.apply.
    """

    __slots__ = (
        "id",
        "state",
        "source",
        "accent",
    )

    def __init__(self, id: Any, source: str, accent: "Accent"):
        self.id = id
        self.state: Any = None
        self.source = source
        self.accent = accent

    def __repr__(self) -> str:
        return f"<{type(self).__name__} id={self.id} state={self.state}>"
