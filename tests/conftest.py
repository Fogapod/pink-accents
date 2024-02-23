import re

from typing import Generator

import pytest

from pink_accents.accent import Accent


class TestAccent(Accent):
    """This is a test accent."""

    PATTERNS = {
        re.compile(r"foo", re.IGNORECASE): "bar",
    }
    WORDS = {
        r"hi": "hello",
        r"sequence": ("seq_1", "seq_2"),
        r"sequence_callable": (
            lambda _: "sequence_callable1",
            lambda _: "sequence_callable2",
        ),
        r"map_ints": {"map_ints1": 1, "map_ints2": 2},
        r"map_floats": {"map_floats1": 0.25},
        r"map_callable": {"map_callable1": lambda _: 42},
        r"map_key_callable": {lambda _: "map_key_callable1": 1},
        r"callable": lambda m: f"callable-{m.severity}",
    }


Accent.clear_accents()


@pytest.fixture
def test_accent(request: pytest.FixtureRequest) -> Generator[Accent, None, None]:
    yield TestAccent(request.param)


@pytest.fixture
def test_accent_cls(request: pytest.FixtureRequest) -> Generator[type[Accent], None, None]:  # noqa: ARG001
    yield TestAccent
