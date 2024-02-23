# pink-accents

Accent system based on string pattern matching.

This is a silly accent system inspired by Space Station 13 accents, based on popular stereotypes. There is no intent in offending anyone or any culture. Maybe this thing has other uses, we'll see.
In it's core it's basically a re.sub call.

This was a part of PINK Discord bot originally: https://github.com/Fogapod/pink

Examples of accents can be found in `examples` folder.

### Console interface

```sh
usage: pink_accents [-h] [-p ACCENT_PATH] [-V] [accent ...]

Interactive accent session.

Starts interactive session if used without arguments.
Lists accents if no accents provided.

positional arguments:
  accent                accent with severity

options:
  -h, --help            show this help message and exit
  -p ACCENT_PATH, --accent-path ACCENT_PATH
                        where to look for accents, defaults to local example folder
  -V, --version         show program's version number and exit
```
