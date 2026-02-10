# src/logging_config.py
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
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