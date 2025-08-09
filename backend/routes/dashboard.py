from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.dashboard import get_dashboard_stats_srv, get_proximos_agendamentos_srv
from schemas.agendamentos import AgendamentoOut
from utils.exception_handler import safe_route
from database import get_db

router = APIRouter(tags=["Dashboard"])

@router.get("/dashboard/stats")
@safe_route("get_dashboard_stats")
def dashboard_stats(db: Session = Depends(get_db)):
    return get_dashboard_stats_srv(db)

@router.get("/agendamentos/proximos", response_model=list[AgendamentoOut])
@safe_route("get_proximos_agendamentos")
def proximos_agendamentos(db: Session = Depends(get_db)):
    return get_proximos_agendamentos_srv(db)
