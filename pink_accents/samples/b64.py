from base64 import b64encode
from typing import Any

from pink_accents import Accent


class Base64(Accent):
    def apply(self, text: str, *, severity: int = 1, **kwargs: Any) -> str:
        return b64encode(text.encode()).decode()
