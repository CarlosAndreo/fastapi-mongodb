import time
import uuid
from typing import Callable

from core.logger import get_logger
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = get_logger(name=__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all HTTP requests and responses with timing information.

    This middleware:
    - Generates a unique request ID for each request
    - Logs incoming requests with method, path and client info
    - Measures request duration
    - Logs response status and duration
    - Adds request ID to response headers
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process the request and log details.

        Args:
            request: The incoming HTTP request.
            call_next: The next middleware or route handler.

        Returns:
            The HTTP response.
        """
        request_id = str(uuid.uuid4())
        method = request.method
        path = request.url.path
        client_host = request.client.host if request.client else "unknown"
        logger.info(
            f"Incoming request: {method} {path}",
            extra={
                "request_id": request_id,
                "method": method,
                "path": path,
                "client_host": client_host,
                "query_params": str(request.query_params),
            },
        )
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        response.headers["X-Request-ID"] = request_id
        logger.info(
            f"Request completed: {method} {path} - {response.status_code}",
            extra={
                "request_id": request_id,
                "method": method,
                "path": path,
                "status_code": response.status_code,
                "duration_ms": round(process_time, 2),
            },
        )
        return response
