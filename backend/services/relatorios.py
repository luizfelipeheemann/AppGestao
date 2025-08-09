from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from typing import Optional, List
from database import get_db
from models import ClientePacote as ClientePacoteDB, Pagamento as PagamentoDB, Agendamento as AgendamentoDB, PacoteServico as PacoteDB
from schemas.relatorio import RelatorioConsumoPacote, RelatorioConsumoItem
from datetime import timedelta

def relatorio_consumo_pacotes(
    cliente_id: Optional[str] = None,
    data_inicio = None,
    data_fim = None
) -> List[RelatorioConsumoPacote]:
    db = next(get_db())
    query = db.query(ClientePacoteDB).options(
        joinedload(ClientePacoteDB.cliente),
        joinedload(ClientePacoteDB.pacote).joinedload(PacoteDB.servicos)
    ).order_by(ClientePacoteDB.data_compra.desc())

    if cliente_id:
        query = query.filter(ClientePacoteDB.cliente_id == cliente_id)
    if data_inicio:
        query = query.filter(ClientePacoteDB.data_compra >= data_inicio)
    if data_fim:
        query = query.filter(ClientePacoteDB.data_compra < (data_fim + timedelta(days=1)))

    compras = query.all()
    resultado = []
    for compra in compras:
        pagamentos_ids = db.query(PagamentoDB.agendamento_id).filter(
            PagamentoDB.metodo_pagamento == 'pacote',
            PagamentoDB.agendamento.has(cliente_id=compra.cliente_id)
        ).subquery()
        usos = db.query(AgendamentoDB).filter(
            AgendamentoDB.id.in_(pagamentos_ids),
            AgendamentoDB.data_hora_inicio >= compra.data_compra
        ).options(joinedload(AgendamentoDB.servico)).order_by(AgendamentoDB.data_hora_inicio).all()

        consumo = [
            RelatorioConsumoItem(data_uso=uso.data_hora_inicio, servico_nome=uso.servico.nome)
            for uso in usos if uso.servico_id in [s.id for s in compra.pacote.servicos]
        ][:compra.pacote.quantidade_sessoes]

        resultado.append(RelatorioConsumoPacote(
            cliente_nome=compra.cliente.nome,
            pacote_nome=compra.pacote.nome,
            data_compra=compra.data_compra,
            data_expiracao=compra.data_expiracao,
            sessoes_total=compra.pacote.quantidade_sessoes,
            sessoes_saldo=compra.saldo_sessoes,
            status=compra.status,
            consumo=consumo
        ))

    return resultado
