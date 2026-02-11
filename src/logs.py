# src/logging_config.py
import logging.config
import logging


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
    'filters': {
        'only_debug': {
            '()': SpecificLevelFilter,
            'level': 'DEBUG',
        }
    },
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(lineno)d [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "simple": {
            "format": "%(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "INFO",  # Solo INFO y superior
        },
        "file_info": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/app.log",
            "formatter": "standard",
            "level": "INFO",  # INFO, WARNING, ERROR, CRITICAL
            "maxBytes": 10485760,
            "backupCount": 5,
        },
        "file_debug": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/debug.log",
            "formatter": "standard",
            "level": "DEBUG",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
            "maxBytes": 10485760,
            "backupCount": 5,
            'filters': ['only_debug'],
        },
    },
    "loggers": {
        "": {  # Root logger
            "handlers": ["console", "file_info", "file_debug"],
            "level": "DEBUG",
            "propagate": True
        }
    }
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)