"""
Configuração de testes para LogiFlow CRM
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db
from models import User
from config import settings

# Banco de dados de teste em memória
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override do get_db para usar banco de testes"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def test_db():
    """
    Cria banco de dados de testes
    """
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """
    Cliente de testes para fazer requisições
    """
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client):
    """
    Headers de autenticação para testes
    """
    # Criar usuário de teste
    response = client.post("/api/v1/auth/register", json={
        "email": "test@logiflow.com",
        "password": "Test123!@#",
        "nome": "Test User"
    })
    
    # Login
    response = client.post("/api/v1/auth/login", json={
        "email": "test@logiflow.com",
        "password": "Test123!@#"
    })
    
    token = response.json()["access_token"]
    
    return {
        "Authorization": f"Bearer {token}",
        "X-Tenant-ID": "1"
    }


@pytest.fixture
def admin_headers(client):
    """
    Headers de admin para testes
    """
    # Criar admin
    response = client.post("/api/v1/auth/register", json={
        "email": "admin@logiflow.com",
        "password": "Admin123!@#",
        "nome": "Admin User",
        "role": "admin"
    })
    
    # Login
    response = client.post("/api/v1/auth/login", json={
        "email": "admin@logiflow.com",
        "password": "Admin123!@#"
    })
    
    token = response.json()["access_token"]
    
    return {
        "Authorization": f"Bearer {token}",
        "X-Tenant-ID": "1"
    }

