import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.infrastructure.observability.context import get_request_id, set_request_id
from app.infrastructure.observability.logging import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = set_request_id(request.headers.get("X-Request-ID"))

        logger.info(
            "request started",
            extra={
                "method": request.method,
                "path": request.url.path,
            },
        )

        start = time.perf_counter()
        status_code = 500

        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception:
            logger.exception("unhandled exception during request")
            raise
        finally:
            duration_ms = round((time.perf_counter() - start) * 1000, 2)
            logger.info(
                "request finished",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": status_code,
                    "duration_ms": duration_ms,
                },
            )

        response.headers["X-Request-ID"] = get_request_id() or request_id
        return response
