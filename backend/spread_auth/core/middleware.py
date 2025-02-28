import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from spread_auth.core.loggers import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Логируем входящий запрос
        body = await request.body()
        logger.debug(f"⤋ Request: {request.method} {request.url} | Body: {body.decode() if body else None}")

        # Выполняем запрос
        response = await call_next(request)

        # Логируем ответ
        process_time = time.time() - start_time
        logger.debug(f"⤊ Response: {response.status_code} | Time: {process_time:.2f}s")

        return response
