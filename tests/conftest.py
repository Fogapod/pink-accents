import re

from typing import Generator

import pytest

from pink_accents.accent import Accent


@pytest.fixture
def test_accent(request) -> Generator[Accent, None, None]:
    class TestAccent(Accent):
        PATTERNS = {
            re.compile(r"foo", re.IGNORECASE): "bar",
        }
        WORDS = {
            r"hi": "hello",
            r"sequence": ("seq_1", "seq_2"),
            r"sequence_callable": (
                lambda m: "sequence_callable1",
                lambda m: "sequence_callable2",
            ),
            r"map_ints": {"map_ints1": 1, "map_ints2": 2},
            r"map_floats": {"map_floats1": 0.25},
            r"map_callable": {"map_callable1": lambda s: 42},
            r"map_key_callable": {lambda m: "map_key_callable1": 1},
            r"callable": lambda m: f"callable-{m.severity}",
        }

    yield TestAccent(request.param)

    Accent.clear_accents()
