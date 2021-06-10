from __future__ import annotations

import logging

from typing import Any, Set, Type

from .context import ReplacementContext
from .replacement import Replacement

log = logging.getLogger(__name__)


class Accent:
    """
    Main accent class.

    Each time this class is inherited, child class is registered.

    Accent replacements are defined with WORDS and PATTERNS variables by default.
    Both of these variables are dicts where keys are regular expressions and keys are:
      - strings: for direct replacements
      - handlers: functions acception Match as argument and returning Optional[str]
      - tuples of strings or handlers: one item is selected with equal probabilities
      - dicts where keys are strings or handlers and values are relative probabilities

    See `ReplacementCB` and children for more info on supported kinds.

    Additional notes:
    In case None is selected, match remains untouched.

    If SUM of dict probabilities < 1, None is added with probability 1 - SUM.
    Dict probabilities can be dynamic, callables accepting int (severity value).

    You can see examples of accents in the `samples` folder. OwO is one of the most
    advanced accents where most features are used.
    """

    _replacements: Set[Replacement]

    __registered_accents: Set[Type[Accent]] = set()

    def __init_subclass__(cls, register: bool = True):
        super().__init_subclass__()

        if register:
            log.debug("registering %s", cls)

            if cls in cls.__registered_accents:
                # does this ever happen?
                log.warn(f"{cls} is already present in accents")

            cls.__registered_accents.add(cls)

    @classmethod
    def get_all_accents(cls) -> Set[Type[Accent]]:
        """Get all registered accent types."""

        return cls.__registered_accents

    @classmethod
    def clear_accents(cls) -> None:
        """Removes all accents from registry."""

        cls.__registered_accents = set()

    def __init__(self, severity: int = 1) -> None:
        self.severity = severity

        self._replacements = set()

        if (patterns := getattr(self, "WORDS", None)) is not None:
            for k, v in patterns.items():
                self.register_replacement(Replacement(rf"\b{k}\b", v))

        if (patterns := getattr(self, "PATTERNS", None)) is not None:
            for k, v in patterns.items():
                self.register_replacement(Replacement(k, v))

        if (replacements := getattr(self, "REPLACEMENTS", None)) is not None:
            for replacement in replacements:
                self.register_replacement(replacement)

    def register_replacement(self, replacement: Replacement) -> None:
        """Add replacement object to internal registry."""

        replacement.severity_hint(self.severity)

        self._replacements.add(replacement)

    @classmethod
    @property
    def name(cls) -> str:
        """Short accent name. Class name by default."""

        return cls.__name__

    @property
    def full_name(self) -> str:
        """Accent name based on short name with additional information like severity."""

        if self.severity == 1:
            return self.name

        return f"{self.name}[{self.severity}]"

    @classmethod
    @property
    def description(cls) -> str:
        """Accent description for user."""

        return ""

    def get_context(
        self,
        *,
        text: str,
        context_id: Any,
        cls: Type[ReplacementContext] = ReplacementContext,
    ) -> ReplacementContext:
        """Context factory."""

        return cls(
            source=text,
            id=context_id,
            accent=self,
        )

    def apply(
        self,
        text: str,
        *,
        limit: int = 2000,
        context_id: Any = None,
    ) -> str:
        """Apply accent to given text."""

        context = self.get_context(text=text, context_id=context_id)

        for replacement in self._replacements:
            text = replacement.apply(
                text,
                severity=self.severity,
                limit=limit,
                context=context,
            )

        return text

    def __str__(self) -> str:
        return self.full_name

    def __repr__(self) -> str:
        return f"<{self.full_name} replacements={self._replacements}>"
