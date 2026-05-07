"""
Logger Configuration Module

Provides centralized logging configuration for the test suite.
Logs to both console and file with consistent formatting.
"""

import logging
import os
import time


class Logger:
    """
    Custom logger class for test automation.

    Features:
    - Console and file output
    - Automatic log directory creation
    - Duplicate log prevention
    - Consistent formatting across all modules
    """

    def __init__(self, logger_name: str, file_level: int = logging.INFO) -> None:
        """
        Initialize logger with console and file handlers.

        Args:
            logger_name: Name of the logger module
            file_level: Log level for file and console output (default: INFO)
        """
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        # Prevent duplicate logs
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # Create logs directory
        os.makedirs("logs", exist_ok=True)

        # Generate log file with current date
        curr_time = time.strftime("%Y-%m-%d")
        self.log_file_name = f"logs/log_{curr_time}.txt"

        # Log format
        fmt = logging.Formatter(
            "%(asctime)s - %(filename)s:[%(lineno)s] - [%(levelname)s] - %(message)s"
        )

        # File handler
        fh = logging.FileHandler(self.log_file_name, mode="a")
        fh.setFormatter(fmt)
        fh.setLevel(file_level)

        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        ch.setLevel(file_level)

        # Add handlers to logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_logger(self) -> logging.Logger:
        """
        Get the configured logger instance.

        Returns:
            logging.Logger: Configured logger object
        """
        return self.logger