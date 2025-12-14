"""
LogiFlow CRM - Leads Router
============================
Gerenciamento de leads capturados do site
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

from database import get_db
from models import Lead, StatusLead

router = APIRouter(prefix="/api/leads", tags=["leads"])


# ========================================
# Schemas
# ========================================

class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    company: str
    vehicles: Optional[str] = None
    message: Optional[str] = None
    source: str = "site"


class LeadUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[int] = None
    message: Optional[str] = None


class LeadResponse(BaseModel):
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
    converted_at: Optional[datetime]
    tenant_id: Optional[int]

    class Config:
        from_attributes = True


# ========================================
# Endpoints
# ========================================

@router.post("/", response_model=LeadResponse, status_code=201)
async def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    """
    Criar novo lead (usado pelo formulário do site)
    """
    # Verificar se email já existe
    existing = db.query(Lead).filter(Lead.email == lead.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    db_lead = Lead(
        name=lead.name,
        email=lead.email,
        phone=lead.phone,
        company=lead.company,
        vehicles=lead.vehicles,
        message=lead.message,
        source=lead.source,
        status=StatusLead.NOVO.value
    )
    
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    
    # TODO: Enviar email de notificação para equipe de vendas
    # TODO: Enviar email de confirmação para o lead
    
    return db_lead


@router.get("/", response_model=List[LeadResponse])
async def list_leads(
    status: Optional[str] = Query(None, description="Filtrar por status"),
    source: Optional[str] = Query(None, description="Filtrar por origem"),
    assigned_to: Optional[int] = Query(None, description="Filtrar por vendedor"),
    limit: int = Query(50, le=100),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    """
    Listar leads com filtros
    """
    query = db.query(Lead)
    
    if status:
        query = query.filter(Lead.status == status)
    if source:
        query = query.filter(Lead.source == source)
    if assigned_to:
        query = query.filter(Lead.assigned_to == assigned_to)
    
    query = query.order_by(Lead.created_at.desc())
    leads = query.offset(offset).limit(limit).all()
    
    return leads


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(lead_id: int, db: Session = Depends(get_db)):
    """
    Obter detalhes de um lead específico
    """
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    
    return lead


@router.patch("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: int,
    lead_update: LeadUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualizar status/informações do lead
    """
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    
    if lead_update.status:
        # Validar status
        try:
            StatusLead(lead_update.status)
            lead.status = lead_update.status
            
            # Se convertido, registrar data
            if lead_update.status == StatusLead.CONVERTIDO.value:
                lead.converted_at = datetime.utcnow()
        except ValueError:
            raise HTTPException(status_code=400, detail="Status inválido")
    
    if lead_update.assigned_to is not None:
        lead.assigned_to = lead_update.assigned_to
    
    if lead_update.message:
        lead.message = lead_update.message
    
    lead.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(lead)
    
    return lead


@router.delete("/{lead_id}", status_code=204)
async def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    """
    Deletar lead
    """
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    
    db.delete(lead)
    db.commit()
    
    return None


@router.get("/stats/summary")
async def get_leads_stats(db: Session = Depends(get_db)):
    """
    Estatísticas de leads
    """
    total = db.query(Lead).count()
    novos = db.query(Lead).filter(Lead.status == StatusLead.NOVO.value).count()
    qualificados = db.query(Lead).filter(Lead.status == StatusLead.QUALIFICADO.value).count()
    convertidos = db.query(Lead).filter(Lead.status == StatusLead.CONVERTIDO.value).count()
    perdidos = db.query(Lead).filter(Lead.status == StatusLead.PERDIDO.value).count()
    
    # Taxa de conversão
    taxa_conversao = (convertidos / total * 100) if total > 0 else 0
    
    return {
        "total": total,
        "novos": novos,
        "qualificados": qualificados,
        "convertidos": convertidos,
        "perdidos": perdidos,
        "taxa_conversao": round(taxa_conversao, 2)
    }
