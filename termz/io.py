"""IO helpers — stdin, file reading, and stream detection."""

from __future__ import annotations

import sys
from pathlib import Path


def is_piped() -> bool:
    """Return ``True`` if stdin is connected to a pipe or redirect (not a TTY)."""
    return not sys.stdin.isatty()


def read_stdin() -> str:
    """Read all of stdin and return it as a string.

    Useful when data is piped into the script::

        echo "hello" | python -c "from termz.io import read_stdin; print(read_stdin())"
    """
    return sys.stdin.read()


def read_file(path: str | Path, encoding: str = "utf-8") -> str:
    """Read a text file and return its contents.

    Args:
        path: Path to the file.
        encoding: File encoding (default ``utf-8``).

    Returns:
        The file contents as a string.

    Raises:
        FileNotFoundError: If *path* does not exist.
    """
    return Path(path).read_text(encoding=encoding)


def write_file(path: str | Path, content: str, encoding: str = "utf-8") -> None:
    """Write *content* to a text file, creating parent directories as needed.

    Args:
        path: Destination path.
        content: Text to write.
        encoding: File encoding (default ``utf-8``).
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding=encoding)
