import random

from typing import Generator

from pink_accents import Match, Accent, ReplacementContext

CURSED_ES = "EĒÊËÈÉ"


def cursed_e_generator(count: int) -> Generator[str, None, None]:
    yield from random.choices(CURSED_ES, k=count)


def next_cursed_e(ctx: ReplacementContext) -> str:
    if ctx.state is None:
        # this is a little hack for knowing the amount of e's we will need ahead of time.
        # this number will usually be greater than the actual amount of e's used because
        # not all letters are replaced, but the advantage is using random.choices only
        # once
        ctx.state = cursed_e_generator(len(ctx.source))

    return next(ctx.state)


def e(m: Match) -> str:
    if m.severity < 5:
        return "e" if m.original.islower() else "E"

    elif m.severity < 10:
        return "E"

    return next_cursed_e(m.context)


class E(Accent):
    PATTERNS = {
        r"[a-z]": e,
    }

    @classmethod
    @property
    def description(cls) -> str:
        """Accent description for user."""

        return "Eeeeee eeeeeeeeeee eee eeee."
