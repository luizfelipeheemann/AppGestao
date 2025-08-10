from fastapi import APIRouter

# Importações absolutas a partir do pacote 'backend'
from backend.routes import agendamento_inteligente
from backend.routes import agendamentos
from backend.routes import auth
from backend.routes import clientes
from backend.routes import clientes_pacotes
from backend.routes import dashboard
from backend.routes import pacotes
from backend.routes import relatorios
from backend.routes import servicos

api_router = APIRouter()

# Inclui as rotas de cada módulo, definindo prefixos e tags para organização
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
api_router.include_router(agendamentos.router, prefix="/agendamentos", tags=["Agendamentos"])
api_router.include_router(agendamento_inteligente.router, prefix="/agendamento-inteligente", tags=["Agendamento Inteligente"])
api_router.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
api_router.include_router(clientes_pacotes.router, prefix="/clientes-pacotes", tags=["Clientes Pacotes"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(pacotes.router, prefix="/pacotes", tags=["Pacotes"])
api_router.include_router(relatorios.router, prefix="/relatorios", tags=["Relatórios"])
api_router.include_router(servicos.router, prefix="/servicos", tags=["Serviços"])
