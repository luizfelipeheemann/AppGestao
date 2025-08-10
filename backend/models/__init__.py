# Código para: backend/models/__init__.py
from sqlalchemy import Table, Column, String, ForeignKey
from backend.core.database import Base

# Define a tabela de associação aqui, em um local central.
# Ela conecta as tabelas 'pacotes_servicos' e 'servicos'.
pacote_servico_association = Table('pacote_servico_association', Base.metadata,
    Column('pacote_id', String(36), ForeignKey('pacotes_servicos.id'), primary_key=True),
    Column('servico_id', String(36), ForeignKey('servicos.id'), primary_key=True)
)

# Importa os modelos para que o SQLAlchemy os reconheça.
# Esta abordagem é mais simples do que a do main.py e funciona bem aqui.
from . import agendamento, cliente, cliente_pacote, pacote, pagamento, servico, usuario
