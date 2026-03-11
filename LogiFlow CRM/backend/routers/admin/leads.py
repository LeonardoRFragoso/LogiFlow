"""
LogiFlow CRM - Admin Leads Router
Gestão de leads de demonstração para administradores
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from database import get_db
from models_main import User, Tenant, TipoNotificacao
from models import Lead, StatusLead
from routers.auth import get_current_user, get_current_admin
from services.system_notifications import notification_service
from loguru import logger

router = APIRouter(prefix="/admin/leads", tags=["Admin - Leads"])


# ========================================
# Schemas
# ========================================

class LeadListResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    company: str
    vehicles: Optional[str]
    message: Optional[str]
    status: str
    source: str
    assigned_to: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class LeadDetailResponse(LeadListResponse):
    converted_at: Optional[datetime]
    tenant_id: Optional[int]
    
    class Config:
        from_attributes = True


class UpdateLeadStatusRequest(BaseModel):
    status: str  # novo, contatado, qualificado, convertido, perdido
    observacao: Optional[str] = None


class AssignLeadRequest(BaseModel):
    user_id: int


class ConvertLeadRequest(BaseModel):
    create_tenant: bool = True
    tenant_name: Optional[str] = None
    plan_type: str = "trial"  # trial, starter, professional, enterprise


class AddLeadNoteRequest(BaseModel):
    nota: str


# ========================================
# Endpoints - Listagem e Filtros
# ========================================

@router.get("/", response_model=List[LeadListResponse])
async def listar_leads_admin(
    status: Optional[str] = Query(None, description="Filtrar por status"),
    source: Optional[str] = Query(None, description="Filtrar por origem"),
    assigned_to: Optional[int] = Query(None, description="Filtrar por vendedor"),
    search: Optional[str] = Query(None, description="Buscar por nome, email ou empresa"),
    limit: int = Query(50, le=100),
    offset: int = Query(0),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Lista todos os leads de demonstração (apenas admin)
    Suporta filtros por status, origem, vendedor e busca
    """
    query = db.query(Lead)
    
    # Filtros
    if status:
        query = query.filter(Lead.status == status)
    if source:
        query = query.filter(Lead.source == source)
    if assigned_to:
        query = query.filter(Lead.assigned_to == assigned_to)
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Lead.name.ilike(search_filter)) |
            (Lead.email.ilike(search_filter)) |
            (Lead.company.ilike(search_filter))
        )
    
    # Ordenar por mais recentes primeiro
    leads = query.order_by(Lead.created_at.desc()).offset(offset).limit(limit).all()
    
    logger.info(f"Admin {current_user.email} listou {len(leads)} leads")
    return leads


