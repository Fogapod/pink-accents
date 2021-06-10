import random

from typing import Optional

from pink_accents import Match, Accent

from ._shared import DISCORD_MESSAGE_END


def bork(m: Match) -> Optional[str]:
    if random.random() * m.severity < 1 / 3:
        return None

    return f" Bork{', bork' * random.randint(0, m.severity)}!"


# https://github.com/unitystation/unitystation/blob/cf3bfff6563f0b3d47752e19021ab145ae318736/UnityProject/Assets/Resources/ScriptableObjects/Speech/Swedish.asset
class Swedish(Accent):
    PATTERNS = {
        r"w": "v",
        r"j": "y",
        r"a": (
            "å",
            "ä",
            "æ",
            "a",
        ),
        r"bo": "bjo",
        r"o": (
            "ö",
            "ø",
            "o",
        ),
        DISCORD_MESSAGE_END: bork,
    }
