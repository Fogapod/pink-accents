from __future__ import annotations

import re
import random
import itertools

from typing import Any, Tuple, Union, Optional, Sequence

from .match import Match
from .types import (
    ReplacementType,
    DynamicWeightFnType,
    ReplacementDictType,
    ReplacementCallableType,
    ReplacementSequenceType,
)
from .context import ReplacementContext

__all__ = ("Replacement",)


class ReplacementCB:
    __slots__ = ("replacement",)

    @classmethod
    def from_replacement(
        cls, replacement: ReplacementType, **kwargs: Any
    ) -> ReplacementCB:
        if isinstance(replacement, str):
            cls = StaticReplacementCB
        elif isinstance(replacement, Sequence):
            cls = SequenceReplacementCB
        elif isinstance(replacement, dict):
            cls = DictReplacementCB
        else:
            # assume callable
            # TODO: check
            cls = CallableReplacementCB

        return cls(replacement, **kwargs)

    def __init__(self, replacement: Any, **kwargs: Any):
        self.replacement = replacement

    def severity_hint(self, severity: int) -> None:
        """
        Called when replacement is registered. Can be useful to precompute something.
        """

        pass

    def replace(self, match: Match) -> Optional[str]:
        """Actual replacing function."""

        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<{type(self).__name__}>"


class StaticReplacementCB(ReplacementCB):
    """Plain string."""

    replacement: str

    def replace(self, match: Match) -> Optional[str]:
        return self.replacement


class SequenceReplacementCB(ReplacementCB):
    """
    Sequence of equally weighted items.

    Items could be one of:
      - string
      - None
      - callable, accepting match
    """

    replacement: ReplacementSequenceType

    def replace(self, match: Match) -> Optional[str]:
        selected = random.choice(self.replacement)

        if isinstance(selected, str) or selected is None:
            return selected

        return selected(match)


class DictReplacementCB(ReplacementCB):
    """
    Dict of weighted items. Key is item and value is weight.

    Items could be one of:
      - string
      - None
      - callable, accepting match

    Weights could be one of:
      - int: relative weights
      - float: relative weights, None is added if weigh sum is < 1 to compensate for 1.0
      - callable, accepting severity and returning float. assumed to be unstable unless
        `is_stable` is True
    """

    __slots__ = (
        "is_stable",
        "items",
        "weights",
        "computable_weights",
        "cum_weights",
    )

    replacement: ReplacementDictType

    def __init__(self, replacemen: ReplacementDictType, is_stable: bool = False):
        super().__init__(replacemen)

        # TODO: make use of this
        self.is_stable = is_stable

    def severity_hint(self, severity: int) -> None:
        self.items = list(self.replacement.keys())

        computed_weights = []

        self.computable_weights: Sequence[Tuple[int, DynamicWeightFnType]] = []

        for i, v in enumerate(self.replacement.values()):
            if isinstance(v, (int, float)):
                computed_weights.append(v)
            else:
                # assume is a callable
                # TODO: proper check
                self.computable_weights.append((i, v))

                # compute for current severity, fail early for ease of debugging
                #
                # TODO: stable/unstable concept? precompute for current severity?
                computed_weights.append(v(severity))

        self.weights = computed_weights

        if not self.computable_weights:
            # inject None if total weight is < 1 for convenience
            # example: {"a": 0.25, "b": 0.5} -> {"a": 0.25, "b": 0.5, None: 0.25}
            if (weights_sum := sum(computed_weights)) < 1:
                self.items.append(None)
                computed_weights.append(1 - weights_sum)

        # is only useful when there are no computable weights
        # computed as early optimization
        # https://docs.python.org/3/library/random.html#random.choices
        self.cum_weights = list(itertools.accumulate(computed_weights))

    def replace(self, match: Match) -> Optional[str]:
        if self.computable_weights:
            for index, fn in self.computable_weights:
                self.weights[index] = fn(match.severity)

            selected = random.choices(self.items, weights=self.weights)[0]
        else:
            selected = random.choices(self.items, cum_weights=self.cum_weights)[0]

        if isinstance(selected, str) or selected is None:
            return selected

        return selected(match)


class CallableReplacementCB(ReplacementCB):
    """Function accepting match object and returning optional string."""

    replacement: ReplacementCallableType

    def replace(self, match: Match) -> Optional[str]:
        # error: Invalid self argument "CallableReplacementCB" to attribute function "replacement" with type "Callable[[Match], Optional[str]]"
        # error: Too many arguments
        #
        # i cannot understand this stupid mypy error. it goes away if i remove
        # replacement annotation
        return self.replacement(match)  # type: ignore


class Replacement:
    """Defines pattern applied callback."""

    __slots__ = (
        "pattern",
        "callback",
        "case_correction_fn",
    )

    def __init__(
        self,
        pattern: Union[str, re.Pattern[str]],
        replacement: ReplacementType,
        *,
        flags: Any = re.IGNORECASE,
        adjust_case: bool = True,
        **kwargs: Any,
    ):
        if isinstance(pattern, re.Pattern):
            self.pattern = pattern
        else:
            self.pattern = re.compile(pattern, flags)

        self.callback = ReplacementCB.from_replacement(replacement, **kwargs)
        self.case_correction_fn = (
            self._case_adjust if adjust_case else self._no_case_adjust
        )

    def severity_hint(self, severity: int) -> None:
        """
        Called when replacement is registered. Propagated to callback.
        """

        self.callback.severity_hint(severity)

    def apply(
        self, text: str, *, severity: int, limit: int, context: ReplacementContext
    ) -> str:
        """Apply callback to all occurrences of pattern."""

        result_len = len(text)

        def repl(match: re.Match[str]) -> str:
            nonlocal result_len

            original = match[0]

            if (
                replacement := self.callback.replace(
                    Match(match=match, severity=severity, context=context)
                )
            ) is None:
                return original

            result_len += len(replacement) - len(original)
            if result_len > limit:
                return original

            return self.case_correction_fn(original, replacement)

        return self.pattern.sub(repl, text)

    @staticmethod
    def _no_case_adjust(original: str, replacement: str) -> str:
        return replacement

    @staticmethod
    def _case_adjust(original: str, replacement: str) -> str:
        if original.islower():
            return replacement

        if original.istitle():
            if replacement.islower():
                # if there are some case variations better leave string untouched
                return replacement.title()

        elif original.isupper():
            return replacement.upper()

        return replacement

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.pattern} => {self.callback}>"
