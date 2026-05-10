"""
Centralised logging configuration.
All modules import the logger from here for consistent formatting.
"""
import logging
import sys
from app.config import settings


def setup_logger(name: str) -> logging.Logger:
    """Return a configured logger for the given module name."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    level = logging.DEBUG if settings.APP_ENV == "development" else logging.INFO
    logger.setLevel(level)

    return logger

# Create a default logger instance for general use
logger = setup_logger("app")
