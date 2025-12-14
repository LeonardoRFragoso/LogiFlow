"""
LogiFlow CRM - Integração Onixsat
Cliente para rastreamento GPS via API Onixsat

MODO SIMULAÇÃO: Pronto para uso real quando houver credenciais
"""

import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random
import logging

logger = logging.getLogger(__name__)


class OnixsatClient:
    """Cliente para API Onixsat (modo simulação ativo)"""
    
    BASE_URL = "https://api.onixsat.com.br/v1"
    
    def __init__(self, api_token: str = None, simulation_mode: bool = True):
        self.api_token = api_token
        self.simulation_mode = simulation_mode
        
        if not simulation_mode and not api_token:
            logger.warning("Token Onixsat não configurado. Usando modo simulação.")
            self.simulation_mode = True
    
    def obter_posicao_veiculo(self, placa: str) -> Dict:
        """Obtém posição atual de um veículo"""
        if self.simulation_mode:
            return self._simular_posicao(placa)
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/posicao/{placa}",
                headers={"Authorization": f"Bearer {self.api_token}"},
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
                    {"placa": "PQR-1122", "modelo": "DAF XF", "status": "rastreando"},
                    {"placa": "STU-3344", "modelo": "MAN TGX", "status": "rastreando"}
                ],
                "modo": "simulacao"
            }
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/veiculos",
                headers={"Authorization": f"Bearer {self.api_token}"},
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
            for i in range(12):
                timestamp = data_inicio + ((data_fim - data_inicio) / 12 * i)
                posicoes.append({
                    "lat": -23.5505 + (i * 0.01),
                    "lng": -46.6333 + (i * 0.01),
                    "speed": random.randint(40, 85),
                    "time": timestamp.isoformat()
                })
            
            return {
                "success": True,
                "placa": placa,
                "posicoes": posicoes,
                "modo": "simulacao"
            }
        
        try:
            params = {
                "start": data_inicio.isoformat(),
                "end": data_fim.isoformat()
            }
            response = requests.get(
                f"{self.BASE_URL}/historico/{placa}",
                headers={"Authorization": f"Bearer {self.api_token}"},
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
                "lat": -23.5505 + random.uniform(-0.08, 0.08),
                "lng": -46.6333 + random.uniform(-0.08, 0.08),
                "speed": random.randint(0, 95),
                "time": datetime.now().isoformat(),
                "engine_on": random.choice([True, False])
            },
            "modo": "simulacao"
        }
