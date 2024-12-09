"""Ultimate Notion provides a pythonic, high-level API for Notion

Notion-API: https://developers.notion.com/reference/intro
"""

from importlib.metadata import PackageNotFoundError, version

from cronspell.cronspell import Cronspell
from cronspell.parse import parse

try:
    __version__ = version("cronspell")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError


__all__ = ["Cronspell", "parse"]
