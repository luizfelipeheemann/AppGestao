from fastapi import HTTPException
from uuid import UUID
from database import get_db
from models import Servico as ServicoDB
from schemas.servico import ServicoCreate, ServicoUpdate
from typing import List

def criar_servico(data: ServicoCreate) -> ServicoDB:
    db = next(get_db())
    obj = ServicoDB(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def listar_servicos() -> List[ServicoDB]:
    db = next(get_db())
    return db.query(ServicoDB).order_by(ServicoDB.nome).all()

def atualizar_servico(servico_id: UUID, data: ServicoUpdate) -> ServicoDB:
    db = next(get_db())
    obj = db.query(ServicoDB).get(str(servico_id))
    if not obj:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    for k, v in data.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def excluir_servico(servico_id: UUID):
    db = next(get_db())
    obj = db.query(ServicoDB).get(str(servico_id))
    if not obj:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    db.delete(obj)
    db.commit()
