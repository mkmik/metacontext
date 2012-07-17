#!/usr/bin/env python
from setuptools import setup, find_packages
from version import get_git_version


setup(
    name = "metacontext",
    version = get_git_version(),
    description = """Metaprogramming with context managers""",
    author = "Marko Mikulicic",
    author_email = "mmikulicic@gmail.com",
    packages = find_packages(),
    install_requires = []
)
