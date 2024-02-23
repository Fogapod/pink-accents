from typing import Any

from pink_accents import Accent


class Reversed(Accent):
    """.txet sesreveR"""

    def apply(self, text: str, **_: Any) -> str:
        return text[::-1]
