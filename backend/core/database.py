from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import scoped_session
import os
from config import settings # Importa as configurações

# Usa a URL do banco de dados a partir do arquivo de configuração
DATABASE_URL = settings.DATABASE_URL

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    poolclass=StaticPool if "sqlite" in DATABASE_URL else None
)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

class CustomBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

Base = declarative_base(cls=CustomBase)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    # A importação foi removida para quebrar o ciclo.
    # Os modelos serão importados em outro lugar antes desta função ser chamada.
    Base.metadata.create_all(bind=engine)
