from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from services.pacotes import criar_pacote_srv, listar_pacotes_srv, atualizar_pacote_srv, excluir_pacote_srv
from schemas.pacote import PacoteServico, PacoteServicoCreate, PacoteServicoUpdate
from utils.exception_handler import safe_route
from database import get_db

router = APIRouter(prefix="/pacotes", tags=["Pacotes"])

@router.post("", response_model=PacoteServico, status_code=status.HTTP_201_CREATED)
@safe_route("criar_pacote")
def criar_pacote(p: PacoteServicoCreate, db: Session = Depends(get_db)):
    return criar_pacote_srv(p, db)

@router.get("", response_model=List[PacoteServico])
@safe_route("listar_pacotes")
def listar_pacotes(db: Session = Depends(get_db)):
    return listar_pacotes_srv(db)

@router.put("/{pacote_id}", response_model=PacoteServico)
@safe_route("atualizar_pacote")
def atualizar_pacote(pacote_id: UUID, p: PacoteServicoUpdate, db: Session = Depends(get_db)):
    return atualizar_pacote_srv(pacote_id, p, db)

@router.delete("/{pacote_id}", status_code=status.HTTP_204_NO_CONTENT)
@safe_route("excluir_pacote")
def excluir_pacote(pacote_id: UUID, db: Session = Depends(get_db)):
    excluir_pacote_srv(pacote_id, db)
