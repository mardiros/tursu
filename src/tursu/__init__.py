"""
Run Gherkin test easilly.
"""
from importlib import metadata

from .compile_all import generate_tests
from .registry import StepRegistry, given, then, when

__version__ = metadata.version("tursu")

__all__ = [
    "given",
    "when",
    "then",
    "StepRegistry",
    "generate_tests",
]
