from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import scoped_session
import os

# Usar SQLite como padrão (pode ser trocado por PostgreSQL ou outro)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Configurações específicas para SQLite
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

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.__dict__})>"

Base = declarative_base(cls=CustomBase)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    import backend.models  # Importa os models para criar as tabelas
    Base.metadata.create_all(bind=engine)
