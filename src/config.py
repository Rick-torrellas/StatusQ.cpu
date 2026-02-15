import os

# These configuration constants define where different log levels will be written

# Primary log file path - captures all log entries by default
LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")

# Level-specific log file paths for granular logging control
# Each constant defines a dedicated file for its corresponding log level

# Debug level log file - captures detailed debugging information
LOG_FILE_DEBUG: str = os.getenv("LOG_FILE_DEBUG", "logs/debug.log")

# Info level log file - captures general operational information
LOG_FILE_INFO: str = os.getenv("LOG_FILE_INFO", "logs/info.log")

# Error level log file - captures error conditions that don't halt the application
LOG_FILE_ERROR: str = os.getenv("LOG_FILE_ERROR", "logs/error.log")

# Critical level log file - captures severe errors that may cause
# application termination
LOG_FILE_CRITICAL: str = os.getenv("LOG_FILE_CRITICAL", "logs/critical.log")

# Warning level log file - captures potential issues that don't affect normal operation
LOG_FILE_WARNING: str = os.getenv("LOG_FILE_WARNING", "logs/warning.log")
