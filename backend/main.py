# Código para: backend/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time

from logging_config import setup_logging, get_logger, LoggingMiddleware
from config import settings
from backend.routes import api_router
from backend.core.database import init_database

# A importação explícita dos modelos não é mais necessária aqui,
# pois o __init__.py da pasta models já cuida disso.
import backend.models

setup_logging()
logger = get_logger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Inicializando aplicação...")
    init_database()
    logger.info("Banco de dados inicializado.")
    yield
    logger.info("Finalizando aplicação...")

# ... (o resto do arquivo continua igual)
app = FastAPI(
    title="Sistema de Gestão para Profissional Liberal",
    description="API segura para gerenciamento de clientes, agendamentos e serviços",
    version="2.0.0",
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
    lifespan=lifespan
)
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)
if settings.is_production:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
    )
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Erro não tratado na requisição: {request.method} {request.url}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Ocorreu um erro interno inesperado no servidor."}
    )
app.include_router(api_router)
