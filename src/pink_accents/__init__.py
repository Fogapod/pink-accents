import importlib
import sys

from pathlib import Path

from .accent import Accent
from .context import ReplacementContext
from .match import Match
from .replacement import Replacement

__version__ = "0.1.0"

__all__ = (
    "Match",
    "Accent",
    "ReplacementContext",
    "Replacement",
    "load_examples",
    "load_from",
)


def load_examples() -> None:
    """Load sample accents"""

    # either installed package or local source folder
    pkg_root = Path(__file__).parent.parent

    load_from(pkg_root.joinpath("examples"))


def load_from(path: Path) -> None:
    """Load accents from path."""

    path_str = str(path)
    sys.path.insert(0, path_str)

    try:
        for child in path.iterdir():
            if child.suffix != ".py":
                continue

            if child.name.startswith("_"):
                continue

            importlib.import_module(child.stem, package=path_str)
    finally:
        sys.path.remove(path_str)
