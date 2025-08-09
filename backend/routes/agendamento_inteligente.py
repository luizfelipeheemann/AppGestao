from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import date
from services.agendamento_inteligente import obter_ultimo_agendamento, sugerir_horarios
from schemas.agendamento_inteligente import AgendamentoSugestao, ErroAgendamento
from utils.exception_handler import safe_route
from database import get_db

router = APIRouter(prefix="/agendamento-inteligente", tags=["Agendamentos Inteligentes"])

@router.post("/sugestoes", response_model=AgendamentoSugestao)
@safe_route("sugerir_horarios")
def rota_sugerir_horarios(
    cliente_id: UUID,
    data: date,
    duracao_minutos: int,
    db: Session = Depends(get_db)
):
    try:
        sugestao = sugerir_horarios(cliente_id, data, duracao_minutos, db)
        return sugestao
    except ErroAgendamento as e:
        raise HTTPException(status_code=400, detail={"code": e.code, "message": e.message})
