from abc import ABC, abstractmethod


class Logger(ABC):
    """Defines the interface for any logger that the application can use.

    This abstract base class establishes the contract that all logger
    implementations must follow, enabling dependency inversion and
    allowing different logging backends to be swapped without affecting
    application code.
    """

    @abstractmethod
    def info(self, message: str):
        """Log an informational message.

        Args:
            message: The string content to log at INFO level
        """
        pass

    @abstractmethod
    def debug(self, message: str):
        """Log a debug message for detailed diagnostic information.

        Args:
            message: The string content to log at DEBUG level
        """
        pass

    @abstractmethod
    def warning(self, message: str):
        """Log a warning message indicating potential issues.

        Args:
            message: The string content to log at WARNING level
        """
        pass

    @abstractmethod
    def error(self, message: str):
        """Log an error message for runtime errors or exceptions.

        Args:
            message: The string content to log at ERROR level
        """
        pass
