from typing import Any

from pink_accents import Accent


class Binary(Accent):
    def apply(self, text: str, *, severity: int = 1, **kwargs: Any) -> str:
        return "".join(f"{ord(c):08b} " for c in text)
