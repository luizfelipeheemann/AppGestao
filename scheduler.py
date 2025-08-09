from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload

from database import SessionLocal, ClientePacote as ClientePacoteDB
from logging_config import get_logger

# Logger específico para o agendador
logger = get_logger("scheduler")

def check_expiring_packages():
    """
    Verifica os pacotes de clientes que expiram nos próximos 7 dias
    e dispara uma notificação (atualmente, um log).
    """
    logger.info("Iniciando verificação de pacotes a expirar...")
    db = SessionLocal()
    try:
        # Define o período de verificação (hoje + 7 dias)
        notification_days = 7
        today = datetime.utcnow().date()
        expiration_limit = today + timedelta(days=notification_days)

        # Busca pacotes que estão ativos, com saldo, e que expiram no período definido
        expiring_packages = db.query(ClientePacoteDB).options(
            joinedload(ClientePacoteDB.cliente),
            joinedload(ClientePacoteDB.pacote)
        ).filter(
            ClientePacoteDB.status == 'ativo',
            ClientePacoteDB.saldo_sessoes > 0,
            ClientePacoteDB.data_expiracao >= today,
            ClientePacoteDB.data_expiracao < expiration_limit
        ).all()

        if not expiring_packages:
            logger.info("Nenhum pacote a expirar nos próximos 7 dias foi encontrado.")
            return

        logger.info(f"Encontrados {len(expiring_packages)} pacotes a expirar.")

        for pkg in expiring_packages:
            days_left = (pkg.data_expiracao.date() - today).days
            
            # SIMULAÇÃO DE NOTIFICAÇÃO (US043)
            # No futuro, esta parte chamaria um serviço de e-mail ou WhatsApp (Épico 5)
            logger.info(
                "NOTIFICAÇÃO: Pacote expirando",
                cliente_nome=pkg.cliente.nome,
                cliente_email=pkg.cliente.email,
                pacote_nome=pkg.pacote.nome,
                saldo_restante=pkg.saldo_sessoes,
                dias_restantes=days_left
            )
            # Fim da simulação

    except Exception as e:
        logger.error("Erro ao verificar pacotes expirando", error=str(e))
    finally:
        db.close()

# Criação da instância do agendador
scheduler = BackgroundScheduler(timezone="UTC")

# Adiciona a tarefa para rodar todos os dias à meia-noite (UTC)
scheduler.add_job(check_expiring_packages, 'cron', hour=0, minute=0)
