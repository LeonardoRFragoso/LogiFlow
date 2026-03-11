"""
Sistema de Notificações do LogiFlow CRM
Gerencia notificações em tempo real para usuários
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from loguru import logger

from models_main import Notification, TipoNotificacao, User


class SystemNotificationService:
    """Serviço para criar e gerenciar notificações do sistema"""
    
    @staticmethod
    def criar_notificacao(
        db: Session,
        user_id: int,
        tipo: TipoNotificacao,
        titulo: str,
        mensagem: str,
        link: Optional[str] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[int] = None,
        icon: Optional[str] = None,
        color: Optional[str] = None
    ) -> Notification:
        """
        Cria uma nova notificação para um usuário
        
        Args:
            db: Sessão do banco de dados
            user_id: ID do usuário destinatário
            tipo: Tipo da notificação
            titulo: Título da notificação
            mensagem: Mensagem detalhada
            link: Link relacionado (opcional)
            entity_type: Tipo da entidade relacionada (opcional)
            entity_id: ID da entidade relacionada (opcional)
            icon: Ícone/emoji da notificação (opcional)
            color: Cor da notificação (opcional)
        
        Returns:
            Notification: Notificação criada
        """
        notification = Notification(
            user_id=user_id,
            tipo=tipo,
            titulo=titulo,
            mensagem=mensagem,
            link=link,
            entity_type=entity_type,
            entity_id=entity_id,
            icon=icon or SystemNotificationService._get_default_icon(tipo),
            color=color or SystemNotificationService._get_default_color(tipo),
            lida=False
        )
        
        db.add(notification)
        db.commit()
        db.refresh(notification)
        
        logger.info(f"Notificação criada: {tipo.value} para user_id={user_id}")
        return notification
    
    @staticmethod
    def criar_notificacao_para_admins(
        db: Session,
        tipo: TipoNotificacao,
        titulo: str,
        mensagem: str,
        **kwargs
    ) -> List[Notification]:
        """
        Cria notificação para todos os usuários admin
        
        Returns:
            List[Notification]: Lista de notificações criadas
        """
        admins = db.query(User).filter(User.tipo == "admin", User.status == "ativo").all()
        notifications = []
        
        for admin in admins:
            notification = SystemNotificationService.criar_notificacao(
                db=db,
                user_id=admin.id,
                tipo=tipo,
                titulo=titulo,
                mensagem=mensagem,
                **kwargs
            )
            notifications.append(notification)
        
        logger.info(f"Notificação enviada para {len(admins)} admins")
        return notifications
    
    @staticmethod
    def marcar_como_lida(db: Session, notification_id: int, user_id: int) -> bool:
        """
        Marca uma notificação como lida
        
        Returns:
            bool: True se marcada com sucesso
        """
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()
        
        if not notification:
            return False
        
        notification.lida = True
        notification.lida_em = datetime.utcnow()
        db.commit()
        
        return True
    
    @staticmethod
    def marcar_todas_como_lidas(db: Session, user_id: int) -> int:
        """
        Marca todas as notificações de um usuário como lidas
        
        Returns:
            int: Número de notificações marcadas
        """
        count = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.lida == False
        ).update({
            "lida": True,
            "lida_em": datetime.utcnow()
        })
        
        db.commit()
        return count
    
    @staticmethod
    def obter_notificacoes(
        db: Session,
        user_id: int,
        apenas_nao_lidas: bool = False,
        limit: int = 50,
        offset: int = 0
    ) -> List[Notification]:
        """
        Obtém notificações de um usuário
        
        Returns:
            List[Notification]: Lista de notificações
        """
        query = db.query(Notification).filter(Notification.user_id == user_id)
        
        if apenas_nao_lidas:
            query = query.filter(Notification.lida == False)
        
        notifications = query.order_by(
            Notification.created_at.desc()
        ).offset(offset).limit(limit).all()
        
        return notifications
    
    @staticmethod
    def contar_nao_lidas(db: Session, user_id: int) -> int:
        """
        Conta notificações não lidas de um usuário
        
        Returns:
            int: Número de notificações não lidas
        """
        count = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.lida == False
        ).count()
        
        return count
    
    @staticmethod
    def _get_default_icon(tipo: TipoNotificacao) -> str:
        """Retorna ícone padrão baseado no tipo"""
        icons = {
            TipoNotificacao.NOVO_LEAD: "👤",
            TipoNotificacao.LEAD_ATRIBUIDO: "📋",
            TipoNotificacao.LEAD_CONVERTIDO: "✅",
            TipoNotificacao.NOVO_PEDIDO: "📦",
            TipoNotificacao.PEDIDO_ATUALIZADO: "🔄",
            TipoNotificacao.ENTREGA_CONFIRMADA: "✅",
            TipoNotificacao.ENTREGA_ATRASADA: "⚠️",
            TipoNotificacao.NOVA_COTACAO: "💰",
            TipoNotificacao.COTACAO_APROVADA: "✅",
            TipoNotificacao.OCORRENCIA_CRIADA: "⚠️",
            TipoNotificacao.USUARIO_CRIADO: "👤",
            TipoNotificacao.SISTEMA: "ℹ️"
        }
        return icons.get(tipo, "📌")
    
    @staticmethod
    def _get_default_color(tipo: TipoNotificacao) -> str:
        """Retorna cor padrão baseada no tipo"""
        colors = {
            TipoNotificacao.NOVO_LEAD: "blue",
            TipoNotificacao.LEAD_ATRIBUIDO: "purple",
            TipoNotificacao.LEAD_CONVERTIDO: "green",
            TipoNotificacao.NOVO_PEDIDO: "blue",
            TipoNotificacao.PEDIDO_ATUALIZADO: "yellow",
            TipoNotificacao.ENTREGA_CONFIRMADA: "green",
            TipoNotificacao.ENTREGA_ATRASADA: "red",
            TipoNotificacao.NOVA_COTACAO: "blue",
            TipoNotificacao.COTACAO_APROVADA: "green",
            TipoNotificacao.OCORRENCIA_CRIADA: "orange",
            TipoNotificacao.USUARIO_CRIADO: "blue",
            TipoNotificacao.SISTEMA: "gray"
        }
        return colors.get(tipo, "gray")


# Instância global
notification_service = SystemNotificationService()
