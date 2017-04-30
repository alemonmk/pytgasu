# Always prefer setuptools over distutils
from setuptools import setup

setup(setup_requires=['setuptools>=30.3.0'], entry_points={'console_scripts': ['pytgasu=pytgasu.cli:cli']})
