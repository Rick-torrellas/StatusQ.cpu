import logging

from src.ports import Logger


class AppLogger(Logger):
    """A Logger port implementation that uses Python's standard logging library."""

    def __init__(self, name: str):
        # Initialize internal logger instance by acquiring a logger
        # with the specified name from the logging module
        self._logger = logging.getLogger(name)

    def info(self, message: str):
        # Delegate info-level logging to the underlying logger instance
        self._logger.info(message)

    def debug(self, message: str):
        # Delegate debug-level logging to the underlying logger instance
        self._logger.debug(message)

    def warning(self, message: str):
        # Delegate warning-level logging to the underlying logger instance
        self._logger.warning(message)

    def error(self, message: str):
        # Delegate error-level logging to the underlying logger instance
        self._logger.error(message)
