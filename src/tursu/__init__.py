"""
Easily run Gherkin tests.
"""

from importlib import metadata

from .registry import given, then, when

__version__ = metadata.version("tursu")

__all__ = [
    "given",
    "when",
    "then",
]
