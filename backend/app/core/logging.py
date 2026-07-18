"""
Logging configuration for Meesho Udaan.

Call setup_logging() once at application startup in main.py.
After that, every module can use logging.getLogger(__name__)
and get consistently formatted output.
"""

import logging
import sys
from app.core.config import settings


def setup_logging() -> None:
    """
    Configures structured logging for the entire application.

    Format: [LEVEL] timestamp | logger_name | message
    """
    log_level = logging.DEBUG if settings.ENVIRONMENT == "development" else logging.INFO

    formatter = logging.Formatter(
        fmt="%(levelname)-8s %(asctime)s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    # Silence noisy third-party loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)

    logging.info("Logging configured | environment=%s", settings.ENVIRONMENT)