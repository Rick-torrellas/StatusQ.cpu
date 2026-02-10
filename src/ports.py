from abc import ABC, abstractmethod
from typing import Any

# --- Abstract Base Class ---

class StateCheck(ABC):
    """
    Abstract base class for any hardware status checker.
    """
    @abstractmethod
    def capture(self) -> Any:
        """
        Required method for capturing current data.
        """
        pass

class Logger(ABC):
    """
    Clase abstracta madre para los loggers.
    """
    @abstractmethod
    def info(self, message: str) -> None:
        pass
    @abstractmethod
    def debug(self, message: str) -> None:
        pass
    @abstractmethod
    def warning(self, message: str) -> None:
        pass
    @abstractmethod
    def error(self, message: str) -> None:
        pass