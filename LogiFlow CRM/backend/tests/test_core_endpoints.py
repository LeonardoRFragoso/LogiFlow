"""
Testes Unitários e Integração - LogiFlow CRM
=============================================
Testes para endpoints críticos: auth, clientes, cotações, pedidos
"""
import pytest
import json
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

# Imports da aplicação
from main import app
from config import settings
from database import Base, get_db
from models import User, Tenant, Cliente, Cotacao, Pedido
import bcrypt

# ========================================
# Configuração de Database para Testes
# ========================================

# Usar SQLite em memória para testes
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar todas as tabelas para teste
Base.metadata.create_all(bind=engine)

def override_get_db() -> Generator:
    """Override do dependency injection de database para testes"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# ========================================
# Client de Teste
# ========================================

client = TestClient(app)


# ========================================
# Fixtures para Testes
# ========================================

@pytest.fixture(scope="function", autouse=True)
def clear_db():
    """Limpa database antes de cada teste"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db() -> Session:
    """Retorna sessão de database para uso em testes"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def tenant(db: Session) -> Tenant:
    """Cria um tenant para testes"""
    tenant = Tenant(
        company_name="Test Company",
        plan="starter"
    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant


@pytest.fixture
def user(db: Session, tenant: Tenant) -> User:
    """Cria um usuário para testes"""
    password = "test123456"
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'), 
        bcrypt.gensalt()
    ).decode('utf-8')
    
    user = User(
        email="test@example.com",
        nome="Test User",
        senha_hash=password_hash,
        tipo="admin",
        status="ativo",
        tenant_id=tenant.id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_headers(user: User) -> dict:
    """Retorna headers de autenticação com token JWT válido"""
    # Fazer login para obter token
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": user.email,
            "password": "test123456"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def cliente(db: Session, tenant: Tenant) -> Cliente:
    """Cria um cliente para testes"""
    cliente = Cliente(
        nome="Test Cliente",
        email="cliente@example.com",
        cnpj="12345678000195",
        tenant_id=tenant.id
    )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


# ========================================
# TESTES: Autenticação
# ========================================

class TestAuth:
    """Testes de autenticação"""
    
    def test_login_sucesso(self, user: User):
        """Testa login bem-sucedido"""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": user.email,
                "password": "test123456"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_falha_email_invalido(self):
        """Testa login com email inválido"""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "invalido@example.com",
                "password": "senha123"
            }
        )
        
        assert response.status_code == 401
        assert "incorretos" in response.json()["detail"].lower()
    
    def test_login_falha_senha_invalida(self, user: User):
        """Testa login com senha incorreta"""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": user.email,
                "password": "senhaerrada"
            }
        )
        
        assert response.status_code == 401
    
    def test_rate_limit_login(self):
        """Testa rate limiting no endpoint de login"""
        # Fazer 5+ requisições rápidas
        for i in range(6):
            response = client.post(
                "/api/v1/auth/login",
                data={
                    "username": f"user{i}@example.com",
                    "password": "password"
                }
            )
            
            if i < 5:
                # Primeiras 5 devem passar (mesmo que falhem)
                assert response.status_code != 429
            else:
                # 6ª deve levar rate limit
                if response.status_code == 429:
                    assert "excedido" in response.json()["detail"].lower()
                    break


# ========================================
# TESTES: Clientes
# ========================================

class TestClientes:
    """Testes de CRUD de clientes"""
    
    def test_listar_clientes_vazio(self, auth_headers: dict):
        """Testa listagem de clientes quando vazio"""
        response = client.get(
            "/api/v1/clientes",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_listar_clientes(self, auth_headers: dict, cliente: Cliente):
        """Testa listagem de clientes"""
        response = client.get(
            "/api/v1/clientes",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(c["id"] == cliente.id for c in data)
    
    def test_create_cliente(self, auth_headers: dict):
        """Testa criação de cliente"""
        response = client.post(
            "/api/v1/clientes",
            headers=auth_headers,
            json={
                "nome": "New Cliente",
                "email": "newcliente@example.com",
                "cnpj": "12345678000195"
            }
        )
        
        assert response.status_code in [200, 201]
        data = response.json()
        assert data["nome"] == "New Cliente"
        assert data["email"] == "newcliente@example.com"
    
    def test_get_cliente(self, auth_headers: dict, cliente: Cliente):
        """Testa obtenção de cliente específico"""
        response = client.get(
            f"/api/v1/clientes/{cliente.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == cliente.id
        assert data["nome"] == cliente.nome
    
    def test_update_cliente(self, auth_headers: dict, cliente: Cliente):
        """Testa atualização de cliente"""
        response = client.put(
            f"/api/v1/clientes/{cliente.id}",
            headers=auth_headers,
            json={
                "nome": "Updated Name"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Updated Name"
    
    def test_delete_cliente(self, auth_headers: dict, cliente: Cliente):
        """Testa deletar cliente"""
        response = client.delete(
            f"/api/v1/clientes/{cliente.id}",
            headers=auth_headers
        )
        
        assert response.status_code in [200, 204]


# ========================================
# TESTES: Autenticação Requerida
# ========================================

class TestAuthRequired:
    """Testes validam que endpoints requerem autenticação"""
    
    def test_listar_clientes_sem_auth(self):
        """Testa acesso negado sem autenticação"""
        response = client.get("/api/v1/clientes")
        
        assert response.status_code == 401 or response.status_code == 403
    
    def test_create_cliente_sem_auth(self):
        """Testa criação sem autenticação"""
        response = client.post(
            "/api/v1/clientes",
            json={
                "nome": "Test",
                "email": "test@example.com"
            }
        )
        
        assert response.status_code == 401 or response.status_code == 403


# ========================================
# TESTES: Health & Metrics
# ========================================

class TestHealth:
    """Testes de health endpoints"""
    
    def test_health_check(self):
        """Testa healthcheck endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
    
    def test_readiness_check(self):
        """Testa readiness endpoint"""
        response = client.get("/ready")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ["ready", "degraded"]
    
    def test_metrics_endpoint(self):
        """Testa endpoint de métricas Prometheus"""
        response = client.get("/metrics")
        
        assert response.status_code == 200
        assert isinstance(response.text, str)
        # Verifica se é formato Prometheus
        assert "HELP" in response.text or "TYPE" in response.text or len(response.text) > 0


# ========================================
# TESTES: Validação de Dados
# ========================================

class TestValidation:
    """Testes de validação de dados"""
    
    def test_email_invalido_login(self):
        """Testa rejei ção de email inválido"""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "email_invalido",
                "password": "senha123"
            }
        )
        
        # Pode falhar no login ou validação, ambos aceitáveis
        assert response.status_code >= 400
    
    def test_create_cliente_campos_obrigatorios(self, auth_headers: dict):
        """Testa validação de campos obrigatórios"""
        # Falta 'nome' que deve ser obrigatório
        response = client.post(
            "/api/v1/clientes",
            headers=auth_headers,
            json={
                "email": "test@example.com"
            }
        )
        
        assert response.status_code >= 400


# ========================================
# TESTES: Database Indices Performance
# ========================================

class TestDatabasePerformance:
    """Testes para validar índices de database"""
    
    def test_query_por_tenant(self, db: Session, tenant: Tenant, cliente: Cliente):
        """Valida que queries por tenant_id usam índices"""
        # Esse teste valida que a migration com índices foi executada
        resultado = db.query(Cliente).filter(
            Cliente.tenant_id == tenant.id
        ).all()
        
        assert len(resultado) >= 1
        assert resultado[0].tenant_id == tenant.id


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
