import os

LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
LOG_FILE_DEBUG = os.getenv('LOG_FILE_DEBUG', 'logs/debug.log')
LOG_FILE_INFO = os.getenv('LOG_FILE_INFO', 'logs/info.log')
LOG_FILE_ERROR = os.getenv('LOG_FILE_ERROR', 'logs/error.log')
LOG_FILE_CRITICAL = os.getenv('LOG_FILE_CRITICAL', 'logs/critical.log')
LOG_FILE_WARNING = os.getenv('LOG_FILE_WARNING', 'logs/warning.log')
LOG_FILE_EXCEPTION = os.getenv('LOG_FILE_EXCEPTION', 'logs/exception.log')