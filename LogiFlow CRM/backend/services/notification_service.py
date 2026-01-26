"""
LogiFlow CRM - Serviço de Notificações
Envia notificações por email e WhatsApp sobre documentos fiscais
"""

import logging
from typing import Dict, Optional
import requests

from models.cte import CTe
from models.mdfe import MDFe
from models.configuracao_fiscal import ConfiguracaoFiscal

logger = logging.getLogger(__name__)


class NotificationService:
    """Serviço para enviar notificações sobre documentos fiscais"""
    
    def __init__(self, email_service_url: str, whatsapp_service_url: str):
        self.email_service_url = email_service_url
        self.whatsapp_service_url = whatsapp_service_url
    
    def notificar_cte_emitido(
        self, 
        cte: CTe, 
        config: ConfiguracaoFiscal,
        destinatario_email: Optional[str] = None,
        destinatario_telefone: Optional[str] = None
    ) -> Dict:
        """Envia notificações sobre CT-e emitido"""
        resultados = {
            "email": {"success": False},
            "whatsapp": {"success": False}
        }
        
        if config.enviar_email_apos_emissao and destinatario_email:
            resultados["email"] = self._enviar_email_cte(cte, config, destinatario_email)
        
        if config.enviar_whatsapp_apos_emissao and destinatario_telefone:
            resultados["whatsapp"] = self._enviar_whatsapp_cte(cte, config, destinatario_telefone)
        
        return resultados
    
    def _enviar_email_cte(self, cte: CTe, config: ConfiguracaoFiscal, destinatario: str) -> Dict:
        """Envia email com CT-e"""
        try:
            mensagem = config.mensagem_email_cte or f"""
            Prezado(a),
            
            Seu CT-e foi emitido com sucesso!
            
            Número: {cte.numero}
            Série: {cte.serie}
            Chave: {cte.chave}
            Valor: R$ {cte.valor_total:.2f}
            
            Anexo: DACTE em PDF
            
            Atenciosamente,
            {config.emitente_razao_social}
            """
            
            payload = {
                "to": destinatario,
                "subject": f"CT-e {cte.numero} - {config.emitente_razao_social}",
                "body": mensagem,
                "attachments": [
                    {
                        "url": cte.url_danfe,
                        "filename": f"DACTE_{cte.numero}.pdf"
                    }
                ]
            }
            
            response = requests.post(
                f"{self.email_service_url}/send",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            logger.info(f"Email CT-e {cte.numero} enviado para {destinatario}")
            return {"success": True}
            
        except Exception as e:
            logger.error(f"Erro ao enviar email CT-e: {e}")
            return {"success": False, "error": str(e)}
    
    def _enviar_whatsapp_cte(self, cte: CTe, config: ConfiguracaoFiscal, telefone: str) -> Dict:
        """Envia WhatsApp com CT-e"""
        try:
            mensagem = config.mensagem_whatsapp_cte or f"""
            🚚 *CT-e Emitido com Sucesso*
            
            Número: *{cte.numero}*
            Série: {cte.serie}
            Chave: {cte.chave}
            Valor: R$ {cte.valor_total:.2f}
            
            Acesse o DACTE: {cte.url_danfe}
            
            {config.emitente_razao_social}
            """
            
            payload = {
                "phone": telefone,
                "message": mensagem
            }
            
            response = requests.post(
                f"{self.whatsapp_service_url}/send",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            logger.info(f"WhatsApp CT-e {cte.numero} enviado para {telefone}")
            return {"success": True}
            
        except Exception as e:
            logger.error(f"Erro ao enviar WhatsApp CT-e: {e}")
            return {"success": False, "error": str(e)}
    
    def notificar_mdfe_emitido(
        self, 
        mdfe: MDFe, 
        config: ConfiguracaoFiscal,
        destinatario_email: Optional[str] = None
    ) -> Dict:
        """Envia notificações sobre MDF-e emitido"""
        if not config.enviar_email_apos_emissao or not destinatario_email:
            return {"success": False, "error": "Notificação não habilitada"}
        
        try:
            mensagem = f"""
            Prezado(a),
            
            Seu MDF-e foi emitido com sucesso!
            
            Número: {mdfe.numero}
            Série: {mdfe.serie}
            Chave: {mdfe.chave}
            CT-es vinculados: {mdfe.quantidade_ctes}
            
            Anexo: DAMDFE em PDF
            
            Atenciosamente,
            {config.emitente_razao_social}
            """
            
            payload = {
                "to": destinatario_email,
                "subject": f"MDF-e {mdfe.numero} - {config.emitente_razao_social}",
                "body": mensagem,
                "attachments": [
                    {
                        "url": mdfe.url_damdfe,
                        "filename": f"DAMDFE_{mdfe.numero}.pdf"
                    }
                ]
            }
            
            response = requests.post(
                f"{self.email_service_url}/send",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            logger.info(f"Email MDF-e {mdfe.numero} enviado para {destinatario_email}")
            return {"success": True}
            
        except Exception as e:
            logger.error(f"Erro ao enviar email MDF-e: {e}")
            return {"success": False, "error": str(e)}
