"""
Easily run Gherkin tests.
"""

from importlib import metadata

from tursu.entrypoints.plugin import tursu_collect_file
from tursu.runtime.pattern_matcher import RegEx
from tursu.runtime.registry import given, then, when

__version__ = metadata.version("tursu")

__all__ = [
    "given",
    "when",
    "then",
    "RegEx",
    "tursu_collect_file",
]
