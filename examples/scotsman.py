from pink_accents import Accent


class Scotsman(Accent):
    """Somewhat rude accent."""

    PATTERNS = {
        r"\Z": {
            " ye daft cunt": lambda s: 0.4 + (0.6 * s / 9),
        }
    }
