"""CLI output helpers — styled print functions and interactive prompts."""

from __future__ import annotations

import sys

# ANSI color codes
_RESET = "\033[0m"
_BOLD = "\033[1m"
_GREEN = "\033[32m"
_YELLOW = "\033[33m"
_RED = "\033[31m"
_CYAN = "\033[36m"
_GREY = "\033[90m"


def _supports_color() -> bool:
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def cprint(text: str, color: str = "", bold: bool = False) -> None:
    """Print *text* with optional ANSI color and bold styling."""
    if not _supports_color():
        print(text)
        return
    prefix = (bold and _BOLD or "") + color
    print(f"{prefix}{text}{_RESET}" if prefix else text)


def success(msg: str) -> None:
    """Print a green success message."""
    cprint(f"  {msg}", color=_GREEN)


def error(msg: str) -> None:
    """Print a red error message to stderr."""
    prefix = (_BOLD + _RED) if _supports_color() else ""
    reset = _RESET if _supports_color() else ""
    print(f"{prefix}  {msg}{reset}", file=sys.stderr)


def warn(msg: str) -> None:
    """Print a yellow warning message."""
    cprint(f"  {msg}", color=_YELLOW)


def info(msg: str) -> None:
    """Print a cyan informational message."""
    cprint(f"  {msg}", color=_CYAN)


def dim(msg: str) -> None:
    """Print a dimmed/grey message."""
    cprint(msg, color=_GREY)


def confirm(prompt: str, default: bool = False) -> bool:
    """Ask a yes/no question and return the boolean answer.

    Args:
        prompt: The question to display.
        default: The value returned when the user presses Enter without input.

    Returns:
        ``True`` for yes, ``False`` for no.
    """
    hint = "[Y/n]" if default else "[y/N]"
    try:
        answer = input(f"{prompt} {hint} ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return False
    if not answer:
        return default
    return answer in ("y", "yes")
