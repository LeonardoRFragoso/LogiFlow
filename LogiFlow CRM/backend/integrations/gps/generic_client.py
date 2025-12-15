"""
LogiFlow CRM - Cliente GPS Genérico
Cliente configurável que lê config_template.json e adapta-se automaticamente
"""
import json
import requests
from typing import Dict, List, Optional
from pathlib import Path
import logging
import base64

logger = logging.getLogger(__name__)


class GenericGPSClient:
    """
    Cliente GPS genérico que se adapta conforme config_template.json
    
    Quando você conseguir a documentação real:
    1. Edite config_template.json com os detalhes reais
    2. Este cliente se adaptará automaticamente
    3. Não precisa alterar código Python!
    """
    
    def __init__(self, provider: str, credentials: Dict, simulation_mode: bool = False):
        """
        Inicializa cliente GPS genérico
        
        Args:
            provider: Nome do provider (sascar, autotrac, onixsat)
            credentials: Dict com credenciais (formato depende do provider)
            simulation_mode: Se True, não faz chamadas reais
        """
        self.provider = provider
        self.credentials = credentials
        self.simulation_mode = simulation_mode
        
        # Carregar configuração do provider
        self.config = self._load_config(provider)
        
        if not self.config:
            logger.error(f"Configuração não encontrada para provider: {provider}")
            self.simulation_mode = True
        
        # Configurar sessão HTTP
        self.session = requests.Session()
        self._setup_auth()
    
    def _load_config(self, provider: str) -> Optional[Dict]:
        """Carrega configuração do provider do config_template.json"""
        try:
            config_path = Path(__file__).parent / "config_template.json"
            with open(config_path, 'r', encoding='utf-8') as f:
                all_configs = json.load(f)
            return all_configs.get(provider)
        except Exception as e:
            logger.error(f"Erro ao carregar config: {e}")
            return None
    
    def _setup_auth(self):
        """Configura autenticação conforme tipo"""
        if not self.config:
            return
        
        auth_type = self.config.get("auth_type")
        
        if auth_type == "bearer":
            # Bearer Token
            token = self.credentials.get("api_key") or self.credentials.get("token")
            if token:
                header = self.config.get("auth_header", "Authorization")
                prefix = self.config.get("auth_prefix", "Bearer")
                self.session.headers[header] = f"{prefix} {token}"
        
        elif auth_type == "basic":
            # Basic Auth
            username = self.credentials.get("username")
            password = self.credentials.get("password")
            if username and password:
                credentials = f"{username}:{password}"
                encoded = base64.b64encode(credentials.encode()).decode()
                self.session.headers["Authorization"] = f"Basic {encoded}"
        
        elif auth_type == "api_key":
            # Custom API Key header
            api_key = self.credentials.get("api_key")
            header_name = self.config.get("auth_header", "X-API-Key")
            if api_key:
                self.session.headers[header_name] = api_key
        
        # Headers comuns
        self.session.headers["Content-Type"] = "application/json"
        self.session.headers["Accept"] = "application/json"
        self.session.headers["User-Agent"] = "LogiFlow-CRM/1.0"
    
    def _build_url(self, endpoint_name: str, **path_params) -> str:
        """Constrói URL do endpoint"""
        endpoint = self.config["endpoints"].get(endpoint_name)
        if not endpoint:
            raise ValueError(f"Endpoint '{endpoint_name}' não encontrado na configuração")
        
        path = endpoint["path"]
        
        # Substituir parâmetros de path
        for param, value in path_params.items():
            path = path.replace(f"{{{param}}}", str(value))
        
        base_url = self.config["base_url"]
        return f"{base_url}{path}"
    
    def _map_response(self, data: Dict, mapping_key: str) -> Dict:
        """Mapeia resposta conforme response_mapping"""
        mapping = self.config.get("response_mapping", {}).get(mapping_key, {})
        
        if not mapping:
            return data
        
        mapped = {}
        for our_field, their_field in mapping.items():
            # Suporta nested fields com ponto (ex: "location.lat")
            value = data
            for key in their_field.split("."):
                value = value.get(key) if isinstance(value, dict) else None
                if value is None:
                    break
            mapped[our_field] = value
        
        return mapped
    
    def obter_posicao_veiculo(self, placa: str) -> Dict:
        """
        Obtém posição atual de um veículo
        
        Args:
            placa: Placa do veículo
        
        Returns:
            Posição com lat, lng, velocidade, etc
        """
        if self.simulation_mode:
            return self._simulate_position(placa)
        
        try:
            url = self._build_url("get_position", placa=placa)
            
            logger.info(f"[{self.provider}] GET {url}")
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Mapear resposta
            mapped = self._map_response(data, "position")
            
            return {
                "success": True,
                "placa": placa,
                "posicao": mapped,
                "raw_response": data  # Para debug
            }
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"[{self.provider}] HTTP Error {e.response.status_code}: {e}")
            return {
                "success": False,
                "error": f"HTTP {e.response.status_code}",
                "message": str(e),
                "hint": "Verifique se as credenciais estão corretas e se o endpoint está correto no config_template.json"
            }
        
        except Exception as e:
            logger.error(f"[{self.provider}] Erro: {e}")
            return {
                "success": False,
                "error": str(e),
                "hint": "Verifique os logs para mais detalhes"
            }
    
    def listar_veiculos(self) -> Dict:
        """Lista todos os veículos rastreados"""
        if self.simulation_mode:
            return self._simulate_vehicles()
        
        try:
            url = self._build_url("list_vehicles")
            
            logger.info(f"[{self.provider}] GET {url}")
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "success": True,
                "veiculos": data,
                "total": len(data) if isinstance(data, list) else None
            }
        
        except Exception as e:
            logger.error(f"[{self.provider}] Erro ao listar veículos: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def obter_historico_rota(self, placa: str, data_inicio: str, data_fim: str) -> Dict:
        """
        Obtém histórico de rota
        
        Args:
            placa: Placa do veículo
            data_inicio: Data início (ISO format)
            data_fim: Data fim (ISO format)
        """
        if self.simulation_mode:
            return self._simulate_history(placa)
        
        try:
            url = self._build_url("get_history", placa=placa)
            
            # Query params (nomes podem variar por provider)
            endpoint = self.config["endpoints"]["get_history"]
            query_params = endpoint.get("query_params", [])
            
            params = {}
            if len(query_params) >= 2:
                params[query_params[0]] = data_inicio
                params[query_params[1]] = data_fim
            
            logger.info(f"[{self.provider}] GET {url} with params {params}")
            
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "success": True,
                "placa": placa,
                "historico": data
            }
        
        except Exception as e:
            logger.error(f"[{self.provider}] Erro ao obter histórico: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # ========================================
    # Métodos de simulação (fallback)
    # ========================================
    
    def _simulate_position(self, placa: str) -> Dict:
        """Retorna posição simulada"""
        import random
        from datetime import datetime
        
        return {
            "success": True,
            "placa": placa,
            "posicao": {
                "latitude": -23.5505 + random.uniform(-0.1, 0.1),
                "longitude": -46.6333 + random.uniform(-0.1, 0.1),
                "velocidade": random.randint(0, 120),
                "data_hora": datetime.now().isoformat(),
                "ignicao": random.choice([True, False]),
                "odometro": random.randint(10000, 200000)
            },
            "modo": "simulacao",
            "provider": self.provider
        }
    
    def _simulate_vehicles(self) -> Dict:
        """Retorna lista simulada de veículos"""
        return {
            "success": True,
            "veiculos": [
                {"placa": "ABC1234", "modelo": "Mercedes Actros", "status": "ativo"},
                {"placa": "DEF5678", "modelo": "Volvo FH", "status": "ativo"}
            ],
            "modo": "simulacao",
            "provider": self.provider
        }
    
    def _simulate_history(self, placa: str) -> Dict:
        """Retorna histórico simulado"""
        import random
        from datetime import datetime, timedelta
        
        posicoes = []
        now = datetime.now()
        
        for i in range(10):
            timestamp = now - timedelta(hours=10-i)
            posicoes.append({
                "latitude": -23.5505 + (i * 0.01),
                "longitude": -46.6333 + (i * 0.01),
                "velocidade": random.randint(40, 100),
                "data_hora": timestamp.isoformat()
            })
        
        return {
            "success": True,
            "placa": placa,
            "historico": posicoes,
            "modo": "simulacao",
            "provider": self.provider
        }

