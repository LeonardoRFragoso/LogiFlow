"""
LogiFlow CRM - Router Motoristas
Endpoints para gestão de motoristas
"""

from fastapi import APIRouter, HTTPException, Query, Path, UploadFile, File, Request, Depends
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date, timedelta
from enum import Enum
from sqlalchemy.orm import Session
import logging
import uuid
import re

from database import get_db
from models import Motorista
from middleware.tenant import get_current_tenant_id
from loguru import logger

logger = logging.getLogger(__name__)
router = APIRouter()


# ========================================
# Enums
# ========================================

class StatusMotorista(str, Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    FERIAS = "ferias"
    AFASTADO = "afastado"
    DESLIGADO = "desligado"


class CategoriaCNH(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    AB = "AB"
    AC = "AC"
    AD = "AD"
    AE = "AE"


class TipoContrato(str, Enum):
    CLT = "clt"
    AGREGADO = "agregado"
    AUTONOMO = "autonomo"
    TERCEIRIZADO = "terceirizado"


class DisponibilidadeMotorista(str, Enum):
    DISPONIVEL = "disponivel"
    EM_VIAGEM = "em_viagem"
    EM_DESCANSO = "em_descanso"
    INDISPONIVEL = "indisponivel"


# ========================================
# Schemas - Simplificados para MVP (campos planos)
# ========================================

class MotoristaBase(BaseModel):
    """Schema base com campos planos para compatibilidade com frontend"""
    # Dados Pessoais
    nome: str = Field(..., min_length=3, max_length=100)
    cpf: str
    rg: Optional[str] = None
    data_nascimento: Optional[str] = None  # Aceita string para flexibilidade
    
    # CNH - campos planos
    cnh_numero: Optional[str] = None
    cnh_categoria: Optional[str] = "E"
    cnh_validade: Optional[str] = None
    
    # Contato
    telefone: Optional[str] = None
    celular: Optional[str] = None
    email: Optional[str] = None
    
    # Endereço - campos planos
    cep: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    
    # Situação
    status: Optional[str] = "ativo"
    disponibilidade: Optional[str] = "disponivel"
    tipo_contrato: Optional[str] = "clt"
    data_admissao: Optional[str] = None
    
    # Outros
    observacoes: Optional[str] = None
    foto_url: Optional[str] = None
    veiculo_padrao_id: Optional[str] = None


class CriarMotoristaRequest(MotoristaBase):
    """Request para criar motorista"""
    pass


class AtualizarMotoristaRequest(BaseModel):
    """Request para atualizar motorista - todos campos opcionais"""
    nome: Optional[str] = None
    cpf: Optional[str] = None
    rg: Optional[str] = None
    data_nascimento: Optional[str] = None
    cnh_numero: Optional[str] = None
    cnh_categoria: Optional[str] = None
    cnh_validade: Optional[str] = None
    telefone: Optional[str] = None
    celular: Optional[str] = None
    email: Optional[str] = None
    cep: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    status: Optional[str] = None
    disponibilidade: Optional[str] = None
    tipo_contrato: Optional[str] = None
    data_admissao: Optional[str] = None
    observacoes: Optional[str] = None
    foto_url: Optional[str] = None
    veiculo_padrao_id: Optional[str] = None


class MotoristaResponse(BaseModel):
    """Response de motorista"""
    id: int
    nome: str
    cpf: Optional[str] = None
    rg: Optional[str] = None
    data_nascimento: Optional[str] = None
    cnh_numero: Optional[str] = None
    cnh_categoria: Optional[str] = None
    cnh_validade: Optional[str] = None
    telefone: Optional[str] = None
    celular: Optional[str] = None
    email: Optional[str] = None
    cep: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    status: Optional[str] = None
    disponibilidade: Optional[str] = None
    tipo_contrato: Optional[str] = None
    data_admissao: Optional[str] = None
    observacoes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AtualizarDisponibilidadeRequest(BaseModel):
    disponibilidade: str
    motivo: Optional[str] = None
    previsao_retorno: Optional[datetime] = None


# ========================================
# Storage Simulado
# ========================================

motoristas_db: dict = {}


# ========================================
# Endpoints
# ========================================

@router.get("")
async def listar_motoristas(
    request: Request,
    status: Optional[StatusMotorista] = None,
    disponibilidade: Optional[DisponibilidadeMotorista] = None,
    tipo_contrato: Optional[TipoContrato] = None,
    categoria_cnh: Optional[CategoriaCNH] = None,
    busca: Optional[str] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Lista motoristas do tenant atual com filtros"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        # Construir query base filtrando por tenant
        query = db.query(Motorista).filter(Motorista.tenant_id == tenant_id)
        
        # Aplicar filtros adicionais
        if status:
            query = query.filter(Motorista.status == status.value)
        if disponibilidade:
            query = query.filter(Motorista.disponibilidade == disponibilidade.value)
        if tipo_contrato:
            query = query.filter(Motorista.tipo_contrato == tipo_contrato.value)
        if busca:
            query = query.filter(
                (Motorista.nome.ilike(f"%{busca}%")) |
                (Motorista.cpf.ilike(f"%{busca}%"))
            )
        
        # Ordenar por nome
        query = query.order_by(Motorista.nome)
        
        # Paginação
        total = query.count()
        motoristas = query.offset((page - 1) * per_page).limit(per_page).all()
        
        logger.info(f"✅ Listados {len(motoristas)} motoristas do tenant {tenant_id}")
        
        return {
            "success": True,
            "data": motoristas,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "pages": (total + per_page - 1) // per_page
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao listar motoristas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/disponiveis")
async def listar_motoristas_disponiveis(
    categoria_cnh: Optional[str] = None,
    request: Request = None,
    db: Session = Depends(get_db)
):
    """Lista motoristas disponíveis para viagem"""
    try:
        tenant_id = get_current_tenant_id(request) if request else None
        
        query = db.query(Motorista).filter(
            Motorista.status == "ativo",
            Motorista.tenant_id == tenant_id
        )
        
        if categoria_cnh:
            query = query.filter(Motorista.cnh_categoria.contains(categoria_cnh))
        
        motoristas = query.all()
        
        return {
            "success": True,
            "data": motoristas,
            "total": len(motoristas)
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao listar motoristas disponíveis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cnh-vencendo")
async def listar_cnh_vencendo(
    dias: int = Query(30, ge=1, le=180),
    request: Request = None,
    db: Session = Depends(get_db)
):
    """Lista motoristas com CNH vencendo nos próximos dias"""
    try:
        tenant_id = get_current_tenant_id(request) if request else None
        data_limite = date.today() + timedelta(days=dias)
        
        motoristas = db.query(Motorista).filter(
            Motorista.status == "ativo",
            Motorista.tenant_id == tenant_id
        ).all()
        
        resultado = []
        for m in motoristas:
            if m.cnh_validade:
                try:
                    validade = datetime.strptime(m.cnh_validade, "%Y-%m-%d").date() if isinstance(m.cnh_validade, str) else m.cnh_validade
                    if validade <= data_limite:
                        resultado.append({
                            "id": m.id,
                            "nome": m.nome,
                            "cnh_numero": m.cnh_numero,
                            "cnh_categoria": m.cnh_categoria,
                            "cnh_validade": m.cnh_validade,
                            "dias_para_vencer": (validade - date.today()).days
                        })
                except:
                    pass
        
        resultado.sort(key=lambda x: x.get("cnh_validade", ""))
        
        return {
            "success": True,
            "data": resultado,
            "total": len(resultado),
            "alerta": f"CNHs vencendo nos próximos {dias} dias"
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar CNH vencendo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/estatisticas")
async def estatisticas_motoristas(
    request: Request,
    db: Session = Depends(get_db)
):
    """Estatísticas dos motoristas"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        motoristas = db.query(Motorista).filter(Motorista.tenant_id == tenant_id).all()
        
        total = len(motoristas)
        por_status = {}
        
        for m in motoristas:
            status = m.status or "ativo"
            por_status[status] = por_status.get(status, 0) + 1
        
        # CNH vencendo em 30 dias
        data_limite = date.today() + timedelta(days=30)
        cnh_vencendo = 0
        for m in motoristas:
            if m.cnh_validade and m.status == "ativo":
                try:
                    validade = datetime.strptime(m.cnh_validade, "%Y-%m-%d").date() if isinstance(m.cnh_validade, str) else m.cnh_validade
                    if validade <= data_limite:
                        cnh_vencendo += 1
                except:
                    pass
        
        return {
            "success": True,
            "data": {
                "total": total,
                "por_status": por_status,
                "cnh_vencendo_30_dias": cnh_vencendo
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao gerar estatísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{motorista_id}")
async def obter_motorista(
    motorista_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Obtém detalhes de um motorista"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        motorista = db.query(Motorista).filter(
            Motorista.id == motorista_id,
            Motorista.tenant_id == tenant_id
        ).first()
        
        if not motorista:
            raise HTTPException(status_code=404, detail="Motorista não encontrado")
        
        return {
            "success": True,
            "data": motorista
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter motorista: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=MotoristaResponse)
async def criar_motorista(
    motorista_data: CriarMotoristaRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Cadastra um novo motorista"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        # Verificar CPF duplicado
        existing = db.query(Motorista).filter(
            Motorista.cpf == motorista_data.cpf,
            Motorista.tenant_id == tenant_id
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="CPF já cadastrado")
        
        # Criar motorista
        motorista = Motorista(
            nome=motorista_data.nome,
            cpf=motorista_data.cpf,
            rg=motorista_data.rg,
            data_nascimento=motorista_data.data_nascimento,
            cnh_numero=motorista_data.cnh_numero,
            cnh_categoria=motorista_data.cnh_categoria,
            cnh_validade=motorista_data.cnh_validade,
            telefone=motorista_data.telefone,
            celular=motorista_data.celular,
            email=motorista_data.email,
            cep=motorista_data.cep,
            endereco=motorista_data.endereco,
            cidade=motorista_data.cidade,
            uf=motorista_data.uf,
            status=motorista_data.status or "ativo",
            disponibilidade=motorista_data.disponibilidade or "disponivel",
            tipo_contrato=motorista_data.tipo_contrato or "clt",
            data_admissao=motorista_data.data_admissao,
            observacoes=motorista_data.observacoes,
            foto_url=motorista_data.foto_url,
            tenant_id=tenant_id
        )
        
        db.add(motorista)
        db.commit()
        db.refresh(motorista)
        
        logger.info(f"✅ Motorista cadastrado: {motorista.nome} (ID: {motorista.id})")
        
        return motorista
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao criar motorista: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{motorista_id}", response_model=MotoristaResponse)
async def atualizar_motorista(
    motorista_id: int,
    motorista_data: AtualizarMotoristaRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Atualiza dados de um motorista"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        motorista = db.query(Motorista).filter(
            Motorista.id == motorista_id,
            Motorista.tenant_id == tenant_id
        ).first()
        
        if not motorista:
            raise HTTPException(status_code=404, detail="Motorista não encontrado")
        
        # Atualizar apenas campos fornecidos
        update_data = motorista_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None and hasattr(motorista, key):
                setattr(motorista, key, value)
        
        db.commit()
        db.refresh(motorista)
        
        logger.info(f"✅ Motorista atualizado: {motorista.nome}")
        
        return motorista
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao atualizar motorista: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{motorista_id}/status")
async def atualizar_status_motorista(
    motorista_id: int,
    status: str,
    request: Request,
    db: Session = Depends(get_db),
    motivo: Optional[str] = None
):
    """Atualiza status do motorista"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        motorista = db.query(Motorista).filter(
            Motorista.id == motorista_id,
            Motorista.tenant_id == tenant_id
        ).first()
        
        if not motorista:
            raise HTTPException(status_code=404, detail="Motorista não encontrado")
        
        motorista.status = status
        db.commit()
        
        logger.info(f"Status do motorista {motorista.nome} alterado para {status}")
        
        return {
            "success": True,
            "message": f"Status alterado para {status}",
            "data": motorista
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao atualizar status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{motorista_id}/disponibilidade")
async def atualizar_disponibilidade(
    motorista_id: int,
    disp_data: AtualizarDisponibilidadeRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Atualiza disponibilidade do motorista"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        motorista = db.query(Motorista).filter(
            Motorista.id == motorista_id,
            Motorista.tenant_id == tenant_id
        ).first()
        
        if not motorista:
            raise HTTPException(status_code=404, detail="Motorista não encontrado")
        
        motorista.disponibilidade = disp_data.disponibilidade
        db.commit()
        
        return {
            "success": True,
            "message": f"Disponibilidade alterada para {disp_data.disponibilidade}",
            "data": motorista
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao atualizar disponibilidade: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{motorista_id}/viagens")
async def listar_viagens_motorista(
    motorista_id: int,
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100)
):
    """Lista viagens realizadas pelo motorista"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        motorista = db.query(Motorista).filter(
            Motorista.id == motorista_id,
            Motorista.tenant_id == tenant_id
        ).first()
        
        if not motorista:
            raise HTTPException(status_code=404, detail="Motorista não encontrado")
        
        # Retorna lista vazia por enquanto
        return {
            "success": True,
            "data": [],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": 0,
                "pages": 0
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao listar viagens: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{motorista_id}")
async def excluir_motorista(
    motorista_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Exclui (inativa) um motorista"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        motorista = db.query(Motorista).filter(
            Motorista.id == motorista_id,
            Motorista.tenant_id == tenant_id
        ).first()
        
        if not motorista:
            raise HTTPException(status_code=404, detail="Motorista não encontrado")
        
        # Soft delete - apenas inativa
        motorista.status = "desligado"
        motorista.disponibilidade = "indisponivel"
        db.commit()
        
        logger.info(f"Motorista desligado: {motorista.nome}")
        
        return {
            "success": True,
            "message": "Motorista desligado com sucesso"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao excluir motorista: {e}")
        raise HTTPException(status_code=500, detail=str(e))
