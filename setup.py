import os
import re

from typing import Sequence

import setuptools  # type: ignore

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

init_py = os.path.join(os.path.dirname(__file__), "pink_accents", "__init__.py")

with open(init_py) as f:
    cont = f.read()

    str_regex = r"['\"]([^'\"]*)['\"]"
    try:
        version = re.findall(rf"^__version__ = {str_regex}$", cont, re.MULTILINE)[0]
    except IndexError:
        raise RuntimeError(f"Unable to find version in {init_py}")

    try:
        author = re.findall(rf"^__author__ = {str_regex}$", cont, re.MULTILINE)[0]
    except IndexError:
        raise RuntimeError(f"Unable to find author in {init_py}")

install_requires: Sequence[str] = []

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: Implementation :: CPython",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Topic :: Text Processing",
    "Typing :: Typed",
]

setuptools.setup(
    name="pink_accents",
    version=version,
    author=author,
    author_email="fogaprod@gmail.com",
    description="Accent system based on string pattern matching",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Fogapod/pink-accents",
    install_requires=install_requires,
    python_requires=">=3.9",
    packages=setuptools.find_packages(),
    package_data={"pink_accents": ["py.typed"]},
    license="MIT",
    classifiers=classifiers,
)
