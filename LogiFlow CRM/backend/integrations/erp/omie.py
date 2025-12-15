"""
LogiFlow CRM - Integração com Omie ERP
API: https://developer.omie.com.br/
"""

import requests
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class OmieClient:
    """Cliente para integração com Omie ERP"""
    
    BASE_URL = "https://app.omie.com.br/api/v1"
    
    def __init__(self, app_key: str, app_secret: str):
        """
        Inicializa cliente Omie
        
        Args:
            app_key: Chave da aplicação Omie
            app_secret: Secret da aplicação Omie
        """
        self.app_key = app_key
        self.app_secret = app_secret
        self.session = requests.Session()
    
    @classmethod
    def from_tenant_credentials(cls, credentials: Dict):
        """
        Cria cliente a partir das credenciais do tenant
        
        Args:
            credentials: Dict com 'app_key' e 'app_secret'
        """
        app_key = credentials.get("app_key")
        app_secret = credentials.get("app_secret")
        
        if not app_key or not app_secret:
            raise ValueError("app_key e app_secret são obrigatórios para Omie")
        
        return cls(app_key=app_key, app_secret=app_secret)
    
    def listar_categorias(self) -> Dict:
        """
        Lista categorias (endpoint simples para testar conexão)
        """
        return self._make_request(
            endpoint="/geral/categorias/",
            call="ListarCategorias",
            params=[{"pagina": 1, "registros_por_pagina": 10}]
        )
    
    def _make_request(self, endpoint: str, call: str, params: List[Dict]) -> Dict:
        """
        Faz requisição para API Omie
        
        Args:
            endpoint: Endpoint da API (ex: /geral/clientes/)
            call: Nome da chamada (ex: ListarClientes)
            params: Parâmetros da chamada
        
        Returns:
            Resposta da API
        """
        payload = {
            "call": call,
            "app_key": self.app_key,
            "app_secret": self.app_secret,
            "param": params
        }
        
        try:
            response = self.session.post(
                f"{self.BASE_URL}{endpoint}",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição Omie: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Erro ao comunicar com Omie"
            }
    
    # ========================================
    # Clientes
    # ========================================
    
    def listar_clientes(self, pagina: int = 1, registros_por_pagina: int = 50) -> Dict:
        """
        Lista clientes do Omie
        
        Args:
            pagina: Número da página
            registros_por_pagina: Quantidade de registros por página
        
        Returns:
            Lista de clientes
        """
        return self._make_request(
            endpoint="/geral/clientes/",
            call="ListarClientes",
            params=[{
                "pagina": pagina,
                "registros_por_pagina": registros_por_pagina,
                "apenas_importado_api": "N"
            }]
        )
    
    def consultar_cliente(self, codigo_cliente_omie: Optional[int] = None, 
                         cnpj_cpf: Optional[str] = None) -> Dict:
        """
        Consulta cliente específico
        
        Args:
            codigo_cliente_omie: Código interno do cliente no Omie
            cnpj_cpf: CNPJ ou CPF do cliente
        
        Returns:
            Dados do cliente
        """
        param = {}
        if codigo_cliente_omie:
            param["codigo_cliente_omie"] = codigo_cliente_omie
        if cnpj_cpf:
            param["cnpj_cpf"] = cnpj_cpf
        
        return self._make_request(
            endpoint="/geral/clientes/",
            call="ConsultarCliente",
            params=[param]
        )
    
    def incluir_cliente(self, dados_cliente: Dict) -> Dict:
        """
        Inclui novo cliente no Omie
        
        Args:
            dados_cliente: Dados do cliente (nome, cnpj, endereço, etc)
        
        Returns:
            Dados do cliente criado
        """
        return self._make_request(
            endpoint="/geral/clientes/",
            call="IncluirCliente",
            params=[dados_cliente]
        )
    
    def alterar_cliente(self, dados_cliente: Dict) -> Dict:
        """
        Altera cliente existente
        
        Args:
            dados_cliente: Dados do cliente incluindo codigo_cliente_omie
        
        Returns:
            Dados do cliente alterado
        """
        return self._make_request(
            endpoint="/geral/clientes/",
            call="AlterarCliente",
            params=[dados_cliente]
        )
    
    def upsert_cliente(self, dados_cliente: Dict) -> Dict:
        """
        Inclui ou altera cliente (upsert)
        
        Args:
            dados_cliente: Dados do cliente
        
        Returns:
            Dados do cliente criado/alterado
        """
        return self._make_request(
            endpoint="/geral/clientes/",
            call="UpsertCliente",
            params=[dados_cliente]
        )
    
    # ========================================
    # Pedidos de Venda
    # ========================================
    
    def listar_pedidos(self, pagina: int = 1, registros_por_pagina: int = 50,
                      apenas_importado_api: str = "N") -> Dict:
        """
        Lista pedidos de venda
        
        Args:
            pagina: Número da página
            registros_por_pagina: Quantidade de registros
            apenas_importado_api: Filtrar apenas importados via API
        
        Returns:
            Lista de pedidos
        """
        return self._make_request(
            endpoint="/produtos/pedido/",
            call="ListarPedidos",
            params=[{
                "pagina": pagina,
                "registros_por_pagina": registros_por_pagina,
                "apenas_importado_api": apenas_importado_api
            }]
        )
    
    def consultar_pedido(self, codigo_pedido: Optional[int] = None,
                        numero_pedido: Optional[str] = None) -> Dict:
        """
        Consulta pedido específico
        
        Args:
            codigo_pedido: Código interno do pedido no Omie
            numero_pedido: Número do pedido
        
        Returns:
            Dados do pedido
        """
        param = {}
        if codigo_pedido:
            param["codigo_pedido"] = codigo_pedido
        if numero_pedido:
            param["numero_pedido"] = numero_pedido
        
        return self._make_request(
            endpoint="/produtos/pedido/",
            call="ConsultarPedido",
            params=[param]
        )
    
    def incluir_pedido(self, dados_pedido: Dict) -> Dict:
        """
        Inclui novo pedido de venda
        
        Args:
            dados_pedido: Dados do pedido
        
        Returns:
            Dados do pedido criado
        """
        return self._make_request(
            endpoint="/produtos/pedido/",
            call="IncluirPedido",
            params=[dados_pedido]
        )
    
    def alterar_pedido(self, dados_pedido: Dict) -> Dict:
        """
        Altera pedido existente
        
        Args:
            dados_pedido: Dados do pedido incluindo codigo_pedido
        
        Returns:
            Dados do pedido alterado
        """
        return self._make_request(
            endpoint="/produtos/pedido/",
            call="AlterarPedido",
            params=[dados_pedido]
        )
    
    # ========================================
    # Serviços
    # ========================================
    
    def listar_servicos(self, pagina: int = 1, registros_por_pagina: int = 50) -> Dict:
        """
        Lista serviços cadastrados
        
        Args:
            pagina: Número da página
            registros_por_pagina: Quantidade de registros
        
        Returns:
            Lista de serviços
        """
        return self._make_request(
            endpoint="/geral/servicos/",
            call="ListarServicos",
            params=[{
                "pagina": pagina,
                "registros_por_pagina": registros_por_pagina
            }]
        )
    
    def incluir_servico(self, dados_servico: Dict) -> Dict:
        """
        Inclui novo serviço
        
        Args:
            dados_servico: Dados do serviço
        
        Returns:
            Dados do serviço criado
        """
        return self._make_request(
            endpoint="/geral/servicos/",
            call="IncluirServico",
            params=[dados_servico]
        )
    
    # ========================================
    # Ordem de Serviço
    # ========================================
    
    def incluir_ordem_servico(self, dados_os: Dict) -> Dict:
        """
        Inclui ordem de serviço
        
        Args:
            dados_os: Dados da OS
        
        Returns:
            Dados da OS criada
        """
        return self._make_request(
            endpoint="/servicos/os/",
            call="IncluirOS",
            params=[dados_os]
        )
    
    # ========================================
    # Helpers - Mapeamento LogiFlow -> Omie
    # ========================================
    
    def mapear_cliente_logiflow_para_omie(self, cliente_logiflow: Dict) -> Dict:
        """
        Mapeia cliente do LogiFlow para formato Omie
        
        Args:
            cliente_logiflow: Dados do cliente no formato LogiFlow
        
        Returns:
            Dados no formato Omie
        """
        return {
            "codigo_cliente_integracao": cliente_logiflow.get("id"),
            "razao_social": cliente_logiflow.get("nome"),
            "nome_fantasia": cliente_logiflow.get("nome_fantasia", cliente_logiflow.get("nome")),
            "cnpj_cpf": cliente_logiflow.get("cnpj") or cliente_logiflow.get("cpf"),
            "telefone1_numero": cliente_logiflow.get("telefone"),
            "email": cliente_logiflow.get("email"),
            "endereco": cliente_logiflow.get("endereco"),
            "endereco_numero": cliente_logiflow.get("numero"),
            "complemento": cliente_logiflow.get("complemento"),
            "bairro": cliente_logiflow.get("bairro"),
            "cidade": cliente_logiflow.get("cidade"),
            "estado": cliente_logiflow.get("uf"),
            "cep": cliente_logiflow.get("cep"),
            "inscricao_estadual": cliente_logiflow.get("ie"),
            "pessoa_fisica": "S" if cliente_logiflow.get("cpf") else "N"
        }
    
    def mapear_pedido_logiflow_para_omie(self, pedido_logiflow: Dict) -> Dict:
        """
        Mapeia pedido do LogiFlow para formato Omie
        
        Args:
            pedido_logiflow: Dados do pedido no formato LogiFlow
        
        Returns:
            Dados no formato Omie
        """
        return {
            "codigo_pedido_integracao": pedido_logiflow.get("id"),
            "codigo_cliente": pedido_logiflow.get("cliente_id"),
            "data_previsao": pedido_logiflow.get("data_entrega_prevista"),
            "observacoes": pedido_logiflow.get("observacoes"),
            "det": [{
                "ide": {
                    "codigo_item_integracao": item.get("id")
                },
                "produto": {
                    "codigo_produto": item.get("servico_id"),
                    "descricao": item.get("descricao", "Serviço de Frete"),
                    "quantidade": 1,
                    "valor_unitario": item.get("valor_frete", 0)
                }
            } for item in pedido_logiflow.get("itens", [])]
        }
    
    def sincronizar_cliente(self, cliente_logiflow: Dict) -> Dict:
        """
        Sincroniza cliente do LogiFlow com Omie (cria ou atualiza)
        
        Args:
            cliente_logiflow: Dados do cliente no LogiFlow
        
        Returns:
            Resultado da sincronização
        """
        try:
            dados_omie = self.mapear_cliente_logiflow_para_omie(cliente_logiflow)
            result = self.upsert_cliente(dados_omie)
            
            if result.get("success"):
                logger.info(f"Cliente sincronizado com Omie: {cliente_logiflow.get('nome')}")
            else:
                logger.error(f"Erro ao sincronizar cliente: {result.get('error')}")
            
            return result
            
        except Exception as e:
            logger.error(f"Erro ao sincronizar cliente: {e}")
            return {"success": False, "error": str(e)}
    
    def sincronizar_pedido(self, pedido_logiflow: Dict) -> Dict:
        """
        Sincroniza pedido do LogiFlow com Omie
        
        Args:
            pedido_logiflow: Dados do pedido no LogiFlow
        
        Returns:
            Resultado da sincronização
        """
        try:
            dados_omie = self.mapear_pedido_logiflow_para_omie(pedido_logiflow)
            result = self.incluir_pedido(dados_omie)
            
            if result.get("success"):
                logger.info(f"Pedido sincronizado com Omie: {pedido_logiflow.get('numero')}")
            else:
                logger.error(f"Erro ao sincronizar pedido: {result.get('error')}")
            
            return result
            
        except Exception as e:
            logger.error(f"Erro ao sincronizar pedido: {e}")
            return {"success": False, "error": str(e)}
