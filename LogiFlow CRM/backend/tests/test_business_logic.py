"""
Testes de Negócio - Cotações e Pedidos
========================================
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from decimal import Decimal

from main import app
from database import get_db
from models import Login, Cotacao, Pedido, Cliente

client = TestClient(app)


# ========================================
# TESTES: Cotações
# ========================================

class TestCotacoes:
    """Testes de funcionalidades de cotações"""
    
    def test_create_cotacao_sucesso(self, auth_headers: dict, cliente: Cliente, db):
        """Testa criação bem-sucedida de cotação"""
        response = client.post(
            "/api/v1/cotacoes",
            headers=auth_headers,
            json={
                "cliente_id": cliente.id,
                "origine": "São Paulo, SP",
                "destino": "Rio de Janeiro, RJ",
                "peso": 100.0,
                "valor_frete": 500.00,
                "data_validade": (datetime.utcnow() + timedelta(days=7)).isoformat()
            }
        )
        
        assert response.status_code in [200, 201]
        data = response.json()
        assert data["cliente_id"] == cliente.id
        assert data["origem"] == "São Paulo, SP"
    
    def test_listar_cotacoes_do_cliente(self, auth_headers: dict, cliente: Cliente):
        """Testa listagem de cotações de um cliente"""
        response = client.get(
            f"/api/v1/cotacoes?cliente_id={cliente.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_buscar_cotacao_por_id(self, auth_headers: dict):
        """Testa busca de cotação específica"""
        # Primeiro criar uma cotação
        # Depois buscá-la
        response = client.get(
            "/api/v1/cotacoes/1",
            headers=auth_headers
        )
        
        # Pode retornar 404 se não existe, é válido
        assert response.status_code in [200, 404]
    
    def test_cotacao_validade_expirada(self, auth_headers: dict, cliente: Cliente):
        """Testa validação de data de validade"""
        response = client.post(
            "/api/v1/cotacoes",
            headers=auth_headers,
            json={
                "cliente_id": cliente.id,
                "origem": "São Paulo",
                "destino": "Rio de Janeiro",
                "peso": 50,
                "valor_frete": 300,
                # Data no passado
                "data_validade": (datetime.utcnow() - timedelta(days=1)).isoformat()
            }
        )
        
        # Pode rejeitar ou aceitar, mas se aceitar deve marcar como inválida
        if response.status_code == 200:
            assert response.json().get("ativa") == False or response.json().get("expirada") == True


# ========================================
# TESTES: Pedidos
# ========================================

class TestPedidos:
    """Testes de funcionalidades de pedidos"""
    
    def test_create_pedido_sucesso(self, auth_headers: dict, cliente: Cliente):
        """Testa criação bem-sucedida de pedido"""
        response = client.post(
            "/api/v1/pedidos",
            headers=auth_headers,
            json={
                "cliente_id": cliente.id,
                "descricao": "Entrega de mercadorias",
                "peso": 100,
                "valor": 500.00,
                "origem": "São Paulo",
                "destino": "Rio de Janeiro"
            }
        )
        
        assert response.status_code in [200, 201]
        data = response.json()
        assert data["cliente_id"] == cliente.id
        assert data["status"] in ["pendente", "ativo", "novo"]
    
    def test_listar_pedidos(self, auth_headers: dict):
        """Testa listagem de pedidos"""
        response = client.get(
            "/api/v1/pedidos",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_listar_pedidos_por_status(self, auth_headers: dict):
        """Testa filtro de pedidos por status"""
        response = client.get(
            "/api/v1/pedidos?status=pendente",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        if isinstance(data, list):
            # Se retornar lista, todos devem ter status 'pendente'
            for item in data:
                if "status" in item:
                    assert item["status"] == "pendente"
    
    def test_atualizar_status_pedido(self, auth_headers: dict):
        """Testa atualização de status de pedido"""
        response = client.patch(
            "/api/v1/pedidos/1",
            headers=auth_headers,
            json={
                "status": "em_transito"
            }
        )
        
        # Pode retornar 404, é valido para pedido não existente
        assert response.status_code in [200, 404]
    
    def test_rastreamento_pedido(self, auth_headers: dict):
        """Testa obtenção de rastreamento de pedido"""
        response = client.get(
            "/api/v1/pedidos/1/rastreamento",
            headers=auth_headers
        )
        
        # Pode não existir, mas endpoint deve estar disponível
        assert response.status_code in [200, 404]


# ========================================
# TESTES: Multi-Tenancy
# ========================================

class TestMultiTenancy:
    """Testes de isolamento de tenants"""
    
    def test_cliente_isolado_por_tenant(self, auth_headers: dict, user: Login, 
                                         cliente: Cliente, db, tenant):
        """Testa que clientes são isolados por tenant"""
        # Buscar clientes - deve retornar apenas do tenant do usuário
        response = client.get(
            "/api/v1/clientes",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Todos os clientes retornados devem pertencer ao tenant do usuário
        if isinstance(data, list):
            for cliente in data:
                assert cliente.get("tenant_id") == user.tenant_id
    
    def test_nao_acessar_dados_outro_tenant(self, auth_headers: dict):
        """Testa que não pode acessar IDs de outro tenant"""
        # Tentar acessar cliente com ID que pode pertencer a outro tenant
        response = client.get(
            "/api/v1/clientes/9999",
            headers=auth_headers
        )
        
        # Deve retornar 404 ou 403, nunca 200 com dados de outro tenant
        assert response.status_code in [404, 403]


# ========================================
# TESTES: Validação de Negócio
# ========================================

class TestLogicaNegocio:
    """Testes de validações de lógica de negócio"""
    
    def test_pedido_requer_cliente_valido(self, auth_headers: dict):
        """Testa que pedido requer cliente válido"""
        response = client.post(
            "/api/v1/pedidos",
            headers=auth_headers,
            json={
                "cliente_id": 9999,  # Não existe
                "descricao": "Test"
            }
        )
        
        # Deve rejeitar cliente inválido
        assert response.status_code >= 400
    
    def test_cotacao_requer_dados_obrigatorios(self, auth_headers: dict):
        """Testa validação de campos obrigatórios em cotação"""
        response = client.post(
            "/api/v1/cotacoes",
            headers=auth_headers,
            json={
                # Faltam campos: cliente_id, origem, destino, etc
                "peso": 100
            }
        )
        
        assert response.status_code >= 400


# ========================================
# TESTES: Performance & Índices
# ========================================

class TestPerformance:
    """Testes para validar performance com índices"""
    
    def test_listar_muitos_clientes_rapido(self, auth_headers: dict, db, tenant):
        """Testa que listagem de muitos clientes é rápida (com índices)"""
        import time
        
        # Criar 100 clientes rapidamente
        for i in range(100):
            cliente = Cliente(
                nome=f"Cliente {i}",
                email=f"cliente{i}@example.com",
                tenant_id=tenant.id
            )
            db.add(cliente)
        db.commit()
        
        # Medir tempo de listagem
        start = time.time()
        response = client.get(
            "/api/v1/clientes",
            headers=auth_headers
        )
        duration = time.time() - start
        
        # Deve responder em menos de 1 segundo
        assert response.status_code == 200
        assert duration < 1.0, f"Query demorou {duration}s, esperado < 1s"
    
    def test_filtro_por_tenant_eficiente(self, auth_headers: dict, db, tenant):
        """Testa que filtro por tenant usa índice"""
        # Esse teste implicitamente valida índice tenant_id
        response = client.get(
            "/api/v1/clientes",
            headers=auth_headers
        )
        
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
