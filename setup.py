#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="python-snake-game",
    version="1.0.0",
    author="Kerlann",
    author_email="kerlann@example.com",
    description="Un jeu Snake classique développé en Python avec Pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kerlann/python-snake-game",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment :: Arcade",
        "Development Status :: 5 - Production/Stable",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "snake-game=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["assets/**/*", "docs/**/*"],
    },
)
