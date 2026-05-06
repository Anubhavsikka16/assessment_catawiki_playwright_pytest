import logging
import os
import time


class Logger:

    def __init__(self, logger_name, file_level=logging.INFO):

        # Create logger
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        # Prevent duplicate logs
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # Create logs directory automatically
        os.makedirs("logs", exist_ok=True)

        # Log file name
        curr_time = time.strftime("%Y-%m-%d")
        self.log_file_name = f"logs/log_{curr_time}.txt"

        # Formatter
        fmt = logging.Formatter(
            '%(asctime)s - %(filename)s:[%(lineno)s] - [%(levelname)s] - %(message)s'
        )

        # File handler
        fh = logging.FileHandler(self.log_file_name, mode="a")
        fh.setFormatter(fmt)
        fh.setLevel(file_level)

        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        ch.setLevel(file_level)

        # Add handlers
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger