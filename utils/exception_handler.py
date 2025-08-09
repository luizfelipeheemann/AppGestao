# utils/exception_handler.py
from functools import wraps
from fastapi import HTTPException, status
import traceback
from logging_config import get_logger

logger = get_logger("exception_handler")

def safe_route(tag: str = "rota"):
    def decorator(func):
        is_async = False
        try:
            is_async = func.__code__.co_flags & 0x80
        except:
            pass

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Erro em {tag}: {e}", exc_info=True)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Erro interno em {tag}"
                )

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Erro em {tag}: {e}", exc_info=True)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Erro interno em {tag}"
                )

        return async_wrapper if is_async else sync_wrapper

    return decorator
