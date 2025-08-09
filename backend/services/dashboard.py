from fastapi import HTTPException
from sqlalchemy import func
from database import get_db
from models import Cliente as ClienteDB, Servico as ServicoDB, Agendamento as AgendamentoDB, Pagamento as PagamentoDB
from datetime import datetime, date
from typing import Dict

def get_dashboard_stats() -> Dict:
    db = next(get_db())
    today = date.today()
    total = db.query(func.count(ClienteDB.id)).scalar()
    clientes_mes = db.query(func.count(ClienteDB.id)).filter(ClienteDB.data_criacao >= today.replace(day=1)).scalar()
    servicos_ativos = db.query(func.count(ServicoDB.id)).filter(ServicoDB.ativo == True).scalar()
    agendamentos_hoje = db.query(func.count(AgendamentoDB.id)).filter(
        AgendamentoDB.data_hora_inicio.between(
            datetime.combine(today, datetime.min.time()),
            datetime.combine(today, datetime.max.time())
        )
    ).scalar()
    receita_mes = db.query(func.sum(PagamentoDB.valor)).filter(
        func.extract('month', PagamentoDB.data_criacao) == today.month,
        func.extract('year', PagamentoDB.data_criacao) == today.year,
        PagamentoDB.status == 'pago'
    ).scalar() or 0

    return {
        "totalClientes": total,
        "clientesNoMes": clientes_mes,
        "servicosAtivos": servicos_ativos,
        "agendamentosHoje": agendamentos_hoje,
        "receitaMes": receita_mes
    }

def get_proximos_agendamentos(limit: int = 5):
    db = next(get_db())
    now = datetime.utcnow()
    return db.query(AgendamentoDB).filter(
        AgendamentoDB.data_hora_inicio >= now,
        AgendamentoDB.status == 'confirmado'
    ).order_by(AgendamentoDB.data_hora_inicio).limit(limit)\
      .options(AgendamentoDB.cliente, AgendamentoDB.servico).all()
