from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from logging_config import setup_logging, get_logger, LoggingMiddleware
from backend.routes import api_router
from backend.core.database import init_database
from config import settings
import time

setup_logging()
logger = get_logger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Inicializando aplicação...")
    init_database()
    yield
    logger.info("Finalizando aplicação...")

app = FastAPI(
    title="Sistema de Gestão para Profissional Liberal",
    description="API segura para gerenciamento de clientes, agendamentos e serviços",
    version="2.0.0",
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
    lifespan=lifespan
)

# Middleware de log estruturado
app.add_middleware(LoggingMiddleware)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Trusted Hosts (modo produção)
if settings.is_production:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
    )

# Manipulador global de exceções
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Erro não tratado: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor"},
        headers={
            "Access-Control-Allow-Origin": "http://localhost:5173",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

# Registro das rotas centralizadas
app.include_router(api_router)
