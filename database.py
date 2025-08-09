from sqlalchemy import create_engine, Column, String, Float, Integer, Boolean, DateTime, Text, ForeignKey, Table, Index
from sqlalchemy.orm import sessionmaker, Session, relationship, declarative_base
from sqlalchemy.sql import func
from config import settings
from logging_config import get_logger
import uuid
from datetime import datetime, timedelta
from typing import Generator

logger = get_logger("database")

# Configuração do banco de dados
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
    echo=not settings.is_production
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Dependência para obter a sessão do banco de dados"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error("Erro na sessão do banco de dados", error=str(e))
        db.rollback()
        raise
    finally:
        db.close()


# Modelos do Banco de Dados
class BaseModel(Base):
    __abstract__ = True
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())


class Usuario(BaseModel):
    __tablename__ = "usuarios"
    
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    ativo = Column(Boolean, default=True)
    
    __table_args__ = (
        Index('ix_usuarios_email', 'email'),
    )
    
    def __repr__(self):
        return f"<Usuario(email='{self.email}', nome='{self.nome}')>"


class Cliente(BaseModel):
    __tablename__ = "clientes"
    
    nome = Column(String(100), nullable=False, index=True)
    telefone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=True, index=True)
    observacoes = Column(Text, nullable=True)
    etiquetas = Column(Text, nullable=True)
    
    agendamentos = relationship("Agendamento", back_populates="cliente", cascade="all, delete-orphan")
    precos_personalizados = relationship("PrecoPersonalizado", back_populates="cliente", cascade="all, delete-orphan")
    pacotes_adquiridos = relationship("ClientePacote", back_populates="cliente", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('ix_clientes_email', 'email'),
    )
    
    def __repr__(self):
        return f"<Cliente(nome='{self.nome}', telefone='{self.telefone}')>"


pacote_servico_association = Table('pacote_servico_association', Base.metadata,
    Column('pacote_id', String(36), ForeignKey('pacotes_servicos.id'), primary_key=True),
    Column('servico_id', String(36), ForeignKey('servicos.id'), primary_key=True)
)


class Servico(BaseModel):
    __tablename__ = "servicos"
    
    nome = Column(String(100), nullable=False, index=True)
    descricao = Column(Text, nullable=True)
    preco = Column(Float, nullable=False)
    duracao_minutos = Column(Integer, nullable=True)
    ativo = Column(Boolean, default=True, index=True)
    
    agendamentos = relationship("Agendamento", back_populates="servico")
    precos_personalizados = relationship("PrecoPersonalizado", back_populates="servico", cascade="all, delete-orphan")
    pacotes = relationship("PacoteServico", secondary=pacote_servico_association, back_populates="servicos")
    
    def __repr__(self):
        return f"<Servico(nome='{self.nome}', preco={self.preco})>"


class Agendamento(BaseModel):
    __tablename__ = "agendamentos"
    
    cliente_id = Column(String(36), ForeignKey("clientes.id"), nullable=False, index=True)
    servico_id = Column(String(36), ForeignKey("servicos.id"), nullable=False, index=True)
    data_hora_inicio = Column(DateTime(timezone=True), nullable=False, index=True)
    data_hora_fim = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(20), default="confirmado", index=True)
    observacoes = Column(Text, nullable=True)
    
    cliente = relationship("Cliente", back_populates="agendamentos")
    servico = relationship("Servico", back_populates="agendamentos")
    pagamentos = relationship("Pagamento", back_populates="agendamento", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('ix_agendamentos_data_hora_inicio', 'data_hora_inicio'),
    )
    
    def __repr__(self):
        return f"<Agendamento(cliente_id='{self.cliente_id}', data_inicio='{self.data_hora_inicio}')>"


class Pagamento(BaseModel):
    __tablename__ = "pagamentos"
    
    agendamento_id = Column(String(36), ForeignKey("agendamentos.id"), nullable=False, index=True)
    valor = Column(Float, nullable=False)
    metodo_pagamento = Column(String(50), nullable=False, index=True)
    status = Column(String(20), default="pendente", index=True)
    descricao = Column(Text, nullable=True)
    link_pagamento = Column(String(500), nullable=True)
    
    agendamento = relationship("Agendamento", back_populates="pagamentos")
    
    def __repr__(self):
        return f"<Pagamento(valor={self.valor}, status='{self.status}')>"


