import re

import pytest

from pink_accents.match import Match
from pink_accents.accent import Accent
from pink_accents.context import ReplacementContext
from pink_accents.replacement import Replacement


@pytest.mark.parametrize("test_accent", [1], indirect=True)
def test_match(test_accent: Accent) -> None:
    source_str = "123"

    re_match = re.match(r"\d+", source_str)

    assert re_match

    match = Match(
        match=re_match,
        severity=1,
        context=ReplacementContext(None, source_str, test_accent),
    )

    assert match.original == source_str


@pytest.mark.parametrize("test_accent", [1], indirect=True)
def test_metadata(test_accent: Accent) -> None:
    assert test_accent.name == "TestAccent"
    assert test_accent.full_name == "TestAccent"
    assert str(test_accent) == "TestAccent"
    assert test_accent.description == ""

    test_accent.severity = 2

    assert test_accent.full_name == "TestAccent[2]"


@pytest.mark.parametrize("test_accent", [1], indirect=True)
def test_basic_replace(test_accent: Accent) -> None:
    assert test_accent.apply("hi foobaz") == "hello barbaz"


@pytest.mark.parametrize("test_accent", [1], indirect=True)
def test_replace_with_limit(test_accent: Accent) -> None:
    assert test_accent.apply("hi", limit=2) == "hi"


def test_accent_registration() -> None:
    assert len(Accent.get_all_accents()) == 0

    class A(Accent):
        pass

    assert len(Accent.get_all_accents()) == 1

    class B(Accent):
        pass

    assert len(Accent.get_all_accents()) == 2

    Accent.clear_accents()

    assert len(Accent.get_all_accents()) == 0


def test_global_vars() -> None:
    class A(Accent):
        WORDS = {r"hi": "hello"}

    a = A()

    assert a.apply("hithere hi abchi") == "hithere hello abchi"

    class B(Accent):
        PATTERNS = {r"\d": "-"}

    b = B()

    assert b.apply("abc123def4") == "abc---def-"

    class C(Accent):
        REPLACEMENTS = [Replacement(r"o+", "a")]

    c = C()

    assert c.apply("oooo-bbb-o") == "a-bbb-a"

    Accent.clear_accents()


@pytest.mark.parametrize("test_accent", [2], indirect=True)
def test_replace(test_accent) -> None:
    assert test_accent.apply("sequence") in ("seq_1", "seq_2")
    assert test_accent.apply("sequence_callable") in (
        "sequence_callable1",
        "sequence_callable2",
    )
    assert test_accent.apply("map_ints") in ("map_ints1", "map_ints2")
    assert test_accent.apply("map_floats") in ("map_floats1", "map_floats")
    assert test_accent.apply("map_callable") == "map_callable1"
    assert test_accent.apply("map_key_callable") == "map_key_callable1"
    assert test_accent.apply("callable") == "callable-2"


@pytest.mark.parametrize("test_accent", [1], indirect=True)
def test_case_adjust_replace(test_accent) -> None:
    assert test_accent.apply("foo") == "bar"
    assert test_accent.apply("Foo") == "Bar"
    assert test_accent.apply("FOO") == "BAR"
