"""
LogiFlow CRM - Integração com Melhor Envio
API: https://docs.melhorenvio.com.br/
"""

import requests
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MelhorEnvioClient:
    """Cliente para integração com Melhor Envio"""
    
    BASE_URL = "https://api.melhorenvio.com.br/v2/me"
    SANDBOX_URL = "https://sandbox.melhorenvio.com.br/api/v2/me"
    
    def __init__(self, token: str, sandbox: bool = False):
        """
        Inicializa cliente Melhor Envio
        
        Args:
            token: Token de acesso da API
            sandbox: Se True, usa ambiente de testes
        """
        self.token = token
        self.base_url = self.SANDBOX_URL if sandbox else self.BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "LogiFlow CRM (contato@logiflow.com.br)"
        })
    
    @classmethod
    def from_tenant_credentials(cls, credentials: Dict):
        """
        Cria cliente a partir das credenciais do tenant
        
        Args:
            credentials: Dict com 'token' e 'sandbox' (opcional)
        """
        token = credentials.get("token")
        if not token:
            raise ValueError("Token do Melhor Envio não encontrado nas credenciais do tenant")
        
        sandbox = credentials.get("sandbox", False)
        return cls(token=token, sandbox=sandbox)
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None,
                     params: Optional[Dict] = None) -> Dict:
        """
        Faz requisição para API Melhor Envio
        
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
                url=f"{self.base_url}{endpoint}",
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
            logger.error(f"Erro na requisição Melhor Envio: {e}")
            error_message = "Erro ao comunicar com Melhor Envio"
            
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_message = error_data.get("message", error_message)
                except:
                    pass
            
            return {
                "success": False,
                "error": str(e),
                "message": error_message
            }
    
    # ========================================
    # Cotação de Frete
    # ========================================
    
    def calcular_frete(self, origem_cep: str, destino_cep: str,
                      peso: float, altura: float, largura: float, 
                      comprimento: float, valor_declarado: Optional[float] = None,
                      servicos: Optional[List[int]] = None) -> Dict:
        """
        Calcula frete para múltiplas transportadoras
        
        Args:
            origem_cep: CEP de origem (apenas números)
            destino_cep: CEP de destino (apenas números)
            peso: Peso em kg
            altura: Altura em cm
            largura: Largura em cm
            comprimento: Comprimento em cm
            valor_declarado: Valor da mercadoria para seguro
            servicos: Lista de IDs de serviços (opcional, calcula todos se None)
        
        Returns:
            Lista de cotações por transportadora
        """
        # Serviços disponíveis:
        # 1 = Correios PAC
        # 2 = Correios SEDEX
        # 3 = Jadlog
        # 4 = Azul Cargo
        # 17 = JadLog Econômico
        
        payload = {
            "from": {
                "postal_code": origem_cep.replace("-", "").replace(".", "")
            },
            "to": {
                "postal_code": destino_cep.replace("-", "").replace(".", "")
            },
            "package": {
                "weight": peso,
                "height": altura,
                "width": largura,
                "length": comprimento
            }
        }
        
        if valor_declarado:
            payload["options"] = {
                "insurance_value": valor_declarado,
                "receipt": False,
                "own_hand": False
            }
        
        if servicos:
            payload["services"] = ",".join(map(str, servicos))
        
        return self._make_request("POST", "/shipment/calculate", data=payload)
    
    def calcular_frete_simples(self, origem_cep: str, destino_cep: str,
                               peso_kg: float, valor_mercadoria: Optional[float] = None) -> Dict:
        """
        Calcula frete de forma simplificada (dimensões padrão)
        
        Args:
            origem_cep: CEP de origem
            destino_cep: CEP de destino
            peso_kg: Peso em kg
            valor_mercadoria: Valor da mercadoria
        
        Returns:
            Lista de cotações
        """
        # Dimensões padrão para carga fracionada
        altura = 20  # cm
        largura = 30  # cm
        comprimento = 40  # cm
        
        # Ajustar dimensões proporcionalmente ao peso
        if peso_kg > 30:
            fator = (peso_kg / 30) ** (1/3)
            altura = int(altura * fator)
            largura = int(largura * fator)
            comprimento = int(comprimento * fator)
        
        return self.calcular_frete(
            origem_cep=origem_cep,
            destino_cep=destino_cep,
            peso=peso_kg,
            altura=altura,
            largura=largura,
            comprimento=comprimento,
            valor_declarado=valor_mercadoria
        )
    
    # Alias para compatibilidade
    calcular_frete_simplificado = calcular_frete_simples
    
    # ========================================
    # Rastreamento
    # ========================================
    
    def rastrear_envio(self, tracking_code: str) -> Dict:
        """
        Rastreia envio pelo código de rastreamento
        
        Args:
            tracking_code: Código de rastreamento
        
        Returns:
            Informações de rastreamento
        """
        return self._make_request("GET", f"/shipment/tracking/{tracking_code}")
    
    # ========================================
    # Agências
    # ========================================
    
    def buscar_agencias(self, cep: str, transportadora_id: Optional[int] = None) -> Dict:
        """
        Busca agências próximas a um CEP
        
        Args:
            cep: CEP para busca
            transportadora_id: ID da transportadora (opcional)
        
        Returns:
            Lista de agências
        """
        params = {"postal_code": cep.replace("-", "").replace(".", "")}
        if transportadora_id:
            params["company"] = transportadora_id
        
        return self._make_request("GET", "/agencies", params=params)
    
    # ========================================
    # Helpers
    # ========================================
    
    def formatar_cotacao_para_logiflow(self, cotacao_melhor_envio: Dict) -> Dict:
        """
        Formata resposta do Melhor Envio para formato LogiFlow
        
        Args:
            cotacao_melhor_envio: Resposta da API Melhor Envio
        
        Returns:
            Cotação formatada
        """
        if not cotacao_melhor_envio.get("success"):
            return cotacao_melhor_envio
        
        cotacoes = cotacao_melhor_envio.get("data", [])
        
        cotacoes_formatadas = []
        for cot in cotacoes:
            cotacoes_formatadas.append({
                "transportadora": cot.get("company", {}).get("name"),
                "servico": cot.get("name"),
                "valor": cot.get("price"),
                "prazo_dias": cot.get("delivery_time"),
                "prazo_range": cot.get("delivery_range", {}),
                "error": cot.get("error"),
                "disponivel": cot.get("error") is None,
                "detalhes": {
                    "company_id": cot.get("company", {}).get("id"),
                    "service_id": cot.get("id"),
                    "discount": cot.get("discount"),
                    "currency": cot.get("currency"),
                    "packages": cot.get("packages")
                }
            })
        
        return {
            "success": True,
            "data": cotacoes_formatadas,
            "total_opcoes": len(cotacoes_formatadas),
            "opcoes_disponiveis": len([c for c in cotacoes_formatadas if c["disponivel"]])
        }
    
    def obter_melhor_cotacao(self, origem_cep: str, destino_cep: str,
                            peso_kg: float, valor_mercadoria: Optional[float] = None,
                            prioridade: str = "preco") -> Dict:
        """
        Obtém a melhor cotação baseada em critério
        
        Args:
            origem_cep: CEP de origem
            destino_cep: CEP de destino
            peso_kg: Peso em kg
            valor_mercadoria: Valor da mercadoria
            prioridade: 'preco' ou 'prazo'
        
        Returns:
            Melhor cotação encontrada
        """
        result = self.calcular_frete_simples(
            origem_cep=origem_cep,
            destino_cep=destino_cep,
            peso_kg=peso_kg,
            valor_mercadoria=valor_mercadoria
        )
        
        if not result.get("success"):
            return result
        
        cotacoes = result.get("data", [])
        
        # Filtrar apenas cotações disponíveis (sem erro)
        cotacoes_disponiveis = [c for c in cotacoes if c.get("error") is None]
        
        if not cotacoes_disponiveis:
            return {
                "success": False,
                "message": "Nenhuma cotação disponível para esta rota"
            }
        
        # Ordenar por critério
        if prioridade == "prazo":
            melhor = min(cotacoes_disponiveis, key=lambda x: x.get("delivery_time", 999))
        else:  # preco
            melhor = min(cotacoes_disponiveis, key=lambda x: float(x.get("price", 999999)))
        
        return {
            "success": True,
            "data": melhor,
            "criterio": prioridade,
            "total_opcoes": len(cotacoes_disponiveis)
        }
    
    def comparar_com_tabela_propria(self, origem_cep: str, destino_cep: str,
                                   peso_kg: float, valor_tabela_propria: float,
                                   valor_mercadoria: Optional[float] = None) -> Dict:
        """
        Compara cotações do Melhor Envio com tabela própria
        
        Args:
            origem_cep: CEP de origem
            destino_cep: CEP de destino
            peso_kg: Peso em kg
            valor_tabela_propria: Valor da tabela própria da transportadora
            valor_mercadoria: Valor da mercadoria
        
        Returns:
            Comparação de preços
        """
        result = self.calcular_frete_simples(
            origem_cep=origem_cep,
            destino_cep=destino_cep,
            peso_kg=peso_kg,
            valor_mercadoria=valor_mercadoria
        )
        
        if not result.get("success"):
            return result
        
        cotacoes = [c for c in result.get("data", []) if c.get("error") is None]
        
        if cotacoes:
            menor_preco_mercado = min(float(c.get("price", 999999)) for c in cotacoes)
            economia_potencial = valor_tabela_propria - menor_preco_mercado
            percentual_economia = (economia_potencial / valor_tabela_propria * 100) if valor_tabela_propria > 0 else 0
        else:
            menor_preco_mercado = None
            economia_potencial = 0
            percentual_economia = 0
        
        return {
            "success": True,
            "data": {
                "valor_tabela_propria": valor_tabela_propria,
                "menor_preco_mercado": menor_preco_mercado,
                "economia_potencial": economia_potencial,
                "percentual_economia": round(percentual_economia, 2),
                "recomendacao": "terceirizar" if economia_potencial > 0 else "frota_propria",
                "cotacoes_disponiveis": cotacoes
            }
        }
