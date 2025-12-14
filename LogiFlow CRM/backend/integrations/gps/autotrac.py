"""
LogiFlow CRM - Integração Autotrac
Cliente para rastreamento GPS via API Autotrac

MODO SIMULAÇÃO: Pronto para uso real quando houver credenciais
"""

import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random
import logging

logger = logging.getLogger(__name__)


class AutotracClient:
    """Cliente para API Autotrac (modo simulação ativo)"""
    
    BASE_URL = "https://api.autotrac.com.br/v2"
    
    def __init__(self, username: str = None, password: str = None, simulation_mode: bool = True):
        self.username = username
        self.password = password
        self.simulation_mode = simulation_mode
        
        if not simulation_mode and (not username or not password):
            logger.warning("Credenciais Autotrac não configuradas. Usando modo simulação.")
            self.simulation_mode = True
    
    def obter_posicao_veiculo(self, placa: str) -> Dict:
        """Obtém posição atual de um veículo"""
        if self.simulation_mode:
            return self._simular_posicao(placa)
        
        # Implementação real quando houver credenciais
        try:
            response = requests.get(
                f"{self.BASE_URL}/veiculos/{placa}/posicao",
                auth=(self.username, self.password),
                timeout=10
            )
            response.raise_for_status()
            return {"success": True, "posicao": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def listar_veiculos(self) -> Dict:
        """Lista todos os veículos"""
        if self.simulation_mode:
            return {
                "success": True,
                "veiculos": [
                    {"placa": "JKL-3456", "modelo": "Iveco Tector", "status": "ativo"},
                    {"placa": "MNO-7890", "modelo": "Ford Cargo", "status": "ativo"}
                ],
                "modo": "simulacao"
            }
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/veiculos",
                auth=(self.username, self.password),
                timeout=10
            )
            response.raise_for_status()
            return {"success": True, "veiculos": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def obter_historico_rota(self, placa: str, data_inicio: datetime, data_fim: datetime) -> Dict:
        """Obtém histórico de rota"""
        if self.simulation_mode:
            posicoes = []
            for i in range(8):
                timestamp = data_inicio + ((data_fim - data_inicio) / 8 * i)
                posicoes.append({
                    "latitude": -23.5505 + (i * 0.015),
                    "longitude": -46.6333 + (i * 0.015),
                    "velocidade": random.randint(50, 90),
                    "timestamp": timestamp.isoformat()
                })
            
            return {
                "success": True,
                "placa": placa,
                "posicoes": posicoes,
                "modo": "simulacao"
            }
        
        try:
            params = {
                "inicio": data_inicio.isoformat(),
                "fim": data_fim.isoformat()
            }
            response = requests.get(
                f"{self.BASE_URL}/veiculos/{placa}/historico",
                auth=(self.username, self.password),
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return {"success": True, "historico": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _simular_posicao(self, placa: str) -> Dict:
        """Simula posição atual"""
        return {
            "success": True,
            "placa": placa,
            "posicao": {
                "latitude": -23.5505 + random.uniform(-0.05, 0.05),
                "longitude": -46.6333 + random.uniform(-0.05, 0.05),
                "velocidade": random.randint(0, 90),
                "timestamp": datetime.now().isoformat(),
                "ignicao": random.choice([True, False])
            },
            "modo": "simulacao"
        }
