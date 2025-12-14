"""
LogiFlow CRM - Integração Frenet
Cliente para cotação de frete via API Frenet
"""

import requests
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class FrenetClient:
    """
    Cliente para API Frenet
    Documentação: https://frenet.com.br/documentacao
    """
    
    BASE_URL = "https://api.frenet.com.br"
    
    def __init__(self, token: str):
        """
        Inicializa cliente Frenet
        
        Args:
            token: Token de autenticação Frenet
        """
        self.token = token
        self.headers = {
            "Content-Type": "application/json",
            "token": token
        }
    
    def calcular_frete(self, dados: Dict) -> Dict:
        """
        Calcula frete via Frenet
        
        Args:
            dados: Dados da cotação
                - cep_origem: CEP de origem (8 dígitos)
                - cep_destino: CEP de destino (8 dígitos)
                - peso: Peso em kg
                - comprimento: Comprimento em cm
                - altura: Altura em cm
                - largura: Largura em cm
                - valor_declarado: Valor da mercadoria
                
        Returns:
            Cotações disponíveis
        """
        try:
            payload = {
                "SellerCEP": self._limpar_cep(dados["cep_origem"]),
                "RecipientCEP": self._limpar_cep(dados["cep_destino"]),
                "ShipmentInvoiceValue": dados.get("valor_declarado", 0),
                "ShippingItemArray": [
                    {
                        "Weight": dados["peso"],
                        "Length": dados.get("comprimento", 20),
                        "Height": dados.get("altura", 20),
                        "Width": dados.get("largura", 20),
                        "Quantity": dados.get("quantidade", 1)
                    }
                ]
            }
            
            # Adicionar serviços específicos se fornecidos
            if "servicos" in dados:
                payload["ShippingServiceCode"] = dados["servicos"]
            
            response = requests.post(
                f"{self.BASE_URL}/shipping/quote",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            
            if not result.get("ShippingSevicesArray"):
                return {
                    "success": False,
                    "error": "Nenhuma opção de frete disponível",
                    "message": result.get("Message", "Erro desconhecido")
                }
            
            # Processar cotações
            cotacoes = []
            for servico in result["ShippingSevicesArray"]:
                if servico.get("Error"):
                    logger.warning(f"Erro no serviço {servico.get('ServiceCode')}: {servico.get('ErrorMessage')}")
                    continue
                
                cotacao = {
                    "transportadora": "Frenet",
                    "servico": servico.get("ServiceDescription", "Serviço Padrão"),
                    "codigo_servico": servico.get("ServiceCode"),
                    "valor": float(servico.get("ShippingPrice", 0)),
                    "prazo_dias": int(servico.get("DeliveryTime", 0)),
                    "prazo_descricao": f"{servico.get('DeliveryTime', 0)} dias úteis",
                    "observacoes": servico.get("Msg", ""),
                    "origem": "frenet"
                }
                cotacoes.append(cotacao)
            
            # Ordenar por valor
            cotacoes.sort(key=lambda x: x["valor"])
            
            logger.info(f"Frenet: {len(cotacoes)} cotações obtidas")
            
            return {
                "success": True,
                "total_cotacoes": len(cotacoes),
                "cotacoes": cotacoes,
                "origem_cep": dados["cep_origem"],
                "destino_cep": dados["cep_destino"]
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao consultar Frenet: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Erro ao comunicar com Frenet"
            }
        except Exception as e:
            logger.error(f"Erro inesperado ao calcular frete Frenet: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Erro interno ao processar cotação"
            }
    
    def calcular_frete_simplificado(
        self,
        cep_origem: str,
        cep_destino: str,
        peso: float,
        valor_declarado: float = 0
    ) -> Dict:
        """
        Versão simplificada do cálculo de frete
        Usa dimensões padrão
        
        Args:
            cep_origem: CEP de origem
            cep_destino: CEP de destino
            peso: Peso em kg
            valor_declarado: Valor da mercadoria
            
        Returns:
            Cotações disponíveis
        """
        dados = {
            "cep_origem": cep_origem,
            "cep_destino": cep_destino,
            "peso": peso,
            "valor_declarado": valor_declarado,
            "comprimento": 20,
            "altura": 20,
            "largura": 20,
            "quantidade": 1
        }
        
        return self.calcular_frete(dados)
    
    def rastrear_envio(self, codigo_rastreio: str) -> Dict:
        """
        Rastreia um envio
        
        Args:
            codigo_rastreio: Código de rastreamento
            
        Returns:
            Status do envio
        """
        try:
            response = requests.get(
                f"{self.BASE_URL}/tracking/trackinginfo",
                params={"ShippingNumber": codigo_rastreio},
                headers=self.headers,
                timeout=15
            )
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("Error"):
                return {
                    "success": False,
                    "error": result.get("ErrorMessage", "Erro ao rastrear")
                }
            
            # Processar eventos de rastreamento
            eventos = []
            if result.get("TrackingEvents"):
                for evento in result["TrackingEvents"]:
                    eventos.append({
                        "data": evento.get("EventDate"),
                        "hora": evento.get("EventTime"),
                        "descricao": evento.get("EventDescription"),
                        "local": evento.get("EventLocation")
                    })
            
            return {
                "success": True,
                "codigo_rastreio": codigo_rastreio,
                "status": result.get("Status"),
                "eventos": eventos,
                "ultima_atualizacao": eventos[0] if eventos else None
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao rastrear envio Frenet: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def listar_servicos_disponiveis(self) -> Dict:
        """
        Lista serviços disponíveis na Frenet
        
        Returns:
            Lista de serviços
        """
        # Serviços comuns da Frenet
        servicos = [
            {
                "codigo": "04014",
                "nome": "SEDEX",
                "descricao": "Serviço expresso dos Correios"
            },
            {
                "codigo": "04510",
                "nome": "PAC",
                "descricao": "Encomenda econômica dos Correios"
            },
            {
                "codigo": "04782",
                "nome": "SEDEX 12",
                "descricao": "Entrega no dia seguinte"
            },
            {
                "codigo": "04790",
                "nome": "SEDEX 10",
                "descricao": "Entrega até às 10h do dia seguinte"
            },
            {
                "codigo": "04804",
                "nome": "SEDEX Hoje",
                "descricao": "Entrega no mesmo dia"
            }
        ]
        
        return {
            "success": True,
            "servicos": servicos
        }
    
    def comparar_com_tabela_propria(
        self,
        cotacoes_frenet: List[Dict],
        valor_tabela_propria: float,
        prazo_tabela_propria: int
    ) -> Dict:
        """
        Compara cotações Frenet com tabela própria
        
        Args:
            cotacoes_frenet: Lista de cotações da Frenet
            valor_tabela_propria: Valor da tabela própria
            prazo_tabela_propria: Prazo da tabela própria
            
        Returns:
            Comparação e recomendação
        """
        if not cotacoes_frenet:
            return {
                "recomendacao": "tabela_propria",
                "motivo": "Nenhuma cotação Frenet disponível",
                "economia": 0
            }
        
        # Pegar a melhor opção da Frenet
        melhor_frenet = min(cotacoes_frenet, key=lambda x: x["valor"])
        
        # Comparar valores
        economia = valor_tabela_propria - melhor_frenet["valor"]
        economia_percentual = (economia / valor_tabela_propria) * 100 if valor_tabela_propria > 0 else 0
        
        # Determinar recomendação
        if economia > 0 and economia_percentual >= 10:  # Economia >= 10%
            recomendacao = "frenet"
            motivo = f"Economia de R$ {economia:.2f} ({economia_percentual:.1f}%)"
        elif prazo_tabela_propria < melhor_frenet["prazo_dias"]:
            recomendacao = "tabela_propria"
            motivo = f"Prazo melhor ({prazo_tabela_propria} vs {melhor_frenet['prazo_dias']} dias)"
        elif abs(economia_percentual) < 10:
            recomendacao = "tabela_propria"
            motivo = "Diferença de preço pequena, priorizar frota própria"
        else:
            recomendacao = "frenet"
            motivo = f"Melhor custo-benefício"
        
        return {
            "recomendacao": recomendacao,
            "motivo": motivo,
            "economia": economia,
            "economia_percentual": economia_percentual,
            "melhor_frenet": melhor_frenet,
            "tabela_propria": {
                "valor": valor_tabela_propria,
                "prazo_dias": prazo_tabela_propria
            }
        }
    
    def _limpar_cep(self, cep: str) -> str:
        """Remove formatação do CEP"""
        return cep.replace("-", "").replace(".", "").strip()
    
    def verificar_disponibilidade(self, cep: str) -> Dict:
        """
        Verifica se um CEP tem cobertura Frenet
        
        Args:
            cep: CEP a verificar
            
        Returns:
            Disponibilidade
        """
        try:
            response = requests.get(
                f"{self.BASE_URL}/cep/check",
                params={"CEP": self._limpar_cep(cep)},
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            
            return {
                "success": True,
                "cep": cep,
                "disponivel": result.get("Available", False),
                "cidade": result.get("City"),
                "estado": result.get("State")
            }
            
        except Exception as e:
            logger.error(f"Erro ao verificar disponibilidade CEP: {e}")
            return {
                "success": False,
                "error": str(e)
            }
