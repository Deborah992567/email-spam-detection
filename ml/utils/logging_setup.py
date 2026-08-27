"""
Logging setup for the ML module.

Writes rotating log files to the project `logs/` folder so that all
machine-learning activity (training, prediction, evaluation) is stored
in files rather than only printed to the terminal.

Log file: logs/ml.log
"""
import logging
import logging.handlers
from pathlib import Path

# Project root: ml/ -> project_root is the repo root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"

FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_ml_logger(name: str = "spamshield.ml") -> logging.Logger:
    """Return a configured ML logger that writes to logs/ml.log."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not any(
        isinstance(h, logging.handlers.RotatingFileHandler)
        and getattr(h, "baseFilename", "").endswith("ml.log")
        for h in logger.handlers
    ):
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        handler = logging.handlers.RotatingFileHandler(
            LOGS_DIR / "ml.log",
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=5,
            encoding="utf-8",
        )
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter(FORMAT, datefmt=DATE_FORMAT))
        logger.addHandler(handler)
        logger.propagate = False

    return logger
