from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

# --- Importações Corrigidas ---
from backend.core.database import get_db
from backend.services.dashboard import get_dashboard_stats_srv, get_proximos_agendamentos_srv
from backend.schemas.agendamentos import Agendamento as AgendamentoOut
from utils.exception_handler import safe_route
# --- Fim das Importações Corrigidas ---

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats", response_model=dict)
@safe_route("get_dashboard_stats")
def dashboard_stats(db: Session = Depends(get_db)):
    return get_dashboard_stats_srv(db)

@router.get("/proximos-agendamentos", response_model=List[AgendamentoOut])
@safe_route("get_proximos_agendamentos")
def proximos_agendamentos(db: Session = Depends(get_db)):
    return get_proximos_agendamentos_srv(db)
