from abc import ABC, abstractmethod


class Logger(ABC):
    """Define la interfaz para cualquier logger que la aplicación pueda usar."""
    @abstractmethod
    def info(self, message: str):
        pass

    @abstractmethod
    def debug(self, message: str):
        pass

    @abstractmethod
    def warning(self, message: str):
        pass

    @abstractmethod
    def error(self, message: str):
        pass
