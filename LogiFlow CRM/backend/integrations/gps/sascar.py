"""
LogiFlow CRM - Integração Sascar
Cliente para rastreamento GPS via API Sascar

MODO SIMULAÇÃO: Este módulo está pronto para uso, mas opera em modo simulação
até que as credenciais reais da Sascar sejam configuradas.

Para ativar:
1. Obter credenciais da Sascar (API Key, Secret)
2. Configurar no .env: SASCAR_API_KEY e SASCAR_API_SECRET
3. Definir SASCAR_SIMULATION_MODE=false
"""

import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random
import logging

logger = logging.getLogger(__name__)


class SascarClient:
    """
    Cliente para API Sascar
    Documentação: https://api.sascar.com.br/docs
    
    Modo Simulação: Retorna dados fictícios para testes
    """
    
    BASE_URL = "https://api.sascar.com.br/v1"
    
    def __init__(self, api_key: str = None, api_secret: str = None, simulation_mode: bool = True):
        """
        Inicializa cliente Sascar
        
        Args:
            api_key: Chave da API Sascar
            api_secret: Secret da API Sascar
            simulation_mode: Se True, retorna dados simulados
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.simulation_mode = simulation_mode
        
        if not simulation_mode and (not api_key or not api_secret):
            logger.warning("Credenciais Sascar não configuradas. Usando modo simulação.")
            self.simulation_mode = True
    
    def obter_posicao_veiculo(self, placa: str) -> Dict:
        """
        Obtém posição atual de um veículo
        
        Args:
            placa: Placa do veículo
            
        Returns:
            Posição atual com lat/lng, velocidade, etc
        """
        if self.simulation_mode:
            return self._simular_posicao_veiculo(placa)
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/veiculos/{placa}/posicao",
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "success": True,
                "placa": placa,
                "posicao": data
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter posição Sascar: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def listar_veiculos(self) -> Dict:
        """
        Lista todos os veículos rastreados
        
        Returns:
            Lista de veículos
        """
        if self.simulation_mode:
            return self._simular_lista_veiculos()
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/veiculos",
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "success": True,
                "veiculos": data.get("veiculos", [])
            }
            
        except Exception as e:
            logger.error(f"Erro ao listar veículos Sascar: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def obter_historico_rota(
        self,
        placa: str,
        data_inicio: datetime,
        data_fim: datetime
    ) -> Dict:
        """
        Obtém histórico de rota de um veículo
        
        Args:
            placa: Placa do veículo
            data_inicio: Data/hora inicial
            data_fim: Data/hora final
            
        Returns:
            Histórico de posições
        """
        if self.simulation_mode:
            return self._simular_historico_rota(placa, data_inicio, data_fim)
        
        try:
            params = {
                "data_inicio": data_inicio.isoformat(),
                "data_fim": data_fim.isoformat()
            }
            
            response = requests.get(
                f"{self.BASE_URL}/veiculos/{placa}/historico",
                headers=self._get_headers(),
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "success": True,
                "placa": placa,
                "periodo": {
                    "inicio": data_inicio.isoformat(),
                    "fim": data_fim.isoformat()
                },
                "posicoes": data.get("posicoes", [])
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter histórico Sascar: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def criar_cerca_eletronica(
        self,
        nome: str,
        coordenadas: List[Dict],
        tipo: str = "entrada_saida"
    ) -> Dict:
        """
        Cria cerca eletrônica (geofence)
        
        Args:
            nome: Nome da cerca
            coordenadas: Lista de {lat, lng}
            tipo: entrada, saida, entrada_saida
            
        Returns:
            ID da cerca criada
        """
        if self.simulation_mode:
            return {
                "success": True,
                "cerca_id": f"sim_fence_{random.randint(1000, 9999)}",
                "message": "Cerca eletrônica criada (simulação)"
            }
        
        try:
            payload = {
                "nome": nome,
                "coordenadas": coordenadas,
                "tipo": tipo
            }
            
            response = requests.post(
                f"{self.BASE_URL}/cercas",
                headers=self._get_headers(),
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "success": True,
                "cerca_id": data.get("id"),
                "message": "Cerca eletrônica criada"
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar cerca Sascar: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def obter_alertas(self, data_inicio: datetime = None) -> Dict:
        """
        Obtém alertas de segurança
        
        Args:
            data_inicio: Data inicial (padrão: últimas 24h)
            
        Returns:
            Lista de alertas
        """
        if self.simulation_mode:
            return self._simular_alertas()
        
        try:
            if not data_inicio:
                data_inicio = datetime.now() - timedelta(days=1)
            
            params = {"data_inicio": data_inicio.isoformat()}
            
            response = requests.get(
                f"{self.BASE_URL}/alertas",
                headers=self._get_headers(),
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "success": True,
                "alertas": data.get("alertas", [])
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter alertas Sascar: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # ===========================================
    # Métodos de Simulação
    # ===========================================
    
    def _simular_posicao_veiculo(self, placa: str) -> Dict:
        """Simula posição de veículo"""
        # Coordenadas de São Paulo (centro)
        lat_base = -23.5505
        lng_base = -46.6333
        
        # Adicionar variação aleatória
        lat = lat_base + random.uniform(-0.1, 0.1)
        lng = lng_base + random.uniform(-0.1, 0.1)
        
        return {
            "success": True,
            "placa": placa,
            "posicao": {
                "latitude": lat,
                "longitude": lng,
                "velocidade_km_h": random.randint(0, 80),
                "ignicao": random.choice([True, False]),
                "data_hora": datetime.now().isoformat(),
                "endereco": f"Rua Simulada, {random.randint(100, 999)} - São Paulo, SP",
                "odometro_km": random.randint(50000, 150000),
                "direcao_graus": random.randint(0, 359)
            },
            "modo": "simulacao"
        }
    
    def _simular_lista_veiculos(self) -> Dict:
        """Simula lista de veículos"""
        veiculos = [
            {
                "placa": "ABC-1234",
                "modelo": "Mercedes-Benz Actros",
                "ano": 2022,
                "status": "em_movimento",
                "ultima_posicao": datetime.now().isoformat()
            },
            {
                "placa": "DEF-5678",
                "modelo": "Volvo FH 540",
                "ano": 2021,
                "status": "parado",
                "ultima_posicao": (datetime.now() - timedelta(minutes=30)).isoformat()
            },
            {
                "placa": "GHI-9012",
                "modelo": "Scania R 450",
                "ano": 2023,
                "status": "em_movimento",
                "ultima_posicao": datetime.now().isoformat()
            }
        ]
        
        return {
            "success": True,
            "veiculos": veiculos,
            "total": len(veiculos),
            "modo": "simulacao"
        }
    
    def _simular_historico_rota(
        self,
        placa: str,
        data_inicio: datetime,
        data_fim: datetime
    ) -> Dict:
        """Simula histórico de rota"""
        posicoes = []
        
        # Gerar 10 posições simuladas
        delta = (data_fim - data_inicio) / 10
        lat_base = -23.5505
        lng_base = -46.6333
        
        for i in range(10):
            timestamp = data_inicio + (delta * i)
            lat = lat_base + (i * 0.01)
            lng = lng_base + (i * 0.01)
            
            posicoes.append({
                "latitude": lat,
                "longitude": lng,
                "velocidade_km_h": random.randint(40, 80),
                "data_hora": timestamp.isoformat(),
                "ignicao": True
            })
        
        return {
            "success": True,
            "placa": placa,
            "periodo": {
                "inicio": data_inicio.isoformat(),
                "fim": data_fim.isoformat()
            },
            "posicoes": posicoes,
            "total_posicoes": len(posicoes),
            "distancia_percorrida_km": round(random.uniform(50, 200), 2),
            "modo": "simulacao"
        }
    
    def _simular_alertas(self) -> Dict:
        """Simula alertas de segurança"""
        tipos_alerta = [
            "excesso_velocidade",
            "parada_nao_autorizada",
            "desvio_rota",
            "cerca_eletronica_violada"
        ]
        
        alertas = []
        for i in range(random.randint(0, 3)):
            alertas.append({
                "id": f"sim_alert_{random.randint(1000, 9999)}",
                "tipo": random.choice(tipos_alerta),
                "placa": f"ABC-{random.randint(1000, 9999)}",
                "data_hora": (datetime.now() - timedelta(hours=random.randint(1, 24))).isoformat(),
                "descricao": "Alerta simulado para testes",
                "severidade": random.choice(["baixa", "media", "alta"])
            })
        
        return {
            "success": True,
            "alertas": alertas,
            "total": len(alertas),
            "modo": "simulacao"
        }
    
    def _get_headers(self) -> Dict:
        """Retorna headers para requisições"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-API-Secret": self.api_secret
        }
