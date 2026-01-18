"""
LogiFlow CRM - SuiteCRM Integration Service
Integração com SuiteCRM via OAuth2 API V8
"""

import httpx
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from loguru import logger
from config import settings


class SuiteCRMService:
    """Serviço de integração com SuiteCRM via API V8"""
    
    def __init__(self):
        self.base_url = settings.SUITECRM_URL.rstrip('/')
        self.client_id = settings.SUITECRM_CLIENT_ID
        self.client_secret = settings.SUITECRM_CLIENT_SECRET
        self.access_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
        self.api_url = f"{self.base_url}/legacy/Api/V8"
    
    async def _get_access_token(self) -> str:
        """Obtém ou renova o access token OAuth2"""
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at - timedelta(minutes=5):
                return self.access_token
        
        token_url = f"{self.base_url}/legacy/Api/access_token"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code != 200:
                logger.error(f"Erro ao obter token: {response.text}")
                raise Exception(f"Erro OAuth2: {response.status_code}")
            
            data = response.json()
            self.access_token = data["access_token"]
            expires_in = data.get("expires_in", 3600)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
            
            logger.info("Token SuiteCRM renovado com sucesso")
            return self.access_token
    
    async def _request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Faz requisição autenticada para a API V8"""
        token = await self._get_access_token()
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=headers
            )
            
            if response.status_code >= 400:
                logger.error(f"Erro API SuiteCRM: {response.status_code} - {response.text}")
                raise Exception(f"Erro API: {response.status_code}")
            
            return response.json() if response.text else {}
    
    # ========== Módulos CRUD ==========
    
    async def get_module_records(
        self, 
        module: str, 
        page_size: int = 20,
        page_number: int = 1,
        filters: Optional[Dict] = None,
        fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Lista registros de um módulo"""
        params = {
            "page[size]": page_size,
            "page[number]": page_number
        }
        
        # Campos básicos que não requerem relacionamento com Users
        # Isso evita o erro "Module id is empty when trying to get Users"
        if not fields:
            fields = ["id", "name", "date_entered", "date_modified", "deleted"]
        
        if fields:
            params[f"fields[{module}]"] = ",".join(fields)
        
        if filters:
            for key, value in filters.items():
                params[f"filter[{key}]"] = value
        
        return await self._request("GET", f"module/{module}", params=params)
    
    async def get_record(self, module: str, record_id: str) -> Dict[str, Any]:
        """Obtém um registro específico"""
        return await self._request("GET", f"module/{module}/{record_id}")
    
    async def create_module_record(self, module: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo registro em um módulo"""
        payload = {
            "data": {
                "type": module,
                "attributes": data
            }
        }
        return await self._request("POST", f"module", data=payload)
    
    async def create_record(self, module: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo registro"""
        data = {
            "data": {
                "type": module,
                "attributes": attributes
            }
        }
        return await self._request("POST", f"module/{module}", data=data)
    
    async def update_record(
        self, 
        module: str, 
        record_id: str, 
        attributes: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Atualiza um registro existente"""
        data = {
            "data": {
                "type": module,
                "id": record_id,
                "attributes": attributes
            }
        }
        return await self._request("PATCH", f"module/{module}/{record_id}", data=data)
    
    async def delete_record(self, module: str, record_id: str) -> bool:
        """Deleta um registro"""
        await self._request("DELETE", f"module/{module}/{record_id}")
        return True
    
    # ========== Métodos Específicos LogiFlow ==========
    
    async def get_cotacoes(self, status: Optional[str] = None) -> List[Dict]:
        """Lista cotações do módulo Cotacoes"""
        filters = {}
        if status:
            filters["status"] = status
        
        result = await self.get_module_records(
            module="Cotacoes",
            filters=filters,
            fields=["name", "cliente_nome", "valor_total", "status", "date_entered"]
        )
        return result.get("data", [])
    
    async def create_cotacao(self, cotacao_data: Dict) -> Dict:
        """Cria uma nova cotação"""
        return await self.create_record("Cotacoes", cotacao_data)
    
    async def get_pedidos(self, status: Optional[str] = None) -> List[Dict]:
        """Lista pedidos do módulo PedidosFrete"""
        filters = {}
        if status:
            filters["status"] = status
        
        result = await self.get_module_records(
            module="PedidosFrete",
            filters=filters,
            fields=["name", "numero_pedido", "account_name", "status_operacional", "previsao_entrega"]
        )
        return result.get("data", [])
    
    async def create_pedido(self, pedido_data: Dict) -> Dict:
        """Cria um novo pedido de frete"""
        return await self.create_record("PedidosFrete", pedido_data)
    
    async def get_entregas(self, pedido_id: Optional[str] = None) -> List[Dict]:
        """Lista entregas do módulo Entregas"""
        filters = {}
        if pedido_id:
            filters["pedido_id"] = pedido_id
        
        result = await self.get_module_records(
            module="Entregas",
            filters=filters,
            fields=["name", "numero_rastreio", "status", "local_atual", "data_entrega"]
        )
        return result.get("data", [])
    
    async def atualizar_status_entrega(
        self, 
        entrega_id: str, 
        novo_status: str,
        observacao: Optional[str] = None
    ) -> Dict:
        """Atualiza status de uma entrega"""
        attributes = {
            "status": novo_status,
            "data_atualizacao": datetime.now().isoformat()
        }
        if observacao:
            attributes["observacao_status"] = observacao
        
        return await self.update_record("Entregas", entrega_id, attributes)
    
    async def get_motoristas(self, status: Optional[str] = None) -> List[Dict]:
        """Lista motoristas"""
        filters = {}
        if status:
            filters["status"] = status
        
        result = await self.get_module_records(
            module="Motoristas",
            filters=filters,
            fields=["name", "cpf", "celular", "cnh", "categoria_cnh", "status"]
        )
        return result.get("data", [])
    
    async def get_veiculos(self, status: Optional[str] = None) -> List[Dict]:
        """Lista veículos"""
        filters = {}
        if status:
            filters["status"] = status
        
        result = await self.get_module_records(
            module="Veiculos",
            filters=filters,
            fields=["name", "placa", "tipo_veiculo", "capacidade_kg", "status"]
        )
        return result.get("data", [])
    
    async def registrar_ocorrencia(self, ocorrencia_data: Dict) -> Dict:
        """Registra uma nova ocorrência"""
        ocorrencia_data["data_ocorrencia"] = datetime.now().isoformat()
        return await self.create_record("Ocorrencias", ocorrencia_data)
    
    # ========== Relacionamentos ==========
    
    async def get_related_records(
        self, 
        module: str, 
        record_id: str, 
        related_module: str
    ) -> List[Dict]:
        """Obtém registros relacionados"""
        result = await self._request(
            "GET", 
            f"module/{module}/{record_id}/relationships/{related_module}"
        )
        return result.get("data", [])
    
    async def create_relationship(
        self,
        module: str,
        record_id: str,
        related_module: str,
        related_id: str
    ) -> bool:
        """Cria relacionamento entre registros"""
        data = {
            "data": {
                "type": related_module,
                "id": related_id
            }
        }
        await self._request(
            "POST",
            f"module/{module}/{record_id}/relationships/{related_module}",
            data=data
        )
        return True
    
    # ========== Utilitários ==========
    
    async def test_connection(self) -> Dict[str, Any]:
        """Testa conexão com SuiteCRM"""
        try:
            token = await self._get_access_token()
            return {
                "success": True,
                "message": "Conexão estabelecida com sucesso",
                "base_url": self.base_url,
                "token_valid": bool(token)
            }
        except Exception as e:
            logger.error(f"Erro ao testar conexão: {e}")
            return {
                "success": False,
                "message": str(e),
                "base_url": self.base_url
            }
    
    async def sync_from_suitecrm(self, module: str) -> Dict[str, Any]:
        """Sincroniza dados do SuiteCRM para o sistema local"""
        try:
            records = await self.get_module_records(module, page_size=100)
            return {
                "success": True,
                "module": module,
                "records_count": len(records.get("data", [])),
                "synced_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Erro ao sincronizar {module}: {e}")
            return {
                "success": False,
                "module": module,
                "error": str(e)
            }


# Instância global
suitecrm_service = SuiteCRMService()
