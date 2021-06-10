import importlib

from pathlib import Path

from .match import Match
from .accent import Accent
from .context import ReplacementContext
from .replacement import Replacement

__version__ = "0.0.1"
__author__ = "Fogapod"

__all__ = (
    "Match",
    "Accent",
    "ReplacementContext",
    "Replacement",
    "load_samples",
    "load_from",
)


def load_samples() -> None:
    """Load sample accents"""

    load_from(f"{__package__}.samples")


def load_from(path: str) -> None:
    """Load accents from path. Path is joined by `.`."""

    joined_path = Path(__file__).parent.parent.joinpath(
        *[Path(p) for p in path.split(".")]
    )

    for child in joined_path.iterdir():
        if child.suffix != ".py":
            continue

        if child.name.startswith("_"):
            continue

        importlib.import_module(f"{path}.{child.stem}")