class PacoteServico(BaseModel):
    __tablename__ = "pacotes_servicos"
    
    nome = Column(String(100), nullable=False, index=True)
    descricao = Column(Text, nullable=True)
    preco = Column(Float, nullable=False)
    quantidade_sessoes = Column(Integer, nullable=False)
    validade_dias = Column(Integer, nullable=False)
    ativo = Column(Boolean, default=True, index=True)
    
    servicos = relationship("Servico", secondary=pacote_servico_association, back_populates="pacotes")
    compras = relationship("ClientePacote", back_populates="pacote", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<PacoteServico(nome='{self.nome}', preco={self.preco})>"


class ClientePacote(BaseModel):
    __tablename__ = "cliente_pacotes"
    
    cliente_id = Column(String(36), ForeignKey("clientes.id"), nullable=False, index=True)
    pacote_id = Column(String(36), ForeignKey("pacotes_servicos.id"), nullable=False, index=True)
    data_compra = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    data_expiracao = Column(DateTime(timezone=True), nullable=False)
    saldo_sessoes = Column(Integer, nullable=False)
    status = Column(String(20), default="ativo", index=True)
    
    cliente = relationship("Cliente", back_populates="pacotes_adquiridos")
    pacote = relationship("PacoteServico", back_populates="compras")
    
    def __repr__(self):
        return f"<ClientePacote(cliente_id='{self.cliente_id}', saldo={self.saldo_sessoes})>"


class PrecoPersonalizado(BaseModel):
    __tablename__ = "precos_personalizados"
    
    cliente_id = Column(String(36), ForeignKey("clientes.id"), nullable=False, index=True)
    servico_id = Column(String(36), ForeignKey("servicos.id"), nullable=False, index=True)
    preco_personalizado = Column(Float, nullable=False)
    observacoes = Column(Text, nullable=True)
    ativo = Column(Boolean, default=True, index=True)
    
    cliente = relationship("Cliente", back_populates="precos_personalizados")
    servico = relationship("Servico", back_populates="precos_personalizados")
    
    def __repr__(self):
        return f"<PrecoPersonalizado(cliente_id='{self.cliente_id}', preco={self.preco_personalizado})>"


# Operações do Banco de Dados
class DatabaseManager:
    def __init__(self, db: Session):
        self.db = db
        self.logger = get_logger("db_manager")
    
    def create_tables(self):
        """Cria todas as tabelas"""
        try:
            Base.metadata.create_all(bind=engine)
            self.logger.info("Tabelas do banco de dados criadas com sucesso")
        except Exception as e:
            self.logger.error("Falha ao criar tabelas", error=str(e))
            raise
    
    def seed_demo_data(self):
        """Popula o banco de dados com dados de demonstração"""
        try:
            if self.db.query(Cliente).first():
                self.logger.info("Dados de demonstração já existem, pulando a inserção")
                return
            
            clientes = [
                Cliente(nome="Maria Santos", telefone="+5511888888888", email="maria@exemplo.com", etiquetas="novo,ansiedade"),
                Cliente(nome="Pedro Oliveira", telefone="+5511777777777", email="pedro@exemplo.com", etiquetas="regular,depressão"),
                Cliente(nome="João Silva", telefone="+5511999999999", email="joao.silva@exemplo.com", etiquetas="")
            ]
            self.db.add_all(clientes)
            self.db.commit()

            servico_consulta = Servico(nome="Consulta Psicológica", descricao="Sessão de terapia individual", preco=150.0, duracao_minutos=60, ativo=True)
            servico_avaliacao = Servico(nome="Avaliação Psicológica", descricao="Avaliação completa com relatório", preco=300.0, duracao_minutos=120, ativo=True)
            self.db.add_all([servico_consulta, servico_avaliacao])
            self.db.commit()

            pacote_terapia = PacoteServico(
                nome="Pacote 5 Sessões de Terapia",
                descricao="Um pacote com desconto para 5 sessões de consulta psicológica.",
                preco=650.0,
                quantidade_sessoes=5,
                validade_dias=90,
                ativo=True,
                servicos=[servico_consulta]
            )
            self.db.add(pacote_terapia)
            self.db.commit()

            cliente_maria = self.db.query(Cliente).filter(Cliente.nome == "Maria Santos").first()
            if cliente_maria:
                compra_pacote = ClientePacote(
                    cliente_id=cliente_maria.id,
                    pacote_id=pacote_terapia.id,
                    data_expiracao=datetime.utcnow() + timedelta(days=pacote_terapia.validade_dias),
                    saldo_sessoes=pacote_terapia.quantidade_sessoes
                )
                self.db.add(compra_pacote)
                self.db.commit()

            self.logger.info("Dados de demonstração inseridos com sucesso")
            
        except Exception as e:
            self.logger.error("Falha ao inserir dados de demonstração", error=str(e))
            self.db.rollback()
            raise


def init_database():
    """Inicializa o banco de dados com tabelas e dados de demonstração"""
    db = SessionLocal()
    try:
        db_manager = DatabaseManager(db)
        db_manager.create_tables()
        db_manager.seed_demo_data()
    finally:
        db.close()