"""
Modelo de Notificações para LogiFlow CRM
Sistema de notificações em tempo real para usuários
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from database import Base


class TipoNotificacao(str, enum.Enum):
    """Tipos de notificação"""
    NOVO_LEAD = "novo_lead"
    LEAD_ATRIBUIDO = "lead_atribuido"
    LEAD_CONVERTIDO = "lead_convertido"
    NOVO_PEDIDO = "novo_pedido"
    PEDIDO_ATUALIZADO = "pedido_atualizado"
    ENTREGA_CONFIRMADA = "entrega_confirmada"
    ENTREGA_ATRASADA = "entrega_atrasada"
    NOVA_COTACAO = "nova_cotacao"
    COTACAO_APROVADA = "cotacao_aprovada"
    OCORRENCIA_CRIADA = "ocorrencia_criada"
    USUARIO_CRIADO = "usuario_criado"
    SISTEMA = "sistema"


class Notification(Base):
    """
    Modelo de Notificação
    Armazena notificações para usuários do sistema
    """
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Destinatário
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Tipo e conteúdo
    tipo = Column(SQLEnum(TipoNotificacao), nullable=False, index=True)
    titulo = Column(String(255), nullable=False)
    mensagem = Column(Text, nullable=False)
    
    # Dados adicionais (JSON-like)
    link = Column(String(500), nullable=True)  # Link para a entidade relacionada
    entity_type = Column(String(50), nullable=True)  # Ex: "lead", "pedido", "entrega"
    entity_id = Column(Integer, nullable=True)  # ID da entidade relacionada
    
    # Metadata
    icon = Column(String(50), nullable=True)  # Emoji ou nome do ícone
    color = Column(String(20), nullable=True)  # Cor da notificação (ex: "success", "warning")
    
    # Status
    lida = Column(Boolean, default=False, nullable=False, index=True)
    lida_em = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relacionamentos
    user = relationship("User", back_populates="notifications")
    
    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, tipo={self.tipo}, lida={self.lida})>"
    
    def to_dict(self):
        """Converte notificação para dicionário"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "tipo": self.tipo.value if isinstance(self.tipo, enum.Enum) else self.tipo,
            "titulo": self.titulo,
            "mensagem": self.mensagem,
            "link": self.link,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "icon": self.icon,
            "color": self.color,
            "lida": self.lida,
            "lida_em": self.lida_em.isoformat() if self.lida_em else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
