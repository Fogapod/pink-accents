from _shared import DISCORD_MESSAGE_END

from pink_accents import Accent


class Slav(Accent):
    """Russian accent."""

    WORDS = {
        r"my": "our",
        r"friend": "comrade",
        r"(enemy|foe)": "american pig",
        r"(fuck|shit)": (
            "blyat",
            "cyka",
        ),
        r"usa": "американские захватчики",
        r"we are being attacked": "нас атакуют",
    }

    PATTERNS = {
        r"\b(a|the) +": {
            "": 0.5,
        },
        r"\bha": "ga",
        r"e(?!e)": "ye",
        r"th": ("z", "g"),
        r"\Bo?u": ("a", "oo"),
        r"w": "v",
        DISCORD_MESSAGE_END: {
            " blyat": 0.5,
        },
    }
