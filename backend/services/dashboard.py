from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from typing import Dict, List
from datetime import datetime, date

# --- Importações Corrigidas ---
from backend.models.cliente import Cliente as ClienteDB
from backend.models.servico import Servico as ServicoDB
from backend.models.agendamento import Agendamento as AgendamentoDB
from backend.models.pagamento import Pagamento as PagamentoDB
# --- Fim das Importações Corrigidas ---

def get_dashboard_stats_srv(db: Session) -> Dict:
    """Busca estatísticas gerais para o dashboard."""
    today = date.today()
    
    total_clientes = db.query(func.count(ClienteDB.id)).scalar()
    
    # Contagem de clientes criados no mês corrente
    clientes_mes = db.query(func.count(ClienteDB.id)).filter(
        func.extract('month', ClienteDB.data_criacao) == today.month,
        func.extract('year', ClienteDB.data_criacao) == today.year
    ).scalar()
    
    servicos_ativos = db.query(func.count(ServicoDB.id)).filter(ServicoDB.ativo == True).scalar()
    
    agendamentos_hoje = db.query(func.count(AgendamentoDB.id)).filter(
        func.date(AgendamentoDB.data_hora_inicio) == today
    ).scalar()
    
    receita_mes = db.query(func.sum(PagamentoDB.valor)).filter(
        func.extract('month', PagamentoDB.data_criacao) == today.month,
        func.extract('year', PagamentoDB.data_criacao) == today.year,
        PagamentoDB.status == 'pago'
    ).scalar() or 0.0 # Garante que o retorno seja float

    return {
        "totalClientes": total_clientes,
        "clientesNoMes": clientes_mes,
        "servicosAtivos": servicos_ativos,
        "agendamentosHoje": agendamentos_hoje,
        "receitaMes": receita_mes
    }

def get_proximos_agendamentos_srv(db: Session, limit: int = 5) -> List[AgendamentoDB]:
    """Busca os próximos agendamentos a partir da data e hora atuais."""
    now = datetime.utcnow()
    return db.query(AgendamentoDB).filter(
        AgendamentoDB.data_hora_inicio >= now,
        AgendamentoDB.status == 'confirmado'
    ).order_by(AgendamentoDB.data_hora_inicio.asc()).limit(limit).options(
        # Usando joinedload para carregar os dados relacionados de forma eficiente
        joinedload(AgendamentoDB.cliente),
        joinedload(AgendamentoDB.servico)
    ).all()
