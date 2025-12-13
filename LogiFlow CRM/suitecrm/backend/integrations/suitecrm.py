"""
LogiFlow CRM - SuiteCRM API Client
===================================
Cliente para integração com SuiteCRM V8 API
"""

import httpx
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from loguru import logger
import json


class SuiteCRMMapper:
    """Mapeador de dados entre LogiFlow e SuiteCRM"""
    
    @staticmethod
    def cotacao_to_suitecrm(dados: Dict) -> Dict:
        """Converte dados de cotação do formato LogiFlow para SuiteCRM"""
        return {
            "name": dados.get("name", f"Cotação - {dados.get('cliente_nome', 'Novo')}"),
            "cliente_id": dados.get("cliente_id"),
            "origem_cidade": dados.get("origem_cidade", dados.get("origem", "").split("/")[0] if "/" in dados.get("origem", "") else dados.get("origem", "")),
            "origem_uf": dados.get("origem_uf", dados.get("origem", "").split("/")[-1] if "/" in dados.get("origem", "") else ""),
            "origem_endereco": dados.get("origem_endereco", ""),
            "origem_cep": dados.get("origem_cep", ""),
            "destino_cidade": dados.get("destino_cidade", dados.get("destino", "").split("/")[0] if "/" in dados.get("destino", "") else dados.get("destino", "")),
            "destino_uf": dados.get("destino_uf", dados.get("destino", "").split("/")[-1] if "/" in dados.get("destino", "") else ""),
            "destino_endereco": dados.get("destino_endereco", ""),
            "destino_cep": dados.get("destino_cep", ""),
            "tipo_carga": dados.get("tipo_carga", "geral"),
            "peso_kg": str(dados.get("peso_kg", 0)),
            "cubagem_m3": str(dados.get("cubagem_m3", 0)) if dados.get("cubagem_m3") else None,
            "quantidade_volumes": str(dados.get("quantidade_volumes", 1)),
            "valor_mercadoria": str(dados.get("valor_mercadoria", 0)) if dados.get("valor_mercadoria") else None,
            "modal": dados.get("modal", "rodoviario"),
            "prazo_estimado": str(dados.get("prazo_estimado", 5)),
            "valor_frete": str(dados.get("valor_proposta", dados.get("valor_frete", 0))),
            "valor_seguro": str(dados.get("valor_seguro", 0)),
            "valor_adicional": str(dados.get("valor_adicional", 0)),
            "validade": dados.get("validade"),
            "status": dados.get("status", "aberta"),
            "observacoes": dados.get("observacoes", ""),
        }
    
    @staticmethod
    def cotacao_from_suitecrm(data: Dict) -> Dict:
        """Converte dados de cotação do formato SuiteCRM para LogiFlow"""
        attrs = data.get("attributes", data)
        return {
            "id": data.get("id", attrs.get("id")),
            "numero": attrs.get("numero_cotacao", ""),
            "name": attrs.get("name", ""),
            "cliente_id": attrs.get("cliente_id", ""),
            "cliente_nome": attrs.get("cliente_name", ""),
            "origem": f"{attrs.get('origem_cidade', '')}/{attrs.get('origem_uf', '')}",
            "origem_cidade": attrs.get("origem_cidade", ""),
            "origem_uf": attrs.get("origem_uf", ""),
            "destino": f"{attrs.get('destino_cidade', '')}/{attrs.get('destino_uf', '')}",
            "destino_cidade": attrs.get("destino_cidade", ""),
            "destino_uf": attrs.get("destino_uf", ""),
            "tipo_carga": attrs.get("tipo_carga", "geral"),
            "peso_kg": float(attrs.get("peso_kg", 0) or 0),
            "cubagem_m3": float(attrs.get("cubagem_m3", 0) or 0) if attrs.get("cubagem_m3") else None,
            "modal": attrs.get("modal", "rodoviario"),
            "prazo_estimado": int(attrs.get("prazo_estimado", 0) or 0),
            "valor_proposta": float(attrs.get("valor_frete", 0) or 0),
            "validade": attrs.get("validade"),
            "status": attrs.get("status", "aberta"),
            "observacoes": attrs.get("observacoes", ""),
            "created_at": attrs.get("date_entered", ""),
            "updated_at": attrs.get("date_modified", ""),
        }
    
    @staticmethod
    def pedido_from_suitecrm(data: Dict) -> Dict:
        """Converte dados de pedido do formato SuiteCRM para LogiFlow"""
        attrs = data.get("attributes", data)
        return {
            "id": data.get("id", attrs.get("id")),
            "numero": attrs.get("numero_pedido", ""),
            "data_pedido": attrs.get("data_pedido"),
            "cliente_id": attrs.get("cliente_id", ""),
            "cliente_nome": attrs.get("cliente_name", ""),
            "cotacao_id": attrs.get("cotacao_id"),
            "origem": f"{attrs.get('origem_cidade', '')}/{attrs.get('origem_uf', '')}",
            "destino": f"{attrs.get('destino_cidade', '')}/{attrs.get('destino_uf', '')}",
            "destinatario_nome": attrs.get("destinatario_nome", ""),
            "tipo_carga": attrs.get("tipo_carga", "geral"),
            "peso_kg": float(attrs.get("peso_kg", 0) or 0),
            "valor_frete": float(attrs.get("valor_frete", 0) or 0),
            "motorista_id": attrs.get("motorista_id"),
            "motorista_nome": attrs.get("motorista_name"),
            "veiculo_id": attrs.get("veiculo_id"),
            "veiculo_nome": attrs.get("veiculo_name"),
            "status": attrs.get("status", "em_planejamento"),
            "sla_status": attrs.get("sla_status", "verde"),
            "previsao_entrega": attrs.get("previsao_entrega"),
            "data_entrega": attrs.get("data_entrega"),
            "cte_numero": attrs.get("cte_numero"),
            "cte_status": attrs.get("cte_status"),
            "created_at": attrs.get("date_entered", ""),
            "updated_at": attrs.get("date_modified", ""),
        }
    
    @staticmethod
    def motorista_from_suitecrm(data: Dict) -> Dict:
        """Converte dados de motorista do formato SuiteCRM para LogiFlow"""
        attrs = data.get("attributes", data)
        return {
            "id": data.get("id", attrs.get("id")),
            "nome": attrs.get("name", ""),
            "cpf": attrs.get("cpf", ""),
            "cnh_numero": attrs.get("cnh_numero", ""),
            "cnh_categoria": attrs.get("cnh_categoria", ""),
            "cnh_validade": attrs.get("cnh_validade"),
            "celular": attrs.get("celular", ""),
            "email": attrs.get("email", ""),
            "status": attrs.get("status", "ativo"),
            "disponibilidade": attrs.get("disponibilidade", "disponivel"),
            "created_at": attrs.get("date_entered", ""),
        }
    
    @staticmethod
    def veiculo_from_suitecrm(data: Dict) -> Dict:
        """Converte dados de veículo do formato SuiteCRM para LogiFlow"""
        attrs = data.get("attributes", data)
        return {
            "id": data.get("id", attrs.get("id")),
            "nome": attrs.get("name", ""),
            "placa": attrs.get("placa", ""),
            "tipo_veiculo": attrs.get("tipo_veiculo", ""),
            "marca": attrs.get("marca", ""),
            "modelo": attrs.get("modelo", ""),
            "capacidade_kg": float(attrs.get("capacidade_kg", 0) or 0),
            "status": attrs.get("status", "disponivel"),
            "status_manutencao": attrs.get("status_manutencao", "ok"),
            "km_atual": int(attrs.get("km_atual", 0) or 0),
            "ultima_manutencao": attrs.get("ultima_manutencao"),
            "created_at": attrs.get("date_entered", ""),
        }


