from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from database import get_db, Servico as ServicoDB
from schemas.servico import ServicoCreate, ServicoUpdate, Servico
from utils.exception_handler import safe_route

router = APIRouter(prefix="/servicos", tags=["Serviços"])

@router.post("", response_model=Servico, status_code=status.HTTP_201_CREATED)
@safe_route("criar_servico")
def criar_servico(servico_data: ServicoCreate, db: Session = Depends(get_db)):
    novo_servico = ServicoDB(**servico_data.dict())
    db.add(novo_servico)
    db.commit()
    db.refresh(novo_servico)
    return novo_servico

@router.get("", response_model=List[Servico])
@safe_route("listar_servicos")
def listar_servicos(db: Session = Depends(get_db)):
    return db.query(ServicoDB).order_by(ServicoDB.nome).all()

@router.put("/{servico_id}", response_model=Servico)
@safe_route("atualizar_servico")
def atualizar_servico(servico_id: UUID, servico_data: ServicoUpdate, db: Session = Depends(get_db)):
    servico_obj = db.query(ServicoDB).filter(ServicoDB.id == str(servico_id)).first()
    if not servico_obj:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    update_data = servico_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(servico_obj, key, value)

    db.commit()
    db.refresh(servico_obj)
    return servico_obj

@router.delete("/{servico_id}", status_code=status.HTTP_204_NO_CONTENT)
@safe_route("excluir_servico")
def excluir_servico(servico_id: UUID, db: Session = Depends(get_db)):
    servico_obj = db.query(ServicoDB).filter(ServicoDB.id == str(servico_id)).first()
    if not servico_obj:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    
    db.delete(servico_obj)
    db.commit()
