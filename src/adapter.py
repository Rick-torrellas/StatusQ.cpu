import logging
from src.ports import Logger

class AppLogger(Logger):
    """Una implementación del Logger port que usa la librería estándar de logging de Python."""
    def __init__(self, name: str):
        self._logger = logging.getLogger(name)

    def info(self, message: str):
        self._logger.info(message)

    def debug(self, message: str):
        self._logger.debug(message)

    def warning(self, message: str):
        self._logger.warning(message)

    def error(self, message: str):
        self._logger.error(message)
