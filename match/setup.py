#!/usr/bin/env python
from setuptools import setup, find_packages
from version import get_git_version


setup(
    name = "metacontext.match",
    version = get_git_version(),
    description = """Example match/case statement for metacontext""",
    author = "Marko Mikulicic",
    author_email = "mmikulicic@gmail.com",
    packages = find_packages(),
    entry_points = {'console_scripts': ['demo = matchkeyword.demo:run']},
    install_requires = ['metacontext']
)
