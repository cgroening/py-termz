"""TUI components — spinners and simple interactive elements."""

from __future__ import annotations

import itertools
import sys
import threading
import time
from types import TracebackType
from typing import Iterator


_SPINNER_FRAMES = ("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏")
_DONE_MARK = ""
_FAIL_MARK = ""


class Spinner:
    """A non-blocking terminal spinner for long-running operations.

    Usage::

        with Spinner("Loading..."):
            time.sleep(2)

        with Spinner("Processing") as s:
            do_work()
            s.text = "Almost done..."
    """

    def __init__(
        self,
        text: str = "Working...",
        *,
        interval: float = 0.08,
        stream: "object" = sys.stdout,
    ) -> None:
        self.text = text
        self.interval = interval
        self._stream = stream
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._success = True

    # ------------------------------------------------------------------
    def _spin(self) -> None:
        frames: Iterator[str] = itertools.cycle(_SPINNER_FRAMES)
        while not self._stop_event.is_set():
            frame = next(frames)
            line = f"\r{frame}  {self.text}"
            self._stream.write(line)  # type: ignore[attr-defined]
            self._stream.flush()  # type: ignore[attr-defined]
            time.sleep(self.interval)

    def start(self) -> "Spinner":
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()
        return self

    def stop(self, *, ok: bool = True) -> None:
        self._success = ok
        self._stop_event.set()
        if self._thread:
            self._thread.join()
        mark = _DONE_MARK if ok else _FAIL_MARK
        self._stream.write(f"\r{mark}  {self.text}\n")  # type: ignore[attr-defined]
        self._stream.flush()  # type: ignore[attr-defined]

    # context manager --------------------------------------------------
    def __enter__(self) -> "Spinner":
        return self.start()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.stop(ok=exc_type is None)
