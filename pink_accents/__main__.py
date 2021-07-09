import re
import sys
import pathlib
import argparse
import textwrap

from typing import Dict, Type

from . import load_from, __version__, load_examples
from .accent import Accent

parser = argparse.ArgumentParser(
    prog="pink_accents",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
        """\
        Interactive accent session.

        Starts interactive session if used without arguments.
        Lists accents if no accents provided.\
        """
    ),
)
parser.add_argument(
    "accents",
    metavar="accent",
    nargs="*",
    help="accent with severity",
)
parser.add_argument(
    "-p",
    "--accent-path",
    type=pathlib.Path,
    help="where to look for accents, defaults to local example folder",
)
parser.add_argument(
    "-V",
    "--version",
    action="version",
    version=f"%(prog)s {__version__}",
)


def main() -> None:
    args = parser.parse_args()

    if args.accent_path is None:
        load_examples()
    else:
        load_from(args.accent_path)

    all_accents: Dict[str, Type[Accent]] = {a.name.lower(): a for a in sorted(Accent.get_all_accents(), key=lambda a: a.name)}  # type: ignore

    if not args.accents:
        longest = max(len(a.name) for a in all_accents.values())  # type: ignore

        for i in all_accents.values():
            print(f"{i.name:>{longest + 1}}: {i.description or 'Unknown'}")

        sys.exit(0)

    accents = set()
    for arg in args.accents:
        if not (match := re.fullmatch(r"(\w+)(:?\[(\d+)\])?", arg)):
            print(f"Warning: Unable to recognize accent: {arg}")

            continue

        name, severity = match.group(1, 3)

        if severity is None:
            severity_int = 1  # thanks mypy
        else:
            severity_int = int(severity)

        try:
            accent_cls = all_accents[name.lower()]
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
