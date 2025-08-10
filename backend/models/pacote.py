# Código para: backend/models/pacote.py
import uuid
from sqlalchemy import Column, String, Text, Float, Integer, Boolean
from sqlalchemy.orm import relationship
from backend.core.database import Base
# Importa a tabela de associação do __init__.py da pasta 'models'
from . import pacote_servico_association

class PacoteServico(Base):
    __tablename__ = "pacotes_servicos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String(100), nullable=False, index=True)
    descricao = Column(Text, nullable=True)
    preco = Column(Float, nullable=False)
    quantidade_sessoes = Column(Integer, nullable=False)
    validade_dias = Column(Integer, nullable=False)
    ativo = Column(Boolean, default=True, index=True)

    # A relação agora usa a tabela importada
    servicos = relationship("Servico", secondary=pacote_servico_association, back_populates="pacotes")
    compras = relationship("ClientePacote", back_populates="pacote", cascade="all, delete-orphan")
