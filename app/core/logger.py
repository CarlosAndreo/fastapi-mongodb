import json
import logging
import logging.config
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


class JsonFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging.

    Formats log records as JSON objects with consistent structure including
    timestamp, level, logger name, module, line number, message and exceptions.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record as a JSON string.

        Args:
            record: The log record to format.

        Returns:
            JSON-formatted string with log information.
        """
        log_data: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        # core/logging.py
        if hasattr(record, "request_id"):
            log_data["request_id"] = getattr(record, "request_id")
        if hasattr(record, "method"):
            log_data["method"] = getattr(record, "method")
        if hasattr(record, "path"):
            log_data["path"] = getattr(record, "path")
        if hasattr(record, "client_host"):
            log_data["client_host"] = getattr(record, "client_host")
        if hasattr(record, "query_params"):
            log_data["query_params"] = getattr(record, "query_params")
        if hasattr(record, "status_code"):
            log_data["status_code"] = getattr(record, "status_code")
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = getattr(record, "duration_ms")
        # all routers
        return json.dumps(log_data, default=str)


LOG_DIR = Path("/var/log/backend")
if "pytest" in sys.modules:
    LOG_DIR = Path("/tmp/logs")
LOG_DIR.mkdir(exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "json": {
            "()": JsonFormatter,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": sys.stdout,
        },
        "console_json": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "json",
            "stream": sys.stdout,
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "json",
            "filename": str(LOG_DIR / "app.log"),
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf-8",
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "json",
            "filename": str(LOG_DIR / "error.log"),
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf-8",
        },
    },
    "loggers": {
        # Root logger
        "": {
            "level": "INFO",
            "handlers": ["console", "file", "error_file"],
        },
        # App logger
        "app": {
            "level": "DEBUG",
            "handlers": ["console_json", "file", "error_file"],
            "propagate": False,
        },
        # Uvicorn loggers
        "uvicorn": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "uvicorn.access": {
            "level": "INFO",
            "handlers": ["file"],
            "propagate": False,
        },
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["console", "error_file"],
            "propagate": False,
        },
        # Silence watchfiles (used by uvicorn --reload)
        "watchfiles": {
            "level": "WARNING",
            "handlers": ["console"],
            "propagate": False,
        },
        "watchfiles.main": {
            "level": "WARNING",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}


def setup_logging(log_level: str = "INFO", use_json: bool = False) -> None:
    """Configure logging for the application.

    Args:
        log_level: The minimum log level to capture (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        use_json: Whether to use JSON formatting for console output.
    """
    LOGGING_CONFIG["loggers"][""]["level"] = log_level
    LOGGING_CONFIG["loggers"]["app"]["level"] = log_level
    if use_json:
        LOGGING_CONFIG["loggers"][""]["handlers"] = [
            "console_json",
            "file",
            "error_file",
        ]
    else:
        LOGGING_CONFIG["loggers"][""]["handlers"] = ["console", "file", "error_file"]
    logging.config.dictConfig(config=LOGGING_CONFIG)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name.

    Args:
        name: The name of the logger (typically __name__ of the module).

    Returns:
        A configured logger instance.
    """
    return logging.getLogger(name=name)
