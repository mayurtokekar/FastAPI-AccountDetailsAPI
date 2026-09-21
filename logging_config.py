import json
import logging
import sys
from datetime import datetime, timezone
from logging.config import dictConfig
from typing import Any, Optional

from starlette.requests import Request
from starlette.responses import Response


class JsonFormatter(logging.Formatter):
    """Structured JSON log formatter.

    Emits one JSON object per line with: timestamp, level, logger, message,
    and any `extra` fields passed to the log call. Exception info is
    included as `exception` when present.
    """

    RESERVED = {
        "name", "msg", "args", "levelname", "levelno", "pathname", "filename",
        "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName",
        "created", "msecs", "relativeCreated", "thread", "threadName",
        "processName", "process", "message", "asctime", "taskName",
    }

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for key, value in record.__dict__.items():
            if key in self.RESERVED or key.startswith("_"):
                continue
            payload[key] = value
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str, ensure_ascii=False)


def configure_logging(level: str = "INFO") -> None:
    """Configure root logging once at startup.

    `level` can be overridden via the `LOG_LEVEL` environment variable
    before this function is called.
    """
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": "logging_config.JsonFormatter",
                },
            },
            "handlers": {
                "stdout": {
                    "class": "logging.StreamHandler",
                    "stream": sys.stdout,
                    "formatter": "json",
                },
            },
            "root": {
                "level": level,
                "handlers": ["stdout"],
            },
            "loggers": {
                "uvicorn": {"level": level, "handlers": ["stdout"], "propagate": False},
                "uvicorn.error": {"level": level, "handlers": ["stdout"], "propagate": False},
                "uvicorn.access": {"level": level, "handlers": ["stdout"], "propagate": False},
            },
        }
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    return logging.getLogger(name if name else "account_details")


def client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.client.host if request.client else "unknown"
