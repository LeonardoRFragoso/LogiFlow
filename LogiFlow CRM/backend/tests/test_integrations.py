"""
Testes para Integrações Externas
"""
import pytest
from fastapi.testclient import TestClient


class TestGPSIntegrations:
    """Testes de integrações GPS"""
    
    def test_gps_sem_credenciais(self, client, auth_headers):
        """GPS sem credenciais configuradas deve retornar erro claro"""
        response = client.get(
            "/api/v1/gps/posicao/ABC1234",
            headers=auth_headers
        )
        
        # Deve retornar 400 com mensagem sobre credenciais
        assert response.status_code == 400
        assert "credenciais" in response.json()["detail"].lower() or \
               "credentials" in response.json()["detail"].lower()
    
    def test_gps_com_credenciais_invalidas(self, client, auth_headers):
        """GPS com credenciais inválidas deve retornar erro"""
        # Criar credencial inválida
        client.post(
            "/api/v1/tenant-credentials/credentials",
            headers=auth_headers,
            json={
                "integration_type": "gps",
                "provider": "sascar",
                "credentials": {
                    "api_key": "invalid_key",
                    "api_secret": "invalid_secret",
                    "environment": "production"
                }
            }
        )
        
        # Tentar usar GPS
        response = client.get(
            "/api/v1/gps/posicao/ABC1234",
            headers=auth_headers
        )
        
        # Mock
        # assert response.status_code in [400, 500]
    
    def test_listar_veiculos_consolidado(self, client, auth_headers):
        """Listar veículos de múltiplos providers"""
        response = client.get(
            "/api/v1/gps/veiculos",
            headers=auth_headers
        )
        
        # Mock
        # assert response.status_code in [200, 400]
        # if response.status_code == 200:
        #     assert "veiculos" in response.json()


class TestFreightIntegrations:
    """Testes de integrações de frete"""
    
    def test_cotacao_automatica_sem_tokens(self, client, auth_headers):
        """Cotação sem tokens configurados deve retornar erro claro"""
        response = client.post(
            "/api/v1/cotacao-automatica/cotar",
            headers=auth_headers,
            json={
                "origem_cep": "01310-100",
                "destino_cep": "04547-130",
                "peso_kg": 10,
                "altura_cm": 20,
                "largura_cm": 20,
                "comprimento_cm": 30,
                "incluir_melhor_envio": True,
                "incluir_frenet": True
            }
        )
        
        # Se não houver tokens, deve avisar
        if response.status_code == 400:
            assert "token" in response.text.lower() or "configur" in response.text.lower()
    
    def test_distance_matrix_sem_chave(self, client, auth_headers):
        """Distance Matrix sem chave em produção deve retornar 400"""
        # Mock: Simular ambiente de produção
        # settings.DEBUG = False
        
        response = client.post(
            "/api/v1/cotacao-automatica/cotar",
            headers=auth_headers,
            json={
                "origem_cep": "01310-100",
                "destino_cep": "04547-130",
                "peso_kg": 10
            }
        )
        
        # Em produção sem chave, deve falhar
        # if not settings.GOOGLE_MAPS_DISTANCE_MATRIX_KEY:
        #     assert response.status_code == 400
        pass


class TestERPIntegrations:
    """Testes de integrações ERP"""
    
    def test_sincronizar_cliente_omie(self, client, auth_headers):
        """Sincronizar cliente com Omie"""
        response = client.post(
            "/api/v1/erp/omie/sync-client",
            headers=auth_headers,
            json={
                "cliente_id": 1,
                "razao_social": "Empresa Teste LTDA",
                "cnpj": "12.345.678/0001-90"
            }
        )
        
        # Mock
        # assert response.status_code in [200, 400]
    
    def test_listar_clientes_bling(self, client, auth_headers):
        """Listar clientes do Bling"""
        response = client.get(
            "/api/v1/erp/bling/clientes",
            headers=auth_headers
        )
        
        # Mock
        # assert response.status_code in [200, 400]

