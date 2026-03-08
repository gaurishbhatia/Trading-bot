# logging_config.py - sets up file + console logging

import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
LOG_FILE = os.path.join(LOG_DIR, "trading_bot.log")

_initialized = False


def setup_logging():
    """
    Call this once at startup. Sets up two handlers:
    - console: INFO level, short format
    - file: DEBUG level, detailed format, 5MB rotation
    """
    global _initialized
    if _initialized:
        return

    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)

    # file handler - captures everything including debug
    os.makedirs(LOG_DIR, exist_ok=True)
    fh = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=3)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(module)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    logger.addHandler(fh)

    # console handler - just the important stuff
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
    ))
    logger.addHandler(ch)

    _initialized = True