class SuiteCRMClient:
    """Cliente para API V8 do SuiteCRM"""
    
    def __init__(self, base_url: str, client_id: str, client_secret: str):
        self.base_url = base_url.rstrip("/")
        self.api_url = f"{self.base_url}/Api/V8"
        self.client_id = client_id
        self.client_secret = client_secret
        self._token: Optional[str] = None
        self._token_expires: Optional[datetime] = None
    
    async def _get_token(self) -> str:
        """Obtém token OAuth2 (com cache)"""
        # Verificar se token ainda é válido
        if self._token and self._token_expires:
            if datetime.now() < self._token_expires - timedelta(minutes=5):
                return self._token
        
        # Obter novo token
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/access_token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret
                }
            )
            
            if response.status_code != 200:
                logger.error(f"Erro ao obter token SuiteCRM: {response.text}")
                raise Exception("Falha na autenticação com SuiteCRM")
            
            data = response.json()
            self._token = data["access_token"]
            self._token_expires = datetime.now() + timedelta(seconds=data.get("expires_in", 3600))
            
            logger.info("Token SuiteCRM obtido com sucesso")
            return self._token
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict:
        """Executa requisição autenticada para SuiteCRM"""
        token = await self._get_token()
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json"
        }
        
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                params=params,
                timeout=30.0
            )
            
            if response.status_code >= 400:
                logger.error(f"Erro SuiteCRM [{response.status_code}]: {response.text}")
                raise Exception(f"Erro na API SuiteCRM: {response.status_code}")
            
            return response.json() if response.text else {}
    
    # ===========================================
    # Módulos Genéricos
    # ===========================================
    
    async def list_records(
        self,
        module: str,
        page: int = 1,
        page_size: int = 20,
        filters: Optional[Dict] = None,
        fields: Optional[List[str]] = None
    ) -> Dict:
        """Lista registros de um módulo"""
        params = {
            "page[number]": page,
            "page[size]": page_size
        }
        
        if fields:
            params["fields[" + module + "]"] = ",".join(fields)
        
        if filters:
            for key, value in filters.items():
                params[f"filter[{key}]"] = value
        
        return await self._request("GET", f"module/{module}", params=params)
    
    async def get_record(self, module: str, record_id: str) -> Dict:
        """Obtém um registro específico"""
        return await self._request("GET", f"module/{module}/{record_id}")
    
    async def create_record(self, module: str, attributes: Dict) -> Dict:
        """Cria um novo registro"""
        payload = {
            "data": {
                "type": module,
                "attributes": attributes
            }
        }
        return await self._request("POST", f"module/{module}", data=payload)
    
    async def update_record(self, module: str, record_id: str, attributes: Dict) -> Dict:
        """Atualiza um registro existente"""
        payload = {
            "data": {
                "type": module,
                "id": record_id,
                "attributes": attributes
            }
        }
        return await self._request("PATCH", f"module/{module}/{record_id}", data=payload)
    
    async def delete_record(self, module: str, record_id: str) -> Dict:
        """Remove um registro"""
        return await self._request("DELETE", f"module/{module}/{record_id}")
    
    # ===========================================
    # Módulos Específicos LogiFlow
    # ===========================================
    
    async def listar_cotacoes(self, page: int = 1, cliente_id: Optional[str] = None) -> Dict:
        """Lista cotações"""
        filters = {}
        if cliente_id:
            filters["cliente_id"] = cliente_id
        return await self.list_records("Cotacoes", page=page, filters=filters)
    
    async def criar_cotacao(self, dados: Dict) -> Dict:
        """Cria nova cotação"""
        return await self.create_record("Cotacoes", dados)
    
    async def listar_pedidos(self, page: int = 1, status: Optional[str] = None) -> Dict:
        """Lista pedidos de frete"""
        filters = {}
        if status:
            filters["status_operacional"] = status
        return await self.list_records("PedidosFrete", page=page, filters=filters)
    
    async def criar_pedido(self, dados: Dict) -> Dict:
        """Cria novo pedido de frete"""
        return await self.create_record("PedidosFrete", dados)
    
    async def atualizar_status_entrega(self, entrega_id: str, status: str, local: str = None) -> Dict:
        """Atualiza status de uma entrega"""
        attributes = {
            "status": status,
            "data_evento": datetime.now().isoformat()
        }
        if local:
            attributes["local_atual"] = local
        
        return await self.update_record("Entregas", entrega_id, attributes)
    
    async def listar_motoristas_ativos(self) -> Dict:
        """Lista motoristas com status ativo"""
        return await self.list_records(
            "Motoristas",
            filters={"status": "Ativo"},
            fields=["nome", "celular", "categoria_cnh", "vencimento_cnh"]
        )
    
    async def listar_veiculos_disponiveis(self) -> Dict:
        """Lista veículos disponíveis"""
        return await self.list_records(
            "Veiculos",
            filters={"status_manutencao": "Disponível"},
            fields=["placa", "tipo_veiculo", "ultima_manutencao"]
        )
