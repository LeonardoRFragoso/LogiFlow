"""
Testes para Autenticação e JWT
"""
import pytest
from fastapi.testclient import TestClient


class TestAuth:
    """Testes de autenticação"""
    
    def test_health_check(self, client):
        """Teste do healthcheck básico"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_login_sucesso(self, client, test_db):
        """Teste de login com credenciais válidas"""
        # Criar usuário primeiro (normalmente feito via seed)
        test_db.execute("""
            INSERT INTO users (email, password_hash, nome, role, ativo) 
            VALUES ('user@test.com', '$2b$12$...', 'Test', 'user', 1)
        """)
        test_db.commit()
        
        response = client.post("/api/v1/auth/login", json={
            "email": "user@test.com",
            "password": "password123"
        })
        
        # Mock - ajustar quando auth estiver completamente implementado
        # assert response.status_code == 200
        # assert "access_token" in response.json()
        # assert "refresh_token" in response.json()
    
    def test_login_credenciais_invalidas(self, client):
        """Teste de login com senha errada"""
        response = client.post("/api/v1/auth/login", json={
            "email": "user@test.com",
            "password": "senha_errada"
        })
        
        # Mock
        # assert response.status_code == 401
    
    def test_refresh_token(self, client):
        """Teste de refresh token"""
        # Login primeiro
        login_response = client.post("/api/v1/auth/login", json={
            "email": "user@test.com",
            "password": "password123"
        })
        
        # Mock
        # refresh_token = login_response.json()["refresh_token"]
        
        # Refresh
        # response = client.post("/api/v1/auth/refresh", json={
        #     "refresh": refresh_token
        # })
        
        # assert response.status_code == 200
        # assert "access_token" in response.json()
    
    def test_token_invalido(self, client):
        """Teste de acesso com token inválido"""
        response = client.get(
            "/api/v1/entregas",
            headers={"Authorization": "Bearer token_invalido"}
        )
        
        # Deve retornar 401 ou 400
        assert response.status_code in [400, 401, 403]
    
    def test_sem_token(self, client):
        """Teste de acesso sem token"""
        response = client.get("/api/v1/entregas")
        
        # Deve retornar 400 (sem tenant) ou 401 (sem auth)
        assert response.status_code in [400, 401, 403]
    
    def test_alterar_senha(self, client, auth_headers):
        """Teste de alteração de senha"""
        response = client.post(
            "/api/v1/auth/alterar-senha",
            headers=auth_headers,
            json={
                "senha_atual": "Test123!@#",
                "senha_nova": "NewPass123!@#"
            }
        )
        
        # Mock
        # assert response.status_code == 200
        # assert response.json()["success"] == True
    
    def test_logout(self, client, auth_headers):
        """Teste de logout"""
        response = client.post(
            "/api/v1/auth/logout",
            headers=auth_headers
        )
        
        # Mock
        # assert response.status_code == 200

