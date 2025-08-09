import structlog
import logging
import sys
from typing import Optional
from config import settings


def setup_logging() -> None:
    """
    Configura logging estruturado com structlog.
    """
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
    )

    processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.contextvars.merge_contextvars,
    ]

    if settings.is_production:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: Optional[str] = None) -> structlog.stdlib.BoundLogger:
    """
    Retorna uma instância de logger estruturado.
    """
    return structlog.get_logger(name)


class LoggingMiddleware:
    """
    Middleware ASGI para logging de requisições HTTP.
    """
    def __init__(self, app):
        self.app = app
        self.logger = get_logger("request")

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        method = scope.get("method", "")
        path = scope.get("path", "")
        query_string = scope.get("query_string", b"").decode()
        headers = dict(scope.get("headers", {}))

        self.logger.info(
            "Request started",
            method=method,
            path=path,
            query_string=query_string,
            headers=headers
        )

        import time
        start_time = time.time()

        async def send_wrapper(message):
            if message.get("type") == "http.response.start":
                status_code = message.get("status")
                duration = time.time() - start_time
                response_headers = dict(message.get("headers", {}))
                self.logger.info(
                    "Response started",
                    method=method,
                    path=path,
                    status_code=status_code,
                    duration=f"{duration:.4f}s",
                    response_headers=response_headers
                )
            await send(message)

        await self.app(scope, receive, send_wrapper)