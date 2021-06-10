from pink_accents import Accent

from ._shared import DISCORD_MESSAGE_END


class Scotsman(Accent):
    PATTERNS = {
        DISCORD_MESSAGE_END: {
            " ye daft cunt": 0.5,
        }
    }
