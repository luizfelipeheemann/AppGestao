# utils/exception_handler.py
from functools import wraps
from fastapi import HTTPException, status
import traceback
import asyncio

# --- Importação Corrigida ---
# A importação já está correta, pois logging_config está na raiz.
from logging_config import get_logger
# --- Fim da Importação Corrigida ---

logger = get_logger("exception_handler")

def safe_route(tag: str = "rota"):
    """
    Um decorador que envolve uma rota FastAPI em um bloco try-except
    para capturar exceções inesperadas e logá-las, retornando um erro 500.
    """
    def decorator(func):
        # Simplifica a detecção de função assíncrona
        if asyncio.iscoroutinefunction(func):
            # Wrapper para funções async def
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                try:
                    # Executa a função de rota original
                    return await func(*args, **kwargs)
                except HTTPException:
                    # Se for uma exceção HTTP planejada, apenas a relança
                    raise
                except Exception as e:
                    # Para qualquer outra exceção, loga o erro completo
                    logger.error(f"Erro inesperado na rota '{tag}': {e}", exc_info=True)
                    # E levanta um erro 500 genérico para o cliente
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Ocorreu um erro interno inesperado."
                    )
            return async_wrapper
        else:
            # Wrapper para funções def síncronas
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except HTTPException:
                    raise
                except Exception as e:
                    logger.error(f"Erro inesperado na rota '{tag}': {e}", exc_info=True)
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Ocorreu um erro interno inesperado."
                    )
            return sync_wrapper
    return decorator
