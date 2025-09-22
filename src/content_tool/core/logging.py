# src/content_tool/core/logging.py
"""Logging configuration for content-tool."""

import logging
import sys
from typing import Optional


def setup_logging(verbose: bool = False, log_file: Optional[str] = None) -> None:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO

    # Create logger
    logger = logging.getLogger("content_tool")
    logger.setLevel(level)

    # Clear existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
