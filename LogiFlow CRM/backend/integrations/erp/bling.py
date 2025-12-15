"""
LogiFlow CRM - Integração com Bling ERP
API: https://developer.bling.com.br/
"""

import requests
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BlingClient:
    """Cliente para integração com Bling ERP"""
    
    BASE_URL = "https://api.bling.com.br/Api/v3"
    
    def __init__(self, api_key: str = None, access_token: str = None):
        """
        Inicializa cliente Bling
        
        Args:
            api_key: API Key (versão antiga da API)
            access_token: Token de acesso OAuth2 (versão nova)
        """
        # Suportar ambos os formatos
        token = access_token or api_key
        if not token:
            raise ValueError("api_key ou access_token é obrigatório")
        
        self.access_token = token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    @classmethod
    def from_tenant_credentials(cls, credentials: Dict):
        """
        Cria cliente a partir das credenciais do tenant
        
        Args:
            credentials: Dict com 'api_key' ou 'access_token'
        """
        api_key = credentials.get("api_key")
        access_token = credentials.get("access_token")
        
        if not api_key and not access_token:
            raise ValueError("api_key ou access_token é obrigatório para Bling")
        
        return cls(api_key=api_key, access_token=access_token)
    
    def listar_situacoes(self) -> Dict:
        """
        Lista situações (endpoint simples para testar conexão)
        """
        return self._make_request("GET", "/situacoes")
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None,
                     params: Optional[Dict] = None) -> Dict:
        """
        Faz requisição para API Bling
        
        Args:
            method: Método HTTP (GET, POST, PUT, DELETE)
            endpoint: Endpoint da API
            data: Dados para enviar no body
            params: Parâmetros de query string
        
        Returns:
            Resposta da API
        """
        try:
            response = self.session.request(
                method=method,
                url=f"{self.BASE_URL}{endpoint}",
                json=data,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            return {
                "success": True,
                "data": response.json() if response.content else None
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição Bling: {e}")
            error_message = "Erro ao comunicar com Bling"
            
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_message = error_data.get("error", {}).get("message", error_message)
                except:
                    pass
            
            return {
                "success": False,
                "error": str(e),
                "message": error_message
            }
    
    # ========================================
    # Contatos (Clientes/Fornecedores)
    # ========================================
    
    def listar_contatos(self, pagina: int = 1, limite: int = 100,
                       tipo: Optional[str] = None) -> Dict:
        """
        Lista contatos (clientes/fornecedores)
        
        Args:
            pagina: Número da página
            limite: Quantidade de registros por página
            tipo: Filtro por tipo (Cliente, Fornecedor, Transportador)
        
        Returns:
            Lista de contatos
        """
        params = {
            "pagina": pagina,
            "limite": limite
        }
        if tipo:
            params["tipo"] = tipo
        
        return self._make_request("GET", "/contatos", params=params)
    
    def consultar_contato(self, contato_id: int) -> Dict:
        """
        Consulta contato específico
        
        Args:
            contato_id: ID do contato no Bling
        
        Returns:
            Dados do contato
        """
        return self._make_request("GET", f"/contatos/{contato_id}")
    
    def criar_contato(self, dados_contato: Dict) -> Dict:
        """
        Cria novo contato
        
        Args:
            dados_contato: Dados do contato
        
        Returns:
            Dados do contato criado
        """
        return self._make_request("POST", "/contatos", data=dados_contato)
    
    def atualizar_contato(self, contato_id: int, dados_contato: Dict) -> Dict:
        """
        Atualiza contato existente
        
        Args:
            contato_id: ID do contato
            dados_contato: Dados a atualizar
        
        Returns:
            Dados do contato atualizado
        """
        return self._make_request("PUT", f"/contatos/{contato_id}", data=dados_contato)
    
    # ========================================
    # Pedidos de Venda
    # ========================================
    
    def listar_pedidos(self, pagina: int = 1, limite: int = 100,
                      data_inicial: Optional[str] = None,
                      data_final: Optional[str] = None) -> Dict:
        """
        Lista pedidos de venda
        
        Args:
            pagina: Número da página
            limite: Quantidade de registros
            data_inicial: Data inicial (formato: YYYY-MM-DD)
            data_final: Data final (formato: YYYY-MM-DD)
        
        Returns:
            Lista de pedidos
        """
        params = {
            "pagina": pagina,
            "limite": limite
        }
        if data_inicial:
            params["dataInicial"] = data_inicial
        if data_final:
            params["dataFinal"] = data_final
        
        return self._make_request("GET", "/pedidos/vendas", params=params)
    
    def consultar_pedido(self, pedido_id: int) -> Dict:
        """
        Consulta pedido específico
        
        Args:
            pedido_id: ID do pedido no Bling
        
        Returns:
            Dados do pedido
        """
        return self._make_request("GET", f"/pedidos/vendas/{pedido_id}")
    
    def criar_pedido(self, dados_pedido: Dict) -> Dict:
        """
        Cria novo pedido de venda
        
        Args:
            dados_pedido: Dados do pedido
        
        Returns:
            Dados do pedido criado
        """
        return self._make_request("POST", "/pedidos/vendas", data=dados_pedido)
    
    def atualizar_pedido(self, pedido_id: int, dados_pedido: Dict) -> Dict:
        """
        Atualiza pedido existente
        
        Args:
            pedido_id: ID do pedido
            dados_pedido: Dados a atualizar
        
        Returns:
            Dados do pedido atualizado
        """
        return self._make_request("PUT", f"/pedidos/vendas/{pedido_id}", data=dados_pedido)
    
    def alterar_situacao_pedido(self, pedido_id: int, situacao_id: int) -> Dict:
        """
        Altera situação do pedido
        
        Args:
            pedido_id: ID do pedido
            situacao_id: ID da nova situação
        
        Returns:
            Resultado da operação
        """
        return self._make_request(
            "PATCH",
            f"/pedidos/vendas/{pedido_id}",
            data={"idSituacao": situacao_id}
        )
    
    # ========================================
    # Produtos/Serviços
    # ========================================
    
    def listar_produtos(self, pagina: int = 1, limite: int = 100,
                       tipo: Optional[str] = None) -> Dict:
        """
        Lista produtos/serviços
        
        Args:
            pagina: Número da página
            limite: Quantidade de registros
            tipo: Filtro por tipo (P=Produto, S=Serviço)
        
        Returns:
            Lista de produtos
        """
        params = {
            "pagina": pagina,
            "limite": limite
        }
        if tipo:
            params["tipo"] = tipo
        
        return self._make_request("GET", "/produtos", params=params)
    
    def criar_produto(self, dados_produto: Dict) -> Dict:
        """
        Cria novo produto/serviço
        
        Args:
            dados_produto: Dados do produto
        
        Returns:
            Dados do produto criado
        """
        return self._make_request("POST", "/produtos", data=dados_produto)
    
    # ========================================
    # Notas Fiscais de Serviço
    # ========================================
    
    def listar_nfse(self, pagina: int = 1, limite: int = 100) -> Dict:
        """
        Lista notas fiscais de serviço
        
        Args:
            pagina: Número da página
            limite: Quantidade de registros
        
        Returns:
            Lista de NFS-e
        """
        params = {
            "pagina": pagina,
            "limite": limite
        }
        return self._make_request("GET", "/nfse", params=params)
    
    def criar_nfse(self, dados_nfse: Dict) -> Dict:
        """
        Cria nota fiscal de serviço
        
        Args:
            dados_nfse: Dados da NFS-e
        
        Returns:
            Dados da NFS-e criada
        """
        return self._make_request("POST", "/nfse", data=dados_nfse)
    
    # ========================================
    # Helpers - Mapeamento LogiFlow -> Bling
    # ========================================
    
    def mapear_cliente_logiflow_para_bling(self, cliente_logiflow: Dict) -> Dict:
        """
        Mapeia cliente do LogiFlow para formato Bling
        
        Args:
            cliente_logiflow: Dados do cliente no formato LogiFlow
        
        Returns:
            Dados no formato Bling
        """
        cpf_cnpj = cliente_logiflow.get("cnpj") or cliente_logiflow.get("cpf")
        tipo_pessoa = "J" if cliente_logiflow.get("cnpj") else "F"
        
        contato = {
            "nome": cliente_logiflow.get("nome"),
            "codigo": cliente_logiflow.get("id"),
            "tipo": "Cliente",
            "numeroDocumento": cpf_cnpj,
            "tipoPessoa": tipo_pessoa,
            "ie": {
                "inscricaoEstadual": cliente_logiflow.get("ie")
            } if cliente_logiflow.get("ie") else None,
            "telefone": cliente_logiflow.get("telefone"),
            "celular": cliente_logiflow.get("celular"),
            "email": cliente_logiflow.get("email"),
            "endereco": {
                "endereco": cliente_logiflow.get("endereco"),
                "numero": cliente_logiflow.get("numero"),
                "complemento": cliente_logiflow.get("complemento"),
                "bairro": cliente_logiflow.get("bairro"),
                "cep": cliente_logiflow.get("cep"),
                "municipio": cliente_logiflow.get("cidade"),
                "uf": cliente_logiflow.get("uf")
            }
        }
        
        # Remover campos None
        return {k: v for k, v in contato.items() if v is not None}
    
    def mapear_pedido_logiflow_para_bling(self, pedido_logiflow: Dict) -> Dict:
        """
        Mapeia pedido do LogiFlow para formato Bling
        
        Args:
            pedido_logiflow: Dados do pedido no formato LogiFlow
        
        Returns:
            Dados no formato Bling
        """
        pedido = {
            "numero": pedido_logiflow.get("numero"),
            "data": datetime.now().strftime("%Y-%m-%d"),
            "contato": {
                "id": pedido_logiflow.get("cliente_id")
            },
            "itens": [{
                "codigo": item.get("id"),
                "descricao": item.get("descricao", "Serviço de Frete"),
                "unidade": "UN",
                "quantidade": 1,
                "valor": item.get("valor_frete", 0)
            } for item in pedido_logiflow.get("itens", [])],
            "transporte": {
                "frete": pedido_logiflow.get("tipo_frete", "CIF").upper(),
                "transportadora": {
                    "nome": "Transportadora Própria"
                }
            },
            "observacoes": pedido_logiflow.get("observacoes"),
            "observacoesInternas": f"Pedido importado do LogiFlow CRM - ID: {pedido_logiflow.get('id')}"
        }
        
        return pedido
    
    def sincronizar_cliente(self, cliente_logiflow: Dict) -> Dict:
        """
        Sincroniza cliente do LogiFlow com Bling
        
        Args:
            cliente_logiflow: Dados do cliente no LogiFlow
        
        Returns:
            Resultado da sincronização
        """
        try:
            dados_bling = self.mapear_cliente_logiflow_para_bling(cliente_logiflow)
            
            # Tentar buscar cliente existente pelo CPF/CNPJ
            cpf_cnpj = cliente_logiflow.get("cnpj") or cliente_logiflow.get("cpf")
            if cpf_cnpj:
                # Buscar na lista (Bling não tem busca direta por CPF/CNPJ)
                result_lista = self.listar_contatos(limite=1)
                # Por simplicidade, sempre criar novo. Em produção, implementar busca
            
            result = self.criar_contato(dados_bling)
            
            if result.get("success"):
                logger.info(f"Cliente sincronizado com Bling: {cliente_logiflow.get('nome')}")
            else:
                logger.error(f"Erro ao sincronizar cliente: {result.get('error')}")
            
            return result
            
        except Exception as e:
            logger.error(f"Erro ao sincronizar cliente: {e}")
            return {"success": False, "error": str(e)}
    
    def sincronizar_pedido(self, pedido_logiflow: Dict) -> Dict:
        """
        Sincroniza pedido do LogiFlow com Bling
        
        Args:
            pedido_logiflow: Dados do pedido no LogiFlow
        
        Returns:
            Resultado da sincronização
        """
        try:
            dados_bling = self.mapear_pedido_logiflow_para_bling(pedido_logiflow)
            result = self.criar_pedido(dados_bling)
            
            if result.get("success"):
                logger.info(f"Pedido sincronizado com Bling: {pedido_logiflow.get('numero')}")
            else:
                logger.error(f"Erro ao sincronizar pedido: {result.get('error')}")
            
            return result
            
        except Exception as e:
            logger.error(f"Erro ao sincronizar pedido: {e}")
            return {"success": False, "error": str(e)}
