import random

from pink_accents import Accent

from ._shared import DISCORD_MESSAGE_END


class Spurdo(Accent):
    PATTERNS = {
        r"xc": "gg",
        r"c": "g",
        r"k": "g",
        r"t": "d",
        r"p": "b",
        r"x": "gs",
        r"\Bng\b": "gn",
        r":?\)+": lambda m: f":{'D' * len(m.original) * (random.randint(1, 5) + m.severity)}",
        DISCORD_MESSAGE_END: {
            lambda m: f" :{'D' * (random.randint(1, 5)+ m.severity)}": 0.5,
        },
    }

    WORDS = {
        r"epic": "ebin",
    }
