"""
Centralized logging configuration for the SpamShield backend.

Writes structured, rotating log files to the `logs/` folder so that
all application activity is stored in files rather than only being
printed to the terminal.

Log files:
    logs/app.log            - Application runtime log (all levels)
    logs/error.log          - Errors and warnings only
    logs/access.log         - HTTP request access log
    logs/ml.log             - Machine learning pipeline activity
"""
import os
import logging
import logging.handlers
from datetime import datetime
from pathlib import Path

# Directory where all log files are stored (repo root /logs)
# logging_config.py lives at backend/app/core/, so 4 parents up = repo root
LOGS_DIR = Path(__file__).resolve().parent.parent.parent.parent / "logs"

FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def ensure_logs_dir() -> Path:
    """Create the logs directory if it does not exist."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    return LOGS_DIR


def _rotating_handler(filename: str, level: int = logging.INFO) -> logging.handlers.RotatingFileHandler:
    """Build a rotating file handler that keeps log files size-managed."""
    ensure_logs_dir()
    handler = logging.handlers.RotatingFileHandler(
        LOGS_DIR / filename,
        maxBytes=5 * 1024 * 1024,  # 5 MB per file
        backupCount=5,             # keep 5 rotated files
        encoding="utf-8",
    )
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(FORMAT, datefmt=DATE_FORMAT))
    return handler


def setup_logging(log_to_console: bool = False, level: int = logging.INFO) -> None:
    """
    Configure application-wide logging to write into rotating log files.
    Only touches the spamshield logger — leaves uvicorn's root handlers alone.
    """
    app_logger = logging.getLogger("spamshield")
    app_logger.setLevel(level)
    # Remove existing rotating handlers to avoid duplicates on re-call
    app_logger.handlers = [
        h for h in app_logger.handlers
        if not isinstance(h, logging.handlers.RotatingFileHandler)
    ]

    app_logger.addHandler(_rotating_handler("app.log", level))
    app_logger.addHandler(_rotating_handler("error.log", logging.ERROR))

    if log_to_console and not any(isinstance(h, logging.StreamHandler) and not isinstance(h, logging.handlers.RotatingFileHandler) for h in app_logger.handlers):
        console = logging.StreamHandler()
        console.setLevel(level)
        console.setFormatter(logging.Formatter(FORMAT, datefmt=DATE_FORMAT))
        app_logger.addHandler(console)

    for noisy in ("uvicorn.access", "httpx", "urllib3", "sqlalchemy.engine"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


def get_ml_logger() -> logging.Logger:
    """Return a dedicated logger for the ML pipeline writing to ml.log."""
    logger = logging.getLogger("spamshield.ml")
    logger.setLevel(logging.INFO)
    # Only attach the ML file handler if not already present
    if not any(
        isinstance(h, logging.handlers.RotatingFileHandler) and getattr(h, "baseFilename", "").endswith("ml.log")
        for h in logger.handlers
    ):
        ensure_logs_dir()
        handler = logging.handlers.RotatingFileHandler(
            LOGS_DIR / "ml.log",
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter(FORMAT, datefmt=DATE_FORMAT))
        logger.addHandler(handler)
        logger.propagate = False
    return logger


def make_http_request_logger() -> logging.Logger:
    """Provide a dedicated access logger writing to access.log."""
    logger = logging.getLogger("spamshield.access")
    logger.setLevel(logging.INFO)
    if not any(
        isinstance(h, logging.handlers.RotatingFileHandler) and getattr(h, "baseFilename", "").endswith("access.log")
        for h in logger.handlers
    ):
        logger.addHandler(_rotating_handler("access.log", logging.INFO))
        logger.propagate = False
    return logger


def log_current_boot(log_to_console: bool = False) -> None:
    """Record a boot marker in the log file for easier session tracking."""
    setup_logging(log_to_console=log_to_console)
    logging.getLogger("spamshield").info(
        "=== SpamShield backend started at %s ===", datetime.now().isoformat()
    )
    logging.getLogger("spamshield").info("Listening on port %s", os.environ.get("PORT", "8000"))
