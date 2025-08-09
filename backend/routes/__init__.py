from fastapi import APIRouter
from routes import (
    agendamento_inteligente,
    agendamentos,
    auth,
    cliente,
    cliente_pacote,
    dashboard,
    pacotes,
    relatorios,
    servicos
)

router = APIRouter()

router.include_router(auth.router)
router.include_router(agendamentos.router)
router.include_router(agendamento_inteligente.router)
router.include_router(cliente.router)
router.include_router(cliente_pacote.router)
router.include_router(dashboard.router)
router.include_router(pacotes.router)
router.include_router(relatorios.router)
router.include_router(servicos.router)
