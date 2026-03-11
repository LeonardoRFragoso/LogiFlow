"""
LogiFlow CRM - Notifications Router
Endpoints para gerenciar notificações do sistema
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from database import get_db
from models_main import Notification, TipoNotificacao, User
from routers.auth import get_current_user
from services.system_notifications import notification_service
from loguru import logger

router = APIRouter(prefix="/api/v1/notifications", tags=["notifications"])


# ========================================
# Schemas
# ========================================

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    tipo: str
    titulo: str
    mensagem: str
    link: Optional[str]
    entity_type: Optional[str]
    entity_id: Optional[int]
    icon: Optional[str]
    color: Optional[str]
    lida: bool
    lida_em: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class NotificationStats(BaseModel):
    total: int
    nao_lidas: int
    lidas: int


# ========================================
# Endpoints
# ========================================

@router.get("/", response_model=List[NotificationResponse])
async def listar_notificacoes(
    apenas_nao_lidas: bool = Query(False, description="Filtrar apenas não lidas"),
    limit: int = Query(50, le=100),
    offset: int = Query(0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista notificações do usuário atual
    """
    notifications = notification_service.obter_notificacoes(
        db=db,
        user_id=current_user.id,
        apenas_nao_lidas=apenas_nao_lidas,
        limit=limit,
        offset=offset
    )
    
    return notifications


@router.get("/stats", response_model=NotificationStats)
async def obter_estatisticas(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtém estatísticas de notificações do usuário
    """
    nao_lidas = notification_service.contar_nao_lidas(db, current_user.id)
    total = db.query(Notification).filter(Notification.user_id == current_user.id).count()
    
    return {
        "total": total,
        "nao_lidas": nao_lidas,
        "lidas": total - nao_lidas
    }


@router.patch("/{notification_id}/read")
async def marcar_como_lida(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Marca uma notificação como lida
    """
    success = notification_service.marcar_como_lida(
        db=db,
        notification_id=notification_id,
        user_id=current_user.id
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    
    return {"success": True, "message": "Notificação marcada como lida"}


@router.patch("/read-all")
async def marcar_todas_como_lidas(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Marca todas as notificações do usuário como lidas
    """
    count = notification_service.marcar_todas_como_lidas(db, current_user.id)
    
    return {
        "success": True,
        "message": f"{count} notificações marcadas como lidas",
        "count": count
    }


@router.delete("/{notification_id}")
async def deletar_notificacao(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deleta uma notificação
    """
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    
    db.delete(notification)
    db.commit()
    
    return {"success": True, "message": "Notificação deletada"}
