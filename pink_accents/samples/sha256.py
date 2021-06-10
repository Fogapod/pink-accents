from typing import Any
from hashlib import sha256

from pink_accents import Accent


class SHA256(Accent):
    def apply(self, text: str, *, severity: int = 1, **kwargs: Any) -> str:
        return sha256(text.encode()).hexdigest()
