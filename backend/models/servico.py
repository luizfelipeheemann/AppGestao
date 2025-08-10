# Código para: backend/models/servico.py
import uuid
from sqlalchemy import Column, String, Text, Float, Integer, Boolean
from sqlalchemy.orm import relationship
from backend.core.database import Base
# Importa a tabela de associação do __init__.py da pasta 'models'
from . import pacote_servico_association

class Servico(Base):
    __tablename__ = "servicos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String(100), nullable=False, index=True)
    descricao = Column(Text, nullable=True)
    preco = Column(Float, nullable=False)
    duracao_minutos = Column(Integer, nullable=True)
    ativo = Column(Boolean, default=True, index=True)

    agendamentos = relationship("Agendamento", back_populates="servico")
    # A relação agora usa a tabela importada
    pacotes = relationship("PacoteServico", secondary=pacote_servico_association, back_populates="servicos")
