from datetime import datetime, timedelta
from fastapi import HTTPException
from uuid import UUID
from database import get_db
from models import ClientePacote as ClientePacoteDB, Cliente as ClienteDB, PacoteServico as PacoteDB
from schemas.cliente_pacote import VendaPacoteCreate
from typing import Optional

def vender_pacote_para_cliente(cliente_id: UUID, data: VendaPacoteCreate) -> ClientePacoteDB:
    db = next(get_db())
    cliente = db.query(ClienteDB).get(str(cliente_id))
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    pacote = db.query(PacoteDB).get(str(data.pacote_id))
    if not pacote:
        raise HTTPException(status_code=404, detail="Pacote não encontrado")
    data_exp = datetime.utcnow() + timedelta(days=pacote.validade_dias)
    obj = ClientePacoteDB(
        cliente_id= str(cliente_id),
        pacote_id= str(data.pacote_id),
        data_expiracao= data_exp,
        saldo_sessoes= pacote.quantidade_sessoes,
        status="ativo"
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def listar_pacotes_do_cliente(cliente_id: UUID):
    db = next(get_db())
    return db.query(ClientePacoteDB).filter(ClientePacoteDB.cliente_id == str(cliente_id))\
        .options(ClientePacoteDB.pacote).all()
