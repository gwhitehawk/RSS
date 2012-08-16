from setuptools import setup
import os.path

from rss import __version__


with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    long_description = readme.read()


classifiers = [
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
]

install_requires = [
]


setup(
    name="rss",
    version=__version__,
    packages=["rss"],
    author="Julian Berman",
    author_email="Julian@GrayVines.com",
    classifiers=classifiers,
    description="RSS, Simply Syndicated",
    license="MIT/X",
    long_description=long_description,
    url="http://github.com/Julian/rss",
    dependency_links=[
        "https://github.com/Julian/treq/tarball/fix-version#egg=treq-dev",
    ],
    install_requires=[
        "feedparser",
        "twisted >= 11.0.0",
        "termcolor >= 1.1.0",
        "treq",
    ]
)
