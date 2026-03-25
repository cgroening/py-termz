# termz

Terminal utilities for CLI, TUI, IO and general use.

```
pip install termz
```

> **Status:** early alpha — API is unstable.

---

## Modules

### `termz.cli` — Styled output & prompts

```python
from termz.cli import success, error, warn, info, confirm

success("Build complete")
warn("Deprecated flag used")
error("Something went wrong")
info("Listening on port 8080")

if confirm("Continue?", default=True):
    ...
```

### `termz.tui` — Spinner

```python
from termz.tui import Spinner
import time

with Spinner("Loading data..."):
    time.sleep(2)
```

### `termz.io` — stdin & file helpers

```python
from termz.io import is_piped, read_stdin, read_file, write_file

if is_piped():
    data = read_stdin()

content = read_file("config.toml")
write_file("output/result.txt", "done")
```

### `termz.utils` — General utilities

```python
from termz.utils import terminal_size, truncate, slugify, platform_name

cols, lines = terminal_size()
print(truncate("A very long string", width=12))  # "A very lo..."
print(slugify("Hello, World!"))                  # "hello-world"
print(platform_name())                           # "macos"
```

---

## Requirements

- Python 3.10+
- No external dependencies

## License

MIT
