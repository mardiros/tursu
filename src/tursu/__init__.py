"""
Run Gherkin test easilly.
"""

from importlib import metadata

from .compile_all import generate_tests
from .registry import Tursu, given, then, when

__version__ = metadata.version("tursu")

__all__ = [
    "given",
    "when",
    "then",
    "Tursu",
    "generate_tests",
]
