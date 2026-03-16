import logging
import sys
from datetime import UTC, datetime
from typing import Any

import orjson

_BUILTIN_RECORD_ATTRS = frozenset(
    {
        "args",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "lineno",
        "message",
        "module",
        "msecs",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "stack_info",
        "taskName",
        "thread",
        "threadName",
    }
)


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        # formatMessage populates record.message
        record.message = record.getMessage()

        payload: dict[str, Any] = {
            "ts": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.message,
        }

        # inject correlation id when available (set by HTTP middleware or Celery tasks)
        from app.infrastructure.observability.context import get_request_id

        if rid := get_request_id():
            payload["request_id"] = rid

        # propagate any extra fields passed via logger.info(..., extra={...})
        for key, value in record.__dict__.items():
            if key not in _BUILTIN_RECORD_ATTRS:
                payload[key] = value

        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info:
            payload["stack_info"] = self.formatStack(record.stack_info)

        return orjson.dumps(payload).decode()


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def setup_logging() -> None:
    from app.infrastructure.config.settings import get_settings

    settings = get_settings()
    level = getattr(logging, settings.log_level.upper(), logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(handler)

    # avoid double-logging HTTP access — our middleware owns that
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    # only surface slow/error queries; keep quiet by default
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
