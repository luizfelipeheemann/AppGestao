# Código para: backend/services/clientes_pacotes.py
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from uuid import UUID
from typing import List
from datetime import datetime, timedelta

# --- Importações Corrigidas ---
from backend.models.cliente import Cliente as ClienteDB
from backend.models.pacote import PacoteServico as PacoteDB
from backend.models.cliente_pacote import ClientePacote as ClientePacoteDB
from backend.schemas.cliente_pacote import VendaPacoteCreate
# --- Fim das Importações Corrigidas ---

def vender_pacote_srv(db: Session, cliente_id: UUID, venda_data: VendaPacoteCreate) -> ClientePacoteDB:
    """Associa um pacote a um cliente."""
    cliente = db.query(ClienteDB).filter(ClienteDB.id == str(cliente_id)).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    pacote = db.query(PacoteDB).filter(PacoteDB.id == str(venda_data.pacote_id)).first()
    if not pacote:
        raise HTTPException(status_code=404, detail="Pacote de serviço não encontrado")

    data_expiracao = datetime.utcnow() + timedelta(days=pacote.validade_dias)
    
    nova_compra = ClientePacoteDB(
        cliente_id=str(cliente_id),
        pacote_id=str(venda_data.pacote_id),
        data_expiracao=data_expiracao,
        saldo_sessoes=pacote.quantidade_sessoes,
        status="ativo"
    )

    db.add(nova_compra)
    db.commit()
    db.refresh(nova_compra)
    return nova_compra

def listar_pacotes_do_cliente_srv(db: Session, cliente_id: UUID) -> List[ClientePacoteDB]:
    """Lista todos os pacotes adquiridos por um cliente específico."""
    # Usando joinedload para carregar os detalhes do pacote junto, otimizando a consulta
    return db.query(ClientePacoteDB).filter(ClientePacoteDB.cliente_id == str(cliente_id)).options(
        joinedload(ClientePacoteDB.pacote)
    ).all()
