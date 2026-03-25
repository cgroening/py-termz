"""General-purpose terminal and string utilities."""

from __future__ import annotations

import os
import re
import shutil
import sys
from typing import NamedTuple


class TerminalSize(NamedTuple):
    columns: int
    lines: int


def terminal_size() -> TerminalSize:
    """Return the current terminal dimensions.

    Falls back to ``(80, 24)`` when the size cannot be determined (e.g. in
    pipes or CI environments).
    """
    size = shutil.get_terminal_size(fallback=(80, 24))
    return TerminalSize(columns=size.columns, lines=size.lines)


def truncate(text: str, width: int, placeholder: str = "...") -> str:
    """Truncate *text* to *width* characters, appending *placeholder* if cut.

    Args:
        text: Input string.
        width: Maximum character count including the placeholder.
        placeholder: Suffix added when the text is truncated (default ``"..."``).

    Returns:
        The (possibly truncated) string.
    """
    if len(text) <= width:
        return text
    cut = width - len(placeholder)
    if cut <= 0:
        return placeholder[:width]
    return text[:cut] + placeholder


def slugify(text: str) -> str:
    """Convert *text* to a URL/filename-friendly slug.

    Example::

        slugify("Hello, World!")  # -> "hello-world"
    """
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-")


def platform_name() -> str:
    """Return a short human-readable platform string: ``linux``, ``macos``, or ``windows``."""
    p = sys.platform
    if p.startswith("linux"):
        return "linux"
    if p == "darwin":
        return "macos"
    if p in ("win32", "cygwin"):
        return "windows"
    return p


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("cls" if sys.platform == "win32" else "clear")
