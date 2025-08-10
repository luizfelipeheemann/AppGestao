from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from uuid import UUID

from backend.models.agendamento import Agendamento as AgendamentoDB
from backend.models.cliente import Cliente as ClienteDB
from backend.schemas.agendamento_inteligente import AgendamentoSugestao, ErroAgendamento

def obter_ultimo_agendamento(cliente_id: UUID, db: Session):
    return db.query(AgendamentoDB).filter(
        AgendamentoDB.cliente_id == str(cliente_id)
    ).order_by(AgendamentoDB.data_hora_inicio.desc()).first()

def sugerir_horarios(cliente_id: UUID, data: datetime.date, duracao_em_minutos: int, db: Session):
    agendamentos_do_dia = db.query(AgendamentoDB).filter(
        AgendamentoDB.data_hora_inicio >= datetime.combine(data, datetime.min.time()),
        AgendamentoDB.data_hora_inicio <= datetime.combine(data, datetime.max.time())
    ).order_by(AgendamentoDB.data_hora_inicio).all()

    horarios_ocupados = [
        (a.data_hora_inicio, a.data_hora_inicio + timedelta(minutes=a.duracao_minutos))
        for a in agendamentos_do_dia
    ]

    inicio = datetime.combine(data, datetime.strptime("08:00", "%H:%M").time())
    fim = datetime.combine(data, datetime.strptime("20:00", "%H:%M").time())
    slot = timedelta(minutes=duracao_em_minutos)
    sugestoes = []

    while inicio + slot <= fim:
        conflito = any([inicio < fim_ocupado and inicio + slot > ini_ocupado for ini_ocupado, fim_ocupado in horarios_ocupados])
        if not conflito:
            sugestoes.append(inicio)
        inicio += timedelta(minutes=30)

    if not sugestoes:
        raise ErroAgendamento(code="ERRO-AGENDA004", message="Não há horários disponíveis para a duração deste serviço na data selecionada.")

    return sugestoes
