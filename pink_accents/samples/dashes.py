from pink_accents import Accent


class Dashes(Accent):
    """Replaces all spaces with dashes."""

    PATTERNS = {
        r" +": "-",
    }
