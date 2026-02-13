import logging
import logging.config

from src.config import (
    LOG_FILE,
    LOG_FILE_CRITICAL,
    LOG_FILE_DEBUG,
    LOG_FILE_ERROR,
    LOG_FILE_INFO,
    LOG_FILE_WARNING,
)


class SpecificLevelFilter(logging.Filter):
    def __init__(self, level=None):
        super().__init__()
        # Guardamos el nivel. Si es string (ej: "INFO"), lo convertimos a int
        if isinstance(level, str):
            self.level = getattr(logging, level.upper())
        else:
            self.level = level

    def filter(self, record):
        # Solo permite el paso si el nivel es exactamente el configurado
        return record.levelno == self.level


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "only_debug": {
            "()": SpecificLevelFilter,
            "level": "DEBUG",
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
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(lineno)d [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {"format": "%(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "INFO",  # Solo INFO y superior
        },
        "file_app": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_FILE,
            "formatter": "standard",
            "level": "DEBUG",  # INFO, WARNING, ERROR, CRITICAL
            "maxBytes": 10485760,
            "backupCount": 5,
        },
        "file_info": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_FILE_INFO,
            "formatter": "standard",
            "level": "INFO",  # INFO, WARNING, ERROR, CRITICAL
            "maxBytes": 10485760,
            "backupCount": 5,
            "filters": ["only_info"],
        },
        "file_debug": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_FILE_DEBUG,
            "formatter": "standard",
            "level": "DEBUG",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
            "maxBytes": 10485760,
            "backupCount": 5,
            "filters": ["only_debug"],
        },
        "file_error": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_FILE_ERROR,
            "formatter": "standard",
            "level": "ERROR",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
            "maxBytes": 10485760,
            "backupCount": 5,
            "filters": ["only_error"],
        },
        "file_critical": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_FILE_CRITICAL,
            "formatter": "standard",
            "level": "CRITICAL",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
            "maxBytes": 10485760,
            "backupCount": 5,
            "filters": ["only_critical"],
        },
        "file_warning": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_FILE_WARNING,
            "formatter": "standard",
            "level": "WARNING",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
            "maxBytes": 10485760,
            "backupCount": 5,
            "filters": ["only_warning"],
        },
    },
    "loggers": {
        "": {  # Root logger
            "handlers": [
                "console",
                "file_info",
                "file_debug",
                "file_error",
                "file_critical",
                "file_warning",
            ],
            "level": "DEBUG",
            "propagate": True,
        }
    },
}


def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
