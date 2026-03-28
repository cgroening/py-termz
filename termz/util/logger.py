import logging
from pathlib import Path

def setup_logging(appname: str, level: int = logging.DEBUG) -> None:
    log_dir = Path.home() / ".local" / "state" / appname
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "app.log"

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
        ],
    )
