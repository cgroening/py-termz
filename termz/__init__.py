"""termz — Terminal utilities for CLI, TUI, IO and general use."""

from termz.cli import confirm, error, info, success, warn
from termz.io import is_piped, read_stdin
from termz.tui import Spinner
from termz.utils import terminal_size, truncate

__version__ = "0.1.0"
__all__ = [
    "confirm",
    "error",
    "info",
    "is_piped",
    "read_stdin",
    "Spinner",
    "success",
    "terminal_size",
    "truncate",
    "warn",
]
