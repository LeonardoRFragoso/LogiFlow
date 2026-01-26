"""
LogiFlow CRM - Serviço de Sincronização CRM
Sincroniza CT-es e MDF-es com o CRM Enterprise
"""

import logging
from typing import Dict, Optional
from datetime import datetime
import requests

from models.cte import CTe
from models.mdfe import MDFe

logger = logging.getLogger(__name__)


class CRMSyncService:
    """Serviço para sincronizar documentos fiscais com CRM Enterprise"""
    
    def __init__(self, crm_url: str, crm_token: str):
        self.crm_url = crm_url
        self.crm_token = crm_token
        self.headers = {
            "Authorization": f"Bearer {crm_token}",
            "Content-Type": "application/json"
        }
    
    def sincronizar_cte(self, cte: CTe, pedido_id: Optional[str] = None) -> Dict:
        """Sincroniza CT-e com o CRM Enterprise"""
        try:
            payload = {
                "tipo": "cte",
                "pedido_id": pedido_id or cte.pedido_id,
                "numero": cte.numero,
                "serie": cte.serie,
                "chave": cte.chave,
                "status": cte.status.value,
                "data_emissao": cte.data_emissao.isoformat() if cte.data_emissao else None,
                "valor_total": cte.valor_total,
                "tomador": {
                    "cnpj": cte.tomador_cnpj,
                    "nome": cte.tomador_nome
                },
                "remetente": {
                    "cnpj": cte.remetente_cnpj,
                    "nome": cte.remetente_nome
                },
                "destinatario": {
                    "cnpj": cte.destinatario_cnpj,
                    "nome": cte.destinatario_nome
                },
                "url_danfe": cte.url_danfe,
                "url_xml": cte.url_xml
            }
            
            response = requests.post(
                f"{self.crm_url}/api/v1/documentos-fiscais",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            logger.info(f"CT-e {cte.numero} sincronizado com CRM")
            return {
                "success": True,
                "data": response.json()
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao sincronizar CT-e com CRM: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def sincronizar_mdfe(self, mdfe: MDFe) -> Dict:
        """Sincroniza MDF-e com o CRM Enterprise"""
        try:
            payload = {
                "tipo": "mdfe",
                "numero": mdfe.numero,
                "serie": mdfe.serie,
                "chave": mdfe.chave,
                "status": mdfe.status.value,
                "data_emissao": mdfe.data_emissao.isoformat() if mdfe.data_emissao else None,
                "quantidade_ctes": mdfe.quantidade_ctes,
                "valor_total_carga": mdfe.valor_total_carga,
                "percurso": mdfe.percurso,
                "url_damdfe": mdfe.url_damdfe,
                "url_xml": mdfe.url_xml
            }
            
            response = requests.post(
                f"{self.crm_url}/api/v1/documentos-fiscais",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            logger.info(f"MDF-e {mdfe.numero} sincronizado com CRM")
            return {
                "success": True,
                "data": response.json()
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao sincronizar MDF-e com CRM: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def atualizar_status_pedido(self, pedido_id: str, status: str, cte_info: Dict) -> Dict:
        """Atualiza status do pedido no CRM após emissão de CT-e"""
        try:
            payload = {
                "status": status,
                "cte_numero": cte_info.get("numero"),
                "cte_chave": cte_info.get("chave"),
                "data_emissao_cte": datetime.utcnow().isoformat()
            }
            
            response = requests.patch(
                f"{self.crm_url}/api/v1/pedidos/{pedido_id}",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            logger.info(f"Status do pedido {pedido_id} atualizado no CRM")
            return {
                "success": True,
                "data": response.json()
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao atualizar status do pedido no CRM: {e}")
            return {
                "success": False,
                "error": str(e)
            }
