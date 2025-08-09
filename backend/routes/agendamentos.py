from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from uuid import UUID
from typing import List
from services.agendamentos import criar_agendamento_srv, listar_agendamentos_srv, atualizar_agendamento_srv, concluir_agendamento_srv
from schemas.agendamentos import AgendamentoCreate, AgendamentoUpdate, AgendamentoOut
from utils.exception_handler import safe_route
from database import get_db

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])

@router.post("", response_model=AgendamentoOut, status_code=status.HTTP_201_CREATED)
@safe_route("criar_agendamento")
def criar_agendamento(ag: AgendamentoCreate, db: Session = Depends(get_db)):
    return criar_agendamento_srv(ag, db)

@router.get("", response_model=List[AgendamentoOut])
@safe_route("listar_agendamentos")
def listar_agendamentos(db: Session = Depends(get_db)):
    return listar_agendamentos_srv(db)

@router.put("/{id}", response_model=AgendamentoOut)
@safe_route("atualizar_agendamento")
def atualizar_agendamento(id: UUID, ag: AgendamentoUpdate, db: Session = Depends(get_db)):
    return atualizar_agendamento_srv(id, ag, db)

@router.patch("/{id}/concluir", response_model=AgendamentoOut)
@safe_route("concluir_agendamento")
def concluir_agendamento(id: UUID, db: Session = Depends(get_db)):
    return concluir_agendamento_srv(id, db)
