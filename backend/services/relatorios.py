from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from datetime import date, datetime, timedelta
from uuid import UUID

# --- Importações Corrigidas ---
from backend.models.cliente_pacote import ClientePacote as ClientePacoteDB
from backend.models.agendamento import Agendamento as AgendamentoDB
from backend.models.pacote import PacoteServico as PacoteDB
from backend.schemas.relatorio import RelatorioConsumoPacote, RelatorioConsumoItem
# --- Fim das Importações Corrigidas ---

def get_relatorio_consumo_pacotes_srv(
    db: Session,
    cliente_id: Optional[UUID] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None
) -> List[RelatorioConsumoPacote]:
    """
    Gera um relatório de consumo de pacotes com base nos filtros fornecidos.
    """
    # A consulta base busca todas as compras de pacotes e já carrega os dados do cliente e do pacote.
    query = db.query(ClientePacoteDB).options(
        joinedload(ClientePacoteDB.cliente),
        joinedload(ClientePacoteDB.pacote)
    ).order_by(ClientePacoteDB.data_compra.desc())

    # Aplica os filtros opcionais
    if cliente_id:
        query = query.filter(ClientePacoteDB.cliente_id == str(cliente_id))
    if data_inicio:
        query = query.filter(ClientePacoteDB.data_compra >= data_inicio)
    if data_fim:
        # Adiciona 1 dia ao data_fim para incluir todo o dia na consulta
        query = query.filter(ClientePacoteDB.data_compra < (data_fim + timedelta(days=1)))

    compras_de_pacotes = query.all()
    
    relatorios_finais = []
    for compra in compras_de_pacotes:
        # Para cada compra de pacote, busca os agendamentos concluídos
        # que ocorreram após a compra e antes da expiração do pacote.
        agendamentos_consumidos = db.query(AgendamentoDB).filter(
            AgendamentoDB.cliente_id == compra.cliente_id,
            AgendamentoDB.servico_id.in_([s.id for s in compra.pacote.servicos]),
            AgendamentoDB.status == 'concluido',
            AgendamentoDB.data_hora_inicio >= compra.data_compra,
            AgendamentoDB.data_hora_inicio <= compra.data_expiracao
        ).options(
            joinedload(AgendamentoDB.servico) # Carrega os detalhes do serviço
        ).order_by(AgendamentoDB.data_hora_inicio.asc()).all()

        # Monta a lista de itens de consumo para o relatório
        consumo_itens = [
            RelatorioConsumoItem(data_uso=ag.data_hora_inicio, servico_nome=ag.servico.nome)
            for ag in agendamentos_consumidos
        ]

        # Monta o objeto final do relatório para esta compra
        relatorio = RelatorioConsumoPacote(
            cliente_nome=compra.cliente.nome,
            pacote_nome=compra.pacote.nome,
            data_compra=compra.data_compra,
            data_expiracao=compra.data_expiracao,
            sessoes_total=compra.pacote.quantidade_sessoes,
            sessoes_saldo=compra.saldo_sessoes,
            status=compra.status,
            consumo=consumo_itens
        )
        relatorios_finais.append(relatorio)

    return relatorios_finais
