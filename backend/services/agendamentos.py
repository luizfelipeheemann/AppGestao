from fastapi import HTTPException
from uuid import UUID
from datetime import datetime
from database import get_db
from models import Agendamento as AgendamentoDB, ClientePacote as ClientePacoteDB, PacoteServico as PacoteDB, Pagamento as PagamentoDB
from schemas.agendamentos import AgendamentoCreate, AgendamentoUpdate
from typing import List

def criar_agendamento(data: AgendamentoCreate) -> AgendamentoDB:
    db = next(get_db())
    obj = AgendamentoDB(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def listar_agendamentos() -> List[AgendamentoDB]:
    db = next(get_db())
    return db.query(AgendamentoDB).order_by(AgendamentoDB.data_hora_inicio.desc()).all()

def atualizar_agendamento(id: UUID, data: AgendamentoUpdate) -> AgendamentoDB:
    db = next(get_db())
    obj = db.query(AgendamentoDB).get(str(id))
    if not obj:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    if data.status == 'concluido':
        raise HTTPException(status_code=400, detail="Use PATCH /agendamentos/{id}/concluir para concluir")
    for k, v in data.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def concluir_agendamento(id: UUID) -> AgendamentoDB:
    db = next(get_db())
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
