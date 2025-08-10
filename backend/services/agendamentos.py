from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from typing import List

from backend.core.database import get_db
from backend.models.agendamento import Agendamento as AgendamentoDB
from backend.models.cliente_pacote import ClientePacote as ClientePacoteDB
from backend.models.pacote import PacoteServico as PacoteDB
from backend.models.pagamento import Pagamento as PagamentoDB
from backend.schemas.agendamentos import AgendamentoCreate, AgendamentoUpdate

def criar_agendamento_srv(ag: AgendamentoCreate, db: Session) -> AgendamentoDB:
    # Usando .model_dump() em vez de .dict() para compatibilidade com Pydantic V2
    obj = AgendamentoDB(**ag.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def listar_agendamentos_srv(db: Session) -> List[AgendamentoDB]:
    return db.query(AgendamentoDB).order_by(AgendamentoDB.data_hora_inicio.desc()).all()

def atualizar_agendamento_srv(id: UUID, data: AgendamentoUpdate, db: Session) -> AgendamentoDB:
    obj = db.query(AgendamentoDB).get(str(id))
    if not obj:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    if data.status == 'concluido':
        raise HTTPException(status_code=400, detail="Use PATCH /agendamentos/{id}/concluir para concluir")
    
    # Usando .model_dump() em vez de .dict()
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(obj, key, value)
        
    db.commit()
    db.refresh(obj)
    return obj

def concluir_agendamento_srv(id: UUID, db: Session) -> AgendamentoDB:
    obj = db.query(AgendamentoDB).get(str(id))
    if not obj:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    if obj.status == 'concluido':
        raise HTTPException(status_code=400, detail="Este agendamento já foi concluído.")

    pacote = db.query(ClientePacoteDB).join(PacoteDB).filter(
        ClientePacoteDB.cliente_id == obj.cliente_id,
        ClientePacoteDB.status == 'ativo',
        ClientePacoteDB.saldo_sessoes > 0,
        ClientePacoteDB.data_expiracao >= datetime.utcnow(),
        PacoteDB.servicos.any(id=obj.servico_id)
    ).order_by(ClientePacoteDB.data_expiracao.asc()).first()

    if pacote:
        pacote.saldo_sessoes -= 1
        if pacote.saldo_sessoes == 0:
            pacote.status = 'esgotado'
        pagamento = PagamentoDB(
            agendamento_id=obj.id, valor=0, metodo_pagamento="pacote", status="pago",
            descricao=f"Utilizado do pacote '{pacote.pacote.nome}'"
        )
    else:
        pagamento = PagamentoDB(
            agendamento_id=obj.id, valor=obj.servico.preco, metodo_pagamento="pix",
            status="pendente", descricao=f"Cobrança pelo serviço: {obj.servico.nome}"
        )
        
    db.add(pagamento)
    obj.status = 'concluido'
    db.commit()
    db.refresh(obj)
    return obj
