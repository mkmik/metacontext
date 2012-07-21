#!/usr/bin/env python
from setuptools import setup, find_packages
from version import get_git_version


setup(
    name = "metacontext",
    version = get_git_version(),
    description = """Metaprogramming with context managers""",
    long_description = open('README.rst').read(),
    author = "Marko Mikulicic",
    author_email = "mmikulicic@gmail.com",
    classifiers = ['License :: OSI Approved :: BSD License',
                   'Intended Audience :: Developers',
                   'Topic :: Software Development :: Libraries',
                   'Topic :: Software Development :: Compilers',
                   'Topic :: Software Development :: Code Generators',
                   'Topic :: Software Development :: Pre-processors',
        ],
    url = "https://github.com/mmikulicic/metacontext",
    packages = find_packages(),
    install_requires = []
)
