from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from uuid import UUID
from typing import List
from datetime import datetime, timedelta

from database import get_db, Cliente as ClienteDB, PacoteServico as PacoteDB, ClientePacote as ClientePacoteDB
from schemas.cliente_pacote import VendaPacoteCreate, ClientePacote as ClientePacoteOut
from utils.exception_handler import safe_route

router = APIRouter(prefix="/clientes/{cliente_id}/pacotes", tags=["Clientes", "Pacotes"])

@router.post("", response_model=ClientePacoteOut, status_code=status.HTTP_201_CREATED)
@safe_route("vender_pacote_para_cliente")
def vender_pacote(cliente_id: UUID, venda: VendaPacoteCreate, db: Session = Depends(get_db)):
    cliente = db.query(ClienteDB).filter(ClienteDB.id == str(cliente_id)).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    pacote = db.query(PacoteDB).filter(PacoteDB.id == venda.pacote_id).first()
    if not pacote:
        raise HTTPException(status_code=404, detail="Tipo de pacote não encontrado")

    data_expiracao = datetime.utcnow() + timedelta(days=pacote.validade_dias)
    
    nova_compra = ClientePacoteDB(
        cliente_id=str(cliente_id),
        pacote_id=venda.pacote_id,
        data_expiracao=data_expiracao,
        saldo_sessoes=pacote.quantidade_sessoes,
        status="ativo"
    )

    db.add(nova_compra)
    db.commit()
    db.refresh(nova_compra)

    return nova_compra

@router.get("", response_model=List[ClientePacoteOut])
@safe_route("listar_pacotes_do_cliente")
def listar_pacotes(cliente_id: UUID, db: Session = Depends(get_db)):
    return db.query(ClientePacoteDB).filter(ClientePacoteDB.cliente_id == str(cliente_id)).options(
        joinedload(ClientePacoteDB.pacote).joinedload(PacoteDB.servicos)
    ).all()
