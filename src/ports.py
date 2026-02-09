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