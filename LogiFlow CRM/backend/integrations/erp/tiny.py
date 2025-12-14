"""
LogiFlow CRM - Integração Tiny ERP
Cliente para integração com API Tiny ERP
"""

import requests
from typing import Dict, List, Optional
import json
import logging

logger = logging.getLogger(__name__)


class TinyClient:
    """
    Cliente para API Tiny ERP
    Documentação: https://tiny.com.br/api-docs
    """
    
    BASE_URL = "https://api.tiny.com.br/api2"
    
    def __init__(self, token: str):
        """
        Inicializa cliente Tiny
        
        Args:
            token: Token de autenticação Tiny
        """
        self.token = token
    
    def _fazer_requisicao(self, endpoint: str, dados: Dict = None, metodo: str = "POST") -> Dict:
        """
        Faz requisição para API Tiny
        
        Args:
            endpoint: Endpoint da API
            dados: Dados a enviar
            metodo: Método HTTP (GET ou POST)
            
        Returns:
            Resposta da API
        """
        try:
            payload = {
                "token": self.token,
                "formato": "JSON"
            }
            
            if dados:
                payload["dados"] = json.dumps(dados) if isinstance(dados, dict) else dados
            
            if metodo == "POST":
                response = requests.post(
                    f"{self.BASE_URL}/{endpoint}",
                    data=payload,
                    timeout=30
                )
            else:
                response = requests.get(
                    f"{self.BASE_URL}/{endpoint}",
                    params=payload,
                    timeout=30
                )
            
            response.raise_for_status()
            result = response.json()
            
            # Verificar status da resposta Tiny
            if result.get("retorno", {}).get("status") == "Erro":
                erros = result.get("retorno", {}).get("erros", [])
                erro_msg = erros[0].get("erro") if erros else "Erro desconhecido"
                logger.error(f"Erro Tiny API: {erro_msg}")
                return {
                    "success": False,
                    "error": erro_msg
                }
            
            return {
                "success": True,
                "data": result.get("retorno", {})
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao comunicar com Tiny: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # ===========================================
    # Contatos (Clientes/Fornecedores)
    # ===========================================
    
    def listar_contatos(self, pagina: int = 1, tipo: str = "C") -> Dict:
        """
        Lista contatos (clientes ou fornecedores)
        
        Args:
            pagina: Número da página
            tipo: C=Cliente, F=Fornecedor
            
        Returns:
            Lista de contatos
        """
        endpoint = "contatos.pesquisa.php"
        dados = {
            "pagina": pagina,
            "tipo": tipo
        }
        
        resultado = self._fazer_requisicao(endpoint, dados, "POST")
        
        if not resultado.get("success"):
            return resultado
        
        contatos = resultado.get("data", {}).get("contatos", [])
        
        return {
            "success": True,
            "contatos": contatos,
            "total": len(contatos)
        }
    
    def obter_contato(self, contato_id: str) -> Dict:
        """
        Obtém dados de um contato específico
        
        Args:
            contato_id: ID do contato no Tiny
            
        Returns:
            Dados do contato
        """
        endpoint = "contato.obter.php"
        dados = {"id": contato_id}
        
        resultado = self._fazer_requisicao(endpoint, dados, "POST")
        
        if not resultado.get("success"):
            return resultado
        
        return {
            "success": True,
            "contato": resultado.get("data", {}).get("contato", {})
        }
    
    def criar_contato(self, dados_contato: Dict) -> Dict:
        """
        Cria novo contato no Tiny
        
        Args:
            dados_contato: Dados do contato
                - nome: Nome/Razão Social
                - tipo_pessoa: F=Física, J=Jurídica
                - cpf_cnpj: CPF ou CNPJ
                - ie: Inscrição Estadual (opcional)
                - endereco, numero, bairro, cidade, uf, cep
                - fone, email
                
        Returns:
            ID do contato criado
        """
        endpoint = "contato.incluir.php"
        
        contato = {
            "contato": {
                "sequencia": 1,
                "codigo": dados_contato.get("codigo", ""),
                "nome": dados_contato["nome"],
                "tipo_pessoa": dados_contato.get("tipo_pessoa", "J"),
                "cpf_cnpj": dados_contato.get("cpf_cnpj", ""),
                "ie": dados_contato.get("ie", ""),
                "endereco": dados_contato.get("endereco", ""),
                "numero": dados_contato.get("numero", ""),
                "complemento": dados_contato.get("complemento", ""),
                "bairro": dados_contato.get("bairro", ""),
                "cep": dados_contato.get("cep", ""),
                "cidade": dados_contato.get("cidade", ""),
                "uf": dados_contato.get("uf", ""),
                "fone": dados_contato.get("fone", ""),
                "email": dados_contato.get("email", "")
            }
        }
        
        resultado = self._fazer_requisicao(endpoint, contato, "POST")
        
        if not resultado.get("success"):
            return resultado
        
        return {
            "success": True,
            "id": resultado.get("data", {}).get("id"),
            "message": "Contato criado com sucesso"
        }
    
    def atualizar_contato(self, contato_id: str, dados_contato: Dict) -> Dict:
        """
        Atualiza contato existente
        
        Args:
            contato_id: ID do contato
            dados_contato: Dados a atualizar
            
        Returns:
            Confirmação de atualização
        """
        endpoint = "contato.alterar.php"
        
        contato = {
            "contato": {
                "id": contato_id,
                **dados_contato
            }
        }
        
        resultado = self._fazer_requisicao(endpoint, contato, "POST")
        
        return resultado
    
    # ===========================================
    # Pedidos de Venda
    # ===========================================
    
    def listar_pedidos(self, pagina: int = 1, data_inicial: str = None, data_final: str = None) -> Dict:
        """
        Lista pedidos de venda
        
        Args:
            pagina: Número da página
            data_inicial: Data inicial (dd/mm/aaaa)
            data_final: Data final (dd/mm/aaaa)
            
        Returns:
            Lista de pedidos
        """
        endpoint = "pedidos.pesquisa.php"
        dados = {"pagina": pagina}
        
        if data_inicial:
            dados["dataInicial"] = data_inicial
        if data_final:
            dados["dataFinal"] = data_final
        
        resultado = self._fazer_requisicao(endpoint, dados, "POST")
        
        if not resultado.get("success"):
            return resultado
        
        pedidos = resultado.get("data", {}).get("pedidos", [])
        
        return {
            "success": True,
            "pedidos": pedidos,
            "total": len(pedidos)
        }
    
    def obter_pedido(self, pedido_id: str) -> Dict:
        """
        Obtém dados de um pedido específico
        
        Args:
            pedido_id: ID do pedido no Tiny
            
        Returns:
            Dados do pedido
        """
        endpoint = "pedido.obter.php"
        dados = {"id": pedido_id}
        
        resultado = self._fazer_requisicao(endpoint, dados, "POST")
        
        if not resultado.get("success"):
            return resultado
        
        return {
            "success": True,
            "pedido": resultado.get("data", {}).get("pedido", {})
        }
    
    def criar_pedido(self, dados_pedido: Dict) -> Dict:
        """
        Cria novo pedido de venda
        
        Args:
            dados_pedido: Dados do pedido
                - cliente: {id, nome, cpf_cnpj}
                - itens: [{descricao, quantidade, valor_unitario}]
                - valor_frete: Valor do frete
                - observacoes: Observações
                
        Returns:
            ID do pedido criado
        """
        endpoint = "pedido.incluir.php"
        
        # Montar estrutura do pedido
        pedido = {
            "pedido": {
                "pedido_pai": {
                    "id_vendedor": dados_pedido.get("id_vendedor", ""),
                    "nome_vendedor": dados_pedido.get("nome_vendedor", ""),
                    "codigo_pedido_integracao": dados_pedido.get("codigo_pedido", ""),
                    "data_pedido": dados_pedido.get("data_pedido", ""),
                    "data_prevista": dados_pedido.get("data_prevista", ""),
                    "nome": dados_pedido["cliente"]["nome"],
                    "cpf_cnpj": dados_pedido["cliente"].get("cpf_cnpj", ""),
                    "endereco": dados_pedido.get("endereco", ""),
                    "numero": dados_pedido.get("numero", ""),
                    "bairro": dados_pedido.get("bairro", ""),
                    "cep": dados_pedido.get("cep", ""),
                    "cidade": dados_pedido.get("cidade", ""),
                    "uf": dados_pedido.get("uf", ""),
                    "fone": dados_pedido.get("fone", ""),
                    "email": dados_pedido.get("email", ""),
                    "valor_frete": dados_pedido.get("valor_frete", 0),
                    "valor_desconto": dados_pedido.get("valor_desconto", 0),
                    "obs": dados_pedido.get("observacoes", ""),
                    "itens": []
                }
            }
        }
        
        # Adicionar itens
        for item in dados_pedido.get("itens", []):
            pedido["pedido"]["pedido_pai"]["itens"].append({
                "item": {
                    "codigo": item.get("codigo", ""),
                    "descricao": item["descricao"],
                    "unidade": item.get("unidade", "UN"),
                    "quantidade": item["quantidade"],
                    "valor_unitario": item["valor_unitario"]
                }
            })
        
        resultado = self._fazer_requisicao(endpoint, pedido, "POST")
        
        if not resultado.get("success"):
            return resultado
        
        return {
            "success": True,
            "id": resultado.get("data", {}).get("id"),
            "numero": resultado.get("data", {}).get("numero"),
            "message": "Pedido criado com sucesso"
        }
    
    # ===========================================
    # Produtos
    # ===========================================
    
    def listar_produtos(self, pagina: int = 1) -> Dict:
        """
        Lista produtos
        
        Args:
            pagina: Número da página
            
        Returns:
            Lista de produtos
        """
        endpoint = "produtos.pesquisa.php"
        dados = {"pagina": pagina}
        
        resultado = self._fazer_requisicao(endpoint, dados, "POST")
        
        if not resultado.get("success"):
            return resultado
        
        produtos = resultado.get("data", {}).get("produtos", [])
        
        return {
            "success": True,
            "produtos": produtos,
            "total": len(produtos)
        }
    
    def criar_produto(self, dados_produto: Dict) -> Dict:
        """
        Cria novo produto/serviço
        
        Args:
            dados_produto: Dados do produto
                - nome: Nome do produto
                - codigo: Código SKU
                - preco: Preço de venda
                - unidade: Unidade (UN, KG, etc)
                - tipo: P=Produto, S=Serviço
                
        Returns:
            ID do produto criado
        """
        endpoint = "produto.incluir.php"
        
        produto = {
            "produto": {
                "sequencia": 1,
                "nome": dados_produto["nome"],
                "codigo": dados_produto.get("codigo", ""),
                "unidade": dados_produto.get("unidade", "UN"),
                "preco": dados_produto.get("preco", 0),
                "tipo": dados_produto.get("tipo", "S"),
                "situacao": dados_produto.get("situacao", "A")
            }
        }
        
        resultado = self._fazer_requisicao(endpoint, produto, "POST")
        
        if not resultado.get("success"):
            return resultado
        
        return {
            "success": True,
            "id": resultado.get("data", {}).get("id"),
            "message": "Produto criado com sucesso"
        }
    
    # ===========================================
    # Helpers - Mapeamento LogiFlow → Tiny
    # ===========================================
    
    def mapear_cliente_logiflow_para_tiny(self, cliente_logiflow: Dict) -> Dict:
        """Mapeia cliente do LogiFlow para formato Tiny"""
        return {
            "nome": cliente_logiflow.get("nome", cliente_logiflow.get("razao_social", "")),
            "tipo_pessoa": "J" if cliente_logiflow.get("cnpj") else "F",
            "cpf_cnpj": cliente_logiflow.get("cnpj") or cliente_logiflow.get("cpf", ""),
            "ie": cliente_logiflow.get("inscricao_estadual", ""),
            "endereco": cliente_logiflow.get("endereco", ""),
            "numero": cliente_logiflow.get("numero", ""),
            "complemento": cliente_logiflow.get("complemento", ""),
            "bairro": cliente_logiflow.get("bairro", ""),
            "cep": cliente_logiflow.get("cep", ""),
            "cidade": cliente_logiflow.get("cidade", ""),
            "uf": cliente_logiflow.get("uf", ""),
            "fone": cliente_logiflow.get("telefone", ""),
            "email": cliente_logiflow.get("email", "")
        }
    
    def mapear_pedido_logiflow_para_tiny(self, pedido_logiflow: Dict) -> Dict:
        """Mapeia pedido do LogiFlow para formato Tiny"""
        return {
            "codigo_pedido": pedido_logiflow.get("numero", ""),
            "data_pedido": pedido_logiflow.get("data_criacao", ""),
            "data_prevista": pedido_logiflow.get("data_entrega_prevista", ""),
            "cliente": {
                "nome": pedido_logiflow.get("cliente_nome", ""),
                "cpf_cnpj": pedido_logiflow.get("cliente_documento", "")
            },
            "endereco": pedido_logiflow.get("destino_endereco", ""),
            "numero": pedido_logiflow.get("destino_numero", ""),
            "bairro": pedido_logiflow.get("destino_bairro", ""),
            "cep": pedido_logiflow.get("destino_cep", ""),
            "cidade": pedido_logiflow.get("destino_cidade", ""),
            "uf": pedido_logiflow.get("destino_uf", ""),
            "valor_frete": pedido_logiflow.get("valor_frete", 0),
            "observacoes": pedido_logiflow.get("observacoes", ""),
            "itens": [
                {
                    "descricao": "Serviço de Transporte",
                    "quantidade": 1,
                    "valor_unitario": pedido_logiflow.get("valor_total", 0)
                }
            ]
        }
    
    # ===========================================
    # Sincronização
    # ===========================================
    
    def sincronizar_cliente(self, cliente_logiflow: Dict) -> Dict:
        """
        Sincroniza cliente do LogiFlow para Tiny
        
        Args:
            cliente_logiflow: Dados do cliente no LogiFlow
            
        Returns:
            Resultado da sincronização
        """
        dados_tiny = self.mapear_cliente_logiflow_para_tiny(cliente_logiflow)
        
        # Verificar se cliente já existe (por CPF/CNPJ)
        # Em produção, implementar busca por documento
        
        return self.criar_contato(dados_tiny)
    
    def sincronizar_pedido(self, pedido_logiflow: Dict) -> Dict:
        """
        Sincroniza pedido do LogiFlow para Tiny
        
        Args:
            pedido_logiflow: Dados do pedido no LogiFlow
            
        Returns:
            Resultado da sincronização
        """
        dados_tiny = self.mapear_pedido_logiflow_para_tiny(pedido_logiflow)
        
        return self.criar_pedido(dados_tiny)
