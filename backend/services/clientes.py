from fastapi import HTTPException
from typing import List
from uuid import UUID
from database import get_db
from models import Cliente as ClienteDB
from schemas.cliente import ClienteCreate, ClienteUpdate

def criar_cliente(data: ClienteCreate) -> ClienteDB:
    db = next(get_db())
    obj = ClienteDB(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def listar_clientes() -> List[ClienteDB]:
    db = next(get_db())
    return db.query(ClienteDB).order_by(ClienteDB.nome).all()

def atualizar_cliente(cliente_id: UUID, data: ClienteUpdate) -> ClienteDB:
    db = next(get_db())
    obj = db.query(ClienteDB).get(str(cliente_id))
    if not obj:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    for k, v in data.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def excluir_cliente(cliente_id: UUID):
    db = next(get_db())
    obj = db.query(ClienteDB).get(str(cliente_id))
    if not obj:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    db.delete(obj)
    db.commit()
