from fastapi import HTTPException
from typing import List
from uuid import UUID
from database import get_db
from models import PacoteServico as PacoteDB
from schemas.pacote import PacoteServicoCreate, PacoteServicoUpdate

def criar_pacote(data: PacoteServicoCreate) -> PacoteDB:
    db = next(get_db())
    obj = PacoteDB(
        nome=data.nome,
        quantidade_sessoes=data.quantidade_sessoes,
        validade_dias=data.validade_dias,
        servicos=[s for s in data.servicos_ids]
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def listar_pacotes() -> List[PacoteDB]:
    db = next(get_db())
    return db.query(PacoteDB).order_by(PacoteDB.nome).all()

def atualizar_pacote(pacote_id: UUID, data: PacoteServicoUpdate) -> PacoteDB:
    db = next(get_db())
    obj = db.query(PacoteDB).get(str(pacote_id))
    if not obj:
        raise HTTPException(status_code=404, detail="Pacote não encontrado")
    for k, v in data.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def excluir_pacote(pacote_id: UUID):
    db = next(get_db())
    obj = db.query(PacoteDB).get(str(pacote_id))
    if not obj:
        raise HTTPException(status_code=404, detail="Pacote não encontrado")
    db.delete(obj)
    db.commit()
