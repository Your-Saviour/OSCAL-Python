# logger.py
import logging
import os
from pythonjsonlogger import jsonlogger  # pip install ls

LOG_FILE = "./logs.log"

# Ensure the directory exists if a path is given
log_dir = os.path.dirname(LOG_FILE)
if log_dir:
    os.makedirs(log_dir, exist_ok=True)


def get_logger(name: str = __name__):
    """
    Returns a configured logger that logs in JSON format
    to both ./logs.log and the console, including script filename.
    """
    logger = logging.getLogger(name)

    # Prevent duplicate handlers if called multiple times
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.DEBUG)

    # JSON formatter including filename
    log_format = "%(asctime)s %(name)s %(levelname)s %(filename)s %(message)s"
    formatter = jsonlogger.JsonFormatter(log_format)

    # File handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)  # capture everything
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # show all logs on console
    console_handler.setFormatter(formatter)

    # Attach handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
