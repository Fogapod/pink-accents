import re
import sys

from typing import Dict, Type

from . import load_samples
from .accent import Accent

# never actually used
USAGE = f"""python -m {__package__} [accent...]

Starts interactive session if used without arguments.
Lists accents if no accents provided.

Accent severity can optionally be passed in square brackets: OwO[10]
"""


def main() -> None:
    load_samples()

    all_accents: Dict[str, Type[Accent]] = {a.name: a for a in sorted(Accent.get_all_accents(), key=lambda a: a.name)}  # type: ignore

    if len(sys.argv) == 1:
        longest = max(len(a.name) for a in all_accents.values())  # type: ignore

        for i in all_accents.values():
            print(f"{i.name:>{longest + 1}}: {i.description or 'Unknown'}")

        sys.exit(0)

    accents = set()
    for arg in sys.argv[1:]:
        if not (match := re.fullmatch(r"(\w+)(:?\[(\d+)\])?", arg)):
            print(f"Warning: Unable to recognize accent: {arg}")

            continue

        name, severity = match.group(1, 3)

        if severity is None:
            severity_int = 1  # thanks mypy
        else:
            severity_int = int(severity)

        try:
            accent_cls = all_accents[name]
        except KeyError:
            print(f"Warning: Skipping unknown accent: {arg}")
        else:
            accents.add(accent_cls(severity_int))

    if not accents:
        print("No accents matched, exiting")
        sys.exit(1)

    while True:
        try:
            text = input("> ")
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)

        for accent in accents:
            text = accent.apply(text)

        print(text)


if __name__ == "__main__":
    main()
