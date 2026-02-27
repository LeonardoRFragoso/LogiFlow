"""
LogiFlow CRM - Model WhatsApp Message
Armazena histórico completo de mensagens WhatsApp
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Enum as SQLEnum, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base


class MessageDirection(str, enum.Enum):
    """Direção da mensagem"""
    INBOUND = "inbound"   # Recebida
    OUTBOUND = "outbound"  # Enviada


class MessageType(str, enum.Enum):
    """Tipo de mensagem"""
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    LOCATION = "location"
    CONTACT = "contact"
    STICKER = "sticker"


class MessageStatus(str, enum.Enum):
    """Status da mensagem"""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"


class WhatsAppMessage(Base):
    """Model para mensagens WhatsApp"""
    
    __tablename__ = "whatsapp_messages"
    
    id = Column(String(36), primary_key=True)
    tenant_id = Column(String(100), nullable=False, index=True)
    
    # Identificação da mensagem
    message_id = Column(String(255), unique=True, index=True)  # ID da Evolution API
    conversation_id = Column(String(36), index=True)  # Agrupa mensagens da mesma conversa
    
    # Direção e tipo
    direction = Column(SQLEnum(MessageDirection), nullable=False, index=True)
    message_type = Column(SQLEnum(MessageType), default=MessageType.TEXT)
    status = Column(SQLEnum(MessageStatus), default=MessageStatus.PENDING, index=True)
    
    # Participantes
    from_number = Column(String(20), nullable=False, index=True)  # Remetente
    to_number = Column(String(20), nullable=False)  # Destinatário
    contact_name = Column(String(255), nullable=True)  # Nome do contato
    
    # Conteúdo
    content = Column(Text, nullable=True)  # Texto da mensagem
    media_url = Column(String(500), nullable=True)  # URL da mídia
    caption = Column(Text, nullable=True)  # Legenda da mídia
    
    # Metadados
    quoted_message_id = Column(String(255), nullable=True)  # Resposta a outra mensagem
    extra_metadata = Column(JSON, nullable=True)  # Dados adicionais
    
    # Relacionamentos com CRM
    cliente_id = Column(String(36), nullable=True, index=True)
    pedido_id = Column(String(36), nullable=True, index=True)
    lead_id = Column(String(36), nullable=True, index=True)
    case_id = Column(String(36), nullable=True, index=True)
    
    # Chatbot
    is_bot_message = Column(Boolean, default=False)  # Enviada pelo bot
    bot_intent = Column(String(100), nullable=True)  # Intenção identificada
    bot_confidence = Column(Integer, nullable=True)  # Confiança (0-100)
    bot_response = Column(Text, nullable=True)  # Resposta do bot
    
    # Timestamps
    timestamp = Column(DateTime, nullable=False, index=True)  # Quando a mensagem foi enviada/recebida
    delivered_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)
    
    # Auditoria
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<WhatsAppMessage(from={self.from_number}, type={self.message_type}, direction={self.direction})>"
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            "id": self.id,
            "message_id": self.message_id,
            "conversation_id": self.conversation_id,
            "direction": self.direction.value if self.direction else None,
            "message_type": self.message_type.value if self.message_type else None,
            "status": self.status.value if self.status else None,
            "from_number": self.from_number,
            "to_number": self.to_number,
            "contact_name": self.contact_name,
            "content": self.content,
            "media_url": self.media_url,
            "caption": self.caption,
            "quoted_message_id": self.quoted_message_id,
            "cliente_id": self.cliente_id,
            "pedido_id": self.pedido_id,
            "lead_id": self.lead_id,
            "case_id": self.case_id,
            "is_bot_message": self.is_bot_message,
            "bot_intent": self.bot_intent,
            "bot_confidence": self.bot_confidence,
            "bot_response": self.bot_response,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "delivered_at": self.delivered_at.isoformat() if self.delivered_at else None,
            "read_at": self.read_at.isoformat() if self.read_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class WhatsAppConversation(Base):
    """Model para conversas WhatsApp"""
    
    __tablename__ = "whatsapp_conversations"
    
    id = Column(String(36), primary_key=True)
    tenant_id = Column(String(100), nullable=False, index=True)
    
    # Identificação
    phone_number = Column(String(20), nullable=False, index=True)
    contact_name = Column(String(255), nullable=True)
    
    # Relacionamentos
    cliente_id = Column(String(36), nullable=True, index=True)
    lead_id = Column(String(36), nullable=True, index=True)
    
    # Estatísticas
    total_messages = Column(Integer, default=0)
    unread_count = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_archived = Column(Boolean, default=False)
    
    # Última mensagem
    last_message_content = Column(Text, nullable=True)
    last_message_at = Column(DateTime, nullable=True, index=True)
    last_message_direction = Column(SQLEnum(MessageDirection), nullable=True)
    
    # Tags e categorias
    tags = Column(JSON, nullable=True)
    category = Column(String(50), nullable=True)  # suporte, vendas, financeiro, etc.
    
    # Atendimento
    assigned_to = Column(String(100), nullable=True)  # Usuário responsável
    assigned_at = Column(DateTime, nullable=True)
    
    # Auditoria
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<WhatsAppConversation(phone={self.phone_number}, messages={self.total_messages})>"
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "phone_number": self.phone_number,
            "contact_name": self.contact_name,
            "cliente_id": self.cliente_id,
            "lead_id": self.lead_id,
            "total_messages": self.total_messages,
            "unread_count": self.unread_count,
            "is_active": self.is_active,
            "is_archived": self.is_archived,
            "last_message_content": self.last_message_content,
            "last_message_at": self.last_message_at.isoformat() if self.last_message_at else None,
            "last_message_direction": self.last_message_direction.value if self.last_message_direction else None,
            "tags": self.tags,
            "category": self.category,
            "assigned_to": self.assigned_to,
            "assigned_at": self.assigned_at.isoformat() if self.assigned_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class WhatsAppConfig(Base):
    """Configurações do WhatsApp por tenant"""
    
    __tablename__ = "whatsapp_configs"
    
    id = Column(String(36), primary_key=True)
    tenant_id = Column(String(100), unique=True, nullable=False, index=True)
    
    # Conexão
    is_connected = Column(Boolean, default=False)
    instance_name = Column(String(100), nullable=True)
    connection_status = Column(String(50), nullable=True)
    last_connection_check = Column(DateTime, nullable=True)
    
    # Configurações de notificação
    auto_notify_pedido_confirmado = Column(Boolean, default=True)
    auto_notify_coleta_realizada = Column(Boolean, default=True)
    auto_notify_em_transito = Column(Boolean, default=True)
    auto_notify_saiu_entrega = Column(Boolean, default=True)
    auto_notify_entregue = Column(Boolean, default=True)
    auto_notify_ocorrencia = Column(Boolean, default=True)
    
    # Chatbot
    chatbot_enabled = Column(Boolean, default=True)
    chatbot_welcome_message = Column(Text, nullable=True)
    chatbot_auto_reply = Column(Boolean, default=True)
    chatbot_business_hours_only = Column(Boolean, default=False)
    
    # Horário comercial
    business_hours_start = Column(String(5), default="08:00")
    business_hours_end = Column(String(5), default="18:00")
    business_days = Column(JSON, default=["monday", "tuesday", "wednesday", "thursday", "friday"])
    
    # Mensagens personalizadas
    out_of_hours_message = Column(Text, nullable=True)
    
    # Auditoria
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<WhatsAppConfig(tenant={self.tenant_id}, connected={self.is_connected})>"
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "is_connected": self.is_connected,
            "instance_name": self.instance_name,
            "connection_status": self.connection_status,
            "last_connection_check": self.last_connection_check.isoformat() if self.last_connection_check else None,
            "auto_notify_pedido_confirmado": self.auto_notify_pedido_confirmado,
            "auto_notify_coleta_realizada": self.auto_notify_coleta_realizada,
            "auto_notify_em_transito": self.auto_notify_em_transito,
            "auto_notify_saiu_entrega": self.auto_notify_saiu_entrega,
            "auto_notify_entregue": self.auto_notify_entregue,
            "auto_notify_ocorrencia": self.auto_notify_ocorrencia,
            "chatbot_enabled": self.chatbot_enabled,
            "chatbot_welcome_message": self.chatbot_welcome_message,
            "chatbot_auto_reply": self.chatbot_auto_reply,
            "chatbot_business_hours_only": self.chatbot_business_hours_only,
            "business_hours_start": self.business_hours_start,
            "business_hours_end": self.business_hours_end,
            "business_days": self.business_days,
            "out_of_hours_message": self.out_of_hours_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