@router.get("/stats")
async def obter_estatisticas_leads(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Obtém estatísticas de leads para o dashboard admin
    """
    total = db.query(Lead).count()
    novos = db.query(Lead).filter(Lead.status == StatusLead.NOVO.value).count()
    contatados = db.query(Lead).filter(Lead.status == StatusLead.CONTATADO.value).count()
    qualificados = db.query(Lead).filter(Lead.status == StatusLead.QUALIFICADO.value).count()
    convertidos = db.query(Lead).filter(Lead.status == StatusLead.CONVERTIDO.value).count()
    perdidos = db.query(Lead).filter(Lead.status == StatusLead.PERDIDO.value).count()
    
    # Leads por origem
    por_origem = {}
    for source in ["site", "indicacao", "google", "facebook", "outro"]:
        count = db.query(Lead).filter(Lead.source == source).count()
        if count > 0:
            por_origem[source] = count
    
    return {
        "success": True,
        "data": {
            "total": total,
            "por_status": {
                "novos": novos,
                "contatados": contatados,
                "qualificados": qualificados,
                "convertidos": convertidos,
                "perdidos": perdidos
            },
            "por_origem": por_origem,
            "taxa_conversao": round((convertidos / total * 100) if total > 0 else 0, 2)
        }
    }


# ========================================
# Endpoints - Detalhes e Atualização
# ========================================

@router.get("/{lead_id}", response_model=LeadDetailResponse)
async def obter_lead_detalhes(
    lead_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Obtém detalhes completos de um lead específico
    """
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    
    return lead


@router.patch("/{lead_id}/status")
async def atualizar_status_lead(
    lead_id: int,
    request: UpdateLeadStatusRequest,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Atualiza o status de um lead
    """
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    
    status_anterior = lead.status
    lead.status = request.status
    lead.updated_at = datetime.utcnow()
    
    # Se foi convertido, marcar data de conversão
    if request.status == StatusLead.CONVERTIDO.value and not lead.converted_at:
        lead.converted_at = datetime.utcnow()
    
    db.commit()
    db.refresh(lead)
    
    logger.info(f"Lead {lead_id} status alterado de {status_anterior} para {request.status} por {current_user.email}")
    
    return {
        "success": True,
        "message": f"Status atualizado para {request.status}",
        "data": {
            "id": lead.id,
            "status": lead.status,
            "status_anterior": status_anterior
        }
    }


@router.patch("/{lead_id}/assign")
async def atribuir_lead(
    lead_id: int,
    request: AssignLeadRequest,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Atribui um lead a um vendedor/usuário
    """
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    
    # Verificar se usuário existe
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    lead.assigned_to = request.user_id
    lead.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(lead)
    
    # Criar notificação para o usuário atribuído
    try:
        notification_service.criar_notificacao(
            db=db,
            user_id=request.user_id,
            tipo=TipoNotificacao.LEAD_ATRIBUIDO,
            titulo=f"Lead atribuído: {lead.company}",
            mensagem=f"O lead {lead.name} da empresa {lead.company} foi atribuído a você. Telefone: {lead.phone}",
            link=f"/admin/leads/{lead.id}",
            entity_type="lead",
            entity_id=lead.id
        )
    except Exception as e:
        logger.error(f"Erro ao criar notificação: {e}")
    
    logger.info(f"Lead {lead_id} atribuído a {user.email} por {current_user.email}")
    
    return {
        "success": True,
        "message": f"Lead atribuído a {user.nome}",
        "data": {
            "id": lead.id,
            "assigned_to": lead.assigned_to,
            "assigned_to_name": user.nome
        }
    }


# ========================================
# Endpoints - Conversão
# ========================================

@router.post("/{lead_id}/convert")
async def converter_lead(
    lead_id: int,
    request: ConvertLeadRequest,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Converte um lead em cliente/tenant
    Cria tenant e usuário automaticamente
    """
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    
    if lead.status == StatusLead.CONVERTIDO.value:
        raise HTTPException(status_code=400, detail="Lead já foi convertido")
    
    tenant = None
    
    if request.create_tenant:
        # Criar tenant
        from routers.auth import _hash_senha
        import secrets
        import string
        
        tenant_name = request.tenant_name or lead.company
        
        # Verificar se tenant já existe
        existing_tenant = db.query(Tenant).filter(Tenant.nome == tenant_name).first()
        if existing_tenant:
            raise HTTPException(status_code=400, detail=f"Tenant {tenant_name} já existe")
        
        tenant = Tenant(
            nome=tenant_name,
            email=lead.email,
            plano=request.plan_type,
            status="active"
        )
        db.add(tenant)
        db.flush()  # Para obter o ID do tenant
        
        # Criar usuário admin para o tenant
        senha_temporaria = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
        
        user = User(
            email=lead.email,
            nome=lead.name,
            senha_hash=_hash_senha(senha_temporaria),
            tipo="admin",
            status="ativo",
            tenant_id=tenant.id
        )
        db.add(user)
        
        # Atualizar lead
        lead.status = StatusLead.CONVERTIDO.value
        lead.converted_at = datetime.utcnow()
        lead.tenant_id = tenant.id
        lead.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(lead)
        db.refresh(tenant)
        db.refresh(user)
        
        logger.info(f"Lead {lead_id} convertido em tenant {tenant.id} por {current_user.email}")
        
        # TODO: Enviar email com credenciais de acesso
        
        return {
            "success": True,
            "message": "Lead convertido com sucesso",
            "data": {
                "lead_id": lead.id,
                "tenant_id": tenant.id,
                "tenant_name": tenant.nome,
                "user_id": user.id,
                "user_email": user.email,
                "senha_temporaria": senha_temporaria,
                "plano": tenant.plano
            }
        }
    else:
        # Apenas marcar como convertido sem criar tenant
        lead.status = StatusLead.CONVERTIDO.value
        lead.converted_at = datetime.utcnow()
        lead.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(lead)
        
        return {
            "success": True,
            "message": "Lead marcado como convertido",
            "data": {
                "lead_id": lead.id,
                "status": lead.status
            }
        }


# ========================================
# Endpoints - Exclusão
# ========================================

@router.delete("/{lead_id}")
async def deletar_lead(
    lead_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Deleta um lead (apenas admin)
    """
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    
    db.delete(lead)
    db.commit()
    
    logger.info(f"Lead {lead_id} deletado por {current_user.email}")
    
    return {
        "success": True,
        "message": "Lead deletado com sucesso"
    }


# ========================================
# Endpoints - Ações em Lote
# ========================================

@router.post("/bulk/assign")
async def atribuir_leads_em_lote(
    lead_ids: List[int],
    user_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Atribui múltiplos leads a um vendedor
    """
    # Verificar se usuário existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Atualizar leads
    updated = db.query(Lead).filter(Lead.id.in_(lead_ids)).update(
        {
            "assigned_to": user_id,
            "updated_at": datetime.utcnow()
        },
        synchronize_session=False
    )
    
    db.commit()
    
    logger.info(f"{updated} leads atribuídos a {user.email} por {current_user.email}")
    
    return {
        "success": True,
        "message": f"{updated} leads atribuídos a {user.nome}",
        "count": updated
    }


@router.post("/bulk/update-status")
async def atualizar_status_em_lote(
    lead_ids: List[int],
    status: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Atualiza status de múltiplos leads
    """
    updated = db.query(Lead).filter(Lead.id.in_(lead_ids)).update(
        {
            "status": status,
            "updated_at": datetime.utcnow()
        },
        synchronize_session=False
    )
    
    db.commit()
    
    logger.info(f"{updated} leads atualizados para status {status} por {current_user.email}")
    
    return {
        "success": True,
        "message": f"{updated} leads atualizados para {status}",
        "count": updated
    }
