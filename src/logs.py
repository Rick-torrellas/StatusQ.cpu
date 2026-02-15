import logging
import logging.config
from typing import Optional, Union

from src.config import (
    LOG_FILE,
    LOG_FILE_CRITICAL,
    LOG_FILE_DEBUG,
    LOG_FILE_ERROR,
    LOG_FILE_INFO,
    LOG_FILE_WARNING,
)


class SpecificLevelFilter(logging.Filter):
    """Custom logging filter that only allows records with a specific log level."""

    def __init__(self, level: Union[int, str, None] = None) -> None:
        super().__init__()
        # Store the target level for filtering
        # If level is provided as string (e.g., "INFO"), convert to
        # corresponding integer constant
        if isinstance(level, str):
            self.level: Optional[int] = getattr(logging, level.upper())
        else:
            self.level = level

    def filter(self, record: logging.LogRecord) -> bool:
        """Determine if the specified record should be logged.

        Returns:
            bool: True only if the record's level exactly matches the configured level
        """
        return record.levelno == self.level


LOGGING_CONFIG = {
    "version": 1,  # Configuration schema version required by dictConfig
    "disable_existing_loggers": False,  # Preserve any pre-existing loggers
    # Filter definitions for level-specific log segregation
    "filters": {
        "only_debug": {
            "()": SpecificLevelFilter,  # Instantiate this filter class
            "level": "DEBUG",  # Configure to capture only DEBUG level
        },
        "only_info": {
            "()": SpecificLevelFilter,
            "level": "INFO",
        },
        "only_warning": {
            "()": SpecificLevelFilter,
            "level": "WARNING",
        },
        "only_error": {
            "()": SpecificLevelFilter,
            "level": "ERROR",
        },
        "only_critical": {
            "()": SpecificLevelFilter,
            "level": "CRITICAL",
        },
    },
    # Formatter definitions controlling log message structure
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(lineno)d [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",  # ISO-like datetime format
        },
        "simple": {
            "format": "%(message)s"
        },  # Minimal format for console output
    },
    # Handler definitions - destinations where log records are sent
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",  # Output to stdout/stderr
            "formatter": "simple",
            "level": "INFO",  # Only INFO level and above reach console
        },
        "file_app": {
            "class": "logging.handlers.RotatingFileHandler",  # Rotates when size limit reached # noqa: E501
            "filename": LOG_FILE,
            "formatter": "standard",
            "level": "DEBUG",  # Accepts DEBUG and above (DEBUG, INFO, WARNING, ERROR, CRITICAL) # noqa: E501
            "maxBytes": 10485760,  # 10MB maximum file size before rotation
            "backupCount": 5,  # Keep 5 rotated backup files
        },
        "file_info": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_FILE_INFO,
            "formatter": "standard",
            "level": "INFO",  # Accepts INFO and above but filtered to only INFO
            "maxBytes": 10485760,
            "backupCount": 5,
            "filters": [
                "only_info"
            ],  # Apply filter to restrict to exact INFO level
        },
        "file_debug": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_FILE_DEBUG,
            "formatter": "standard",
            "level": "DEBUG",  # Accepts all levels but filtered to only DEBUG
            "maxBytes": 10485760,
            "backupCount": 5,
            "filters": ["only_debug"],
        },
        "file_error": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_FILE_ERROR,
            "formatter": "standard",
            "level": "ERROR",  # Accepts ERROR and above but filtered to only ERROR
            "maxBytes": 10485760,
            "backupCount": 5,
            "filters": ["only_error"],
        },
        "file_critical": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_FILE_CRITICAL,
            "formatter": "standard",
            "level": "CRITICAL",  # Accepts CRITICAL and above but filtered to only CRITICAL # noqa: E501
            "maxBytes": 10485760,
            "backupCount": 5,
            "filters": ["only_critical"],
        },
        "file_warning": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_FILE_WARNING,
            "formatter": "standard",
            "level": "WARNING",  # Accepts WARNING and above but filtered to only WARNING  # noqa: E501
            "maxBytes": 10485760,
            "backupCount": 5,
            "filters": ["only_warning"],
        },
    },
    # Logger definitions - named loggers that propagate to handlers
    "loggers": {
        "": {  # Root logger (empty string denotes root)
            "handlers": [
                "console",
                "file_info",
                "file_debug",
                "file_error",
                "file_critical",
                "file_warning",
                # Note: file_app is excluded but can be added if needed
            ],
            "level": "DEBUG",  # Root logger accepts all levels
            "propagate": True,  # Allow propagation to ancestor loggers
        }
    },
}


def setup_logging():
    """Configure the logging system using the predefined dictionary configuration.

    This function initializes all loggers, handlers, and formatters according to
    the LOGGING_CONFIG dictionary. It should be called once at application startup.
    """
    logging.config.dictConfig(LOGGING_CONFIG)
