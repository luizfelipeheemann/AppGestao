import pytest
import os
import tempfile
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Set test environment
os.environ["ENVIRONMENT"] = "test"
os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from main import app
from database import get_db, Base
from auth import create_access_token


@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={
            "check_same_thread": False,
        },
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="function")
def test_db(test_engine):
    """Create test database session"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(test_db):
    """Create test client with database override"""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def auth_token():
    """Create authentication token for testing"""
    token_data = {"sub": "test@example.com", "user_id": "test-user-id"}
    return create_access_token(data=token_data)


@pytest.fixture
def auth_headers(auth_token):
    """Create authorization headers for testing"""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def sample_cliente_data():
    """Sample client data for testing"""
    return {
        "nome": "João Silva",
        "telefone": "+5511999999999",
        "email": "joao@teste.com",
        "observacoes": "Cliente de teste",
        "etiquetas": ["teste", "novo"]
    }


@pytest.fixture
def sample_servico_data():
    """Sample service data for testing"""
    return {
        "nome": "Consulta Teste",
        "descricao": "Serviço de teste",
        "preco": 100.0,
        "duracao_minutos": 60,
        "ativo": True
    }


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "nome": "Usuário Teste",
        "email": "usuario@teste.com",
        "senha": "TestPassword123"
    }

