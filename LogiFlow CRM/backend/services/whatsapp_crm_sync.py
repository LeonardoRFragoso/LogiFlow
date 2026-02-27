"""
LogiFlow CRM - WhatsApp CRM Sync Service
Sincroniza conversas WhatsApp com CRM Enterprise
"""

from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Optional
import logging
import requests

from models.whatsapp_message import WhatsAppMessage, WhatsAppConversation

logger = logging.getLogger(__name__)


class WhatsAppCRMSync:
    """Serviço para sincronizar WhatsApp com CRM Enterprise"""
    
    def __init__(self, db: Session, tenant_id: str, crm_url: str, crm_token: str):
        self.db = db
        self.tenant_id = tenant_id
        self.crm_url = crm_url
        self.crm_token = crm_token
        self.headers = {
            "Authorization": f"Bearer {crm_token}",
            "Content-Type": "application/json"
        }
    
    def criar_lead_de_conversa(self, conversa: WhatsAppConversation) -> Optional[str]:
        """Cria um lead no CRM a partir de uma conversa WhatsApp"""
        try:
            payload = {
                "nome": conversa.contact_name or f"Cliente WhatsApp {conversa.phone_number}",
                "telefone": conversa.phone_number,
                "origem": "whatsapp",
                "status": "novo",
                "observacoes": f"Lead criado automaticamente via WhatsApp. Última mensagem: {conversa.last_message_content}"
            }
            
            response = requests.post(
                f"{self.crm_url}/api/v1/leads",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            lead_data = response.json()
            lead_id = lead_data.get("id")
            
            # Atualizar conversa com lead_id
            conversa.lead_id = lead_id
            self.db.commit()
            
            logger.info(f"Lead {lead_id} criado para conversa {conversa.id}")
            return lead_id
            
        except Exception as e:
            logger.error(f"Erro ao criar lead de conversa: {e}")
            return None
    
    def criar_caso_de_conversa(
        self, 
        conversa: WhatsAppConversation, 
        categoria: str = "suporte",
        prioridade: str = "media"
    ) -> Optional[str]:
        """Cria um caso de atendimento no CRM"""
        try:
            # Buscar últimas mensagens para contexto
            mensagens = self.db.query(WhatsAppMessage).filter(
                WhatsAppMessage.conversation_id == conversa.id
            ).order_by(WhatsAppMessage.timestamp.desc()).limit(5).all()
            
            historico = "\n".join([
                f"{msg.timestamp.strftime('%d/%m/%Y %H:%M')} - {'Cliente' if msg.direction.value == 'inbound' else 'Atendente'}: {msg.content}"
                for msg in reversed(mensagens)
            ])
            
            payload = {
                "titulo": f"Atendimento WhatsApp - {conversa.contact_name or conversa.phone_number}",
                "descricao": f"Atendimento iniciado via WhatsApp.\n\nHistórico:\n{historico}",
                "categoria": categoria,
                "prioridade": prioridade,
                "origem": "whatsapp",
                "cliente_telefone": conversa.phone_number,
                "cliente_id": conversa.cliente_id,
                "status": "aberto"
            }
            
            response = requests.post(
                f"{self.crm_url}/api/v1/cases",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            case_data = response.json()
            case_id = case_data.get("id")
            
            # Atualizar conversa com case_id
            conversa.case_id = case_id
            self.db.commit()
            
            logger.info(f"Caso {case_id} criado para conversa {conversa.id}")
            return case_id
            
        except Exception as e:
            logger.error(f"Erro ao criar caso de conversa: {e}")
            return None
    
    def vincular_conversa_a_cliente(self, conversa: WhatsAppConversation, cliente_id: str) -> bool:
        """Vincula uma conversa WhatsApp a um cliente existente"""
        try:
            conversa.cliente_id = cliente_id
            self.db.commit()
            
            logger.info(f"Conversa {conversa.id} vinculada ao cliente {cliente_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao vincular conversa a cliente: {e}")
            self.db.rollback()
            return False
    
    def vincular_conversa_a_pedido(self, conversa: WhatsAppConversation, pedido_id: str) -> bool:
        """Vincula uma conversa WhatsApp a um pedido"""
        try:
            conversa.pedido_id = pedido_id
            self.db.commit()
            
            logger.info(f"Conversa {conversa.id} vinculada ao pedido {pedido_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao vincular conversa a pedido: {e}")
            self.db.rollback()
            return False
    
    def sincronizar_mensagens_com_timeline(self, conversa_id: str) -> int:
        """Sincroniza mensagens WhatsApp com timeline do CRM"""
        try:
            conversa = self.db.query(WhatsAppConversation).filter(
                WhatsAppConversation.id == conversa_id
            ).first()
            
            if not conversa or not conversa.cliente_id:
                return 0
            
            # Buscar mensagens não sincronizadas
            mensagens = self.db.query(WhatsAppMessage).filter(
                WhatsAppMessage.conversation_id == conversa_id,
                WhatsAppMessage.extra_metadata.is_(None) | 
                ~WhatsAppMessage.extra_metadata.has_key("synced_to_crm")
            ).order_by(WhatsAppMessage.timestamp.asc()).all()
            
            synced_count = 0
            
            for msg in mensagens:
                try:
                    payload = {
                        "tipo": "whatsapp_message",
                        "descricao": f"{'📥 Recebida' if msg.direction.value == 'inbound' else '📤 Enviada'}: {msg.content}",
                        "data": msg.timestamp.isoformat(),
                        "usuario": "Sistema WhatsApp",
                        "metadata": {
                            "message_id": msg.message_id,
                            "phone_number": msg.from_number if msg.direction.value == "inbound" else msg.to_number,
                            "message_type": msg.message_type.value,
                            "bot_intent": msg.bot_intent
                        }
                    }
                    
                    response = requests.post(
                        f"{self.crm_url}/api/v1/clientes/{conversa.cliente_id}/timeline",
                        json=payload,
                        headers=self.headers,
                        timeout=30
                    )
                    response.raise_for_status()
                    
                    # Marcar como sincronizada
                    if msg.extra_metadata is None:
                        msg.extra_metadata = {}
                    msg.extra_metadata["synced_to_crm"] = True
                    msg.extra_metadata["synced_at"] = datetime.utcnow().isoformat()
                    
                    synced_count += 1
                    
                except Exception as e:
                    logger.error(f"Erro ao sincronizar mensagem {msg.id}: {e}")
                    continue
            
            self.db.commit()
            
            logger.info(f"{synced_count} mensagens sincronizadas com timeline do CRM")
            return synced_count
            
        except Exception as e:
            logger.error(f"Erro ao sincronizar mensagens com timeline: {e}")
            return 0
    
    def buscar_cliente_por_telefone(self, telefone: str) -> Optional[Dict]:
        """Busca cliente no CRM pelo telefone"""
        try:
            response = requests.get(
                f"{self.crm_url}/api/v1/clientes/buscar",
                params={"telefone": telefone},
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            if data.get("success") and data.get("data"):
                return data["data"]
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar cliente por telefone: {e}")
            return None
    
    def atualizar_atividade_cliente(self, cliente_id: str, atividade: str) -> bool:
        """Atualiza última atividade do cliente no CRM"""
        try:
            payload = {
                "ultima_atividade": datetime.utcnow().isoformat(),
                "ultima_interacao": atividade
            }
            
            response = requests.patch(
                f"{self.crm_url}/api/v1/clientes/{cliente_id}",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao atualizar atividade do cliente: {e}")
            return False
    
    def criar_nota_rapida(self, cliente_id: str, nota: str) -> bool:
        """Cria uma nota rápida no CRM"""
        try:
            payload = {
                "tipo": "nota",
                "conteudo": nota,
                "origem": "whatsapp",
                "data": datetime.utcnow().isoformat()
            }
            
            response = requests.post(
                f"{self.crm_url}/api/v1/clientes/{cliente_id}/notas",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar nota rápida: {e}")
            return False


def get_whatsapp_crm_sync(
    db: Session, 
    tenant_id: str, 
    crm_url: str = "http://localhost:8000",
    crm_token: str = ""
) -> WhatsAppCRMSync:
    """Retorna instância do serviço de sincronização"""
    return WhatsAppCRMSync(db, tenant_id, crm_url, crm_token)
