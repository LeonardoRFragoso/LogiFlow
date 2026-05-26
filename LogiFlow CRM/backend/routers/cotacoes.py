"""
LogiFlow CRM - Router Cotações
Endpoints para gestão de cotações de frete
"""

from fastapi import APIRouter, HTTPException, Query, Path, Depends, Request
from pydantic import BaseModel, Field, validator
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, date, timedelta
from enum import Enum
from decimal import Decimal
import logging
import uuid

from database import get_db
from models import Cotacao
from middleware.tenant import get_current_tenant_id

logger = logging.getLogger(__name__)
router = APIRouter()


# ========================================
# Enums
# ========================================

class StatusCotacao(str, Enum):
    RASCUNHO = "rascunho"
    ENVIADA = "enviada"
    EM_ANALISE = "em_analise"
    APROVADA = "aprovada"
    REJEITADA = "rejeitada"
    EXPIRADA = "expirada"
    CONVERTIDA = "convertida"  # Virou pedido


class TipoFrete(str, Enum):
    CIF = "cif"  # Frete por conta do remetente
    FOB = "fob"  # Frete por conta do destinatário


class TipoCarga(str, Enum):
    FRACIONADA = "fracionada"
    LOTACAO = "lotacao"
    CONTAINER = "container"
    GRANEL = "granel"


class ModalTransporte(str, Enum):
    RODOVIARIO = "rodoviario"
    AEREO = "aereo"
    MARITIMO = "maritimo"
    FERROVIARIO = "ferroviario"


# ========================================
# Schemas - Simplificados para MVP (campos planos)
# ========================================

class CotacaoBase(BaseModel):
    """Schema base com campos planos para compatibilidade com frontend"""
    # Cliente
    cliente: Optional[str] = None  # ID do cliente (frontend envia como 'cliente')
    cliente_id: Optional[str] = None  # Alias
    cliente_nome: Optional[str] = None
    
    # Origem - campos planos
    origem_cidade: Optional[str] = None
    origem_uf: Optional[str] = None
    origem_cep: Optional[str] = None
    origem_logradouro: Optional[str] = None
    
    # Destino - campos planos
    destino_cidade: Optional[str] = None
    destino_uf: Optional[str] = None
    destino_cep: Optional[str] = None
    destino_logradouro: Optional[str] = None
    
    # Carga
    tipo_carga: Optional[str] = "geral"
    modal: Optional[str] = "rodoviario"
    peso_kg: Optional[float] = None
    cubagem_m3: Optional[float] = None
    quantidade_volumes: Optional[int] = 1
    valor_mercadoria: Optional[float] = None
    
    # Valores e Prazo
    prazo_estimado: Optional[int] = 5
    valor_frete: Optional[float] = None
    valor_seguro: Optional[float] = 0
    valor_adicional: Optional[float] = 0
    validade: Optional[str] = None
    
    # Status e Observações
    status: Optional[str] = "rascunho"
    urgente: bool = False
    observacoes: Optional[str] = None


class CriarCotacaoRequest(CotacaoBase):
    """Request para criar cotação"""
    pass


class AtualizarCotacaoRequest(CotacaoBase):
    """Request para atualizar cotação - todos campos opcionais"""
    pass


class AprovarCotacaoRequest(BaseModel):
    observacao: Optional[str] = None
    criar_pedido: bool = True


class RejeitarCotacaoRequest(BaseModel):
    motivo: str = Field(..., min_length=5)


class CotacaoResponse(BaseModel):
    """Response de cotação"""
    id: int
    numero: Optional[str] = None
    cliente_id: Optional[str] = None
    cliente_nome: Optional[str] = None
    status: Optional[str] = None
    origem_cidade: Optional[str] = None
    origem_uf: Optional[str] = None
    destino_cidade: Optional[str] = None
    destino_uf: Optional[str] = None
    tipo_carga: Optional[str] = None
    modal: Optional[str] = None
    peso_kg: Optional[float] = None
    cubagem_m3: Optional[float] = None
    quantidade_volumes: Optional[int] = None
    valor_mercadoria: Optional[float] = None
    prazo_estimado: Optional[int] = None
    valor_frete: Optional[float] = None
    valor_seguro: Optional[float] = None
    valor_adicional: Optional[float] = None
    validade: Optional[str] = None
    urgente: bool = False
    observacoes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ========================================
# Storage Simulado (substituir por Repository Pattern)
# ========================================

cotacoes_db: dict = {}
cotacao_counter = 1000


def gerar_numero_cotacao() -> str:
    global cotacao_counter
    cotacao_counter += 1
    ano = datetime.now().year
    return f"COT-{ano}-{cotacao_counter:05d}"


# ========================================
# Endpoints
# ========================================

@router.get("")
async def listar_cotacoes(
    request: Request,
    status: Optional[str] = None,
    cliente_id: Optional[int] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    urgente: Optional[bool] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Lista cotações com filtros opcionais"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        query = db.query(Cotacao).filter(Cotacao.tenant_id == tenant_id)
        
        # Aplicar filtros
        if status:
            query = query.filter(Cotacao.status == status)
        if cliente_id:
            query = query.filter(Cotacao.cliente_id == cliente_id)
        if urgente is not None:
            query = query.filter(Cotacao.urgente == urgente)
        if data_inicio:
            query = query.filter(Cotacao.created_at >= data_inicio)
        if data_fim:
            query = query.filter(Cotacao.created_at <= data_fim)
        
        # Ordenar por data (mais recentes primeiro)
        query = query.order_by(Cotacao.created_at.desc())
        
        # Paginação
        total = query.count()
        cotacoes = query.offset((page - 1) * per_page).limit(per_page).all()
        
        logger.info(f"✅ Listadas {len(cotacoes)} cotações do tenant {tenant_id}")
        
        return {
            "success": True,
            "data": cotacoes,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "pages": (total + per_page - 1) // per_page
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao listar cotações: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/estatisticas")
async def estatisticas_cotacoes(
    request: Request,
    db: Session = Depends(get_db)
):
    """Retorna estatísticas das cotações"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        cotacoes = db.query(Cotacao).filter(Cotacao.tenant_id == tenant_id).all()
        
        total = len(cotacoes)
        por_status = {}
        valor_total = 0
        
        for c in cotacoes:
            status = c.status or "rascunho"
            por_status[status] = por_status.get(status, 0) + 1
            if c.status in ["aprovada", "convertida"]:
                valor_total += (c.valor_frete or 0) + (c.valor_seguro or 0) + (c.valor_adicional or 0)
        
        return {
            "success": True,
            "data": {
                "total": total,
                "por_status": por_status,
                "valor_aprovado": valor_total,
                "taxa_conversao": round(
                    (por_status.get("convertida", 0) / total * 100) if total > 0 else 0, 2
                )
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao gerar estatísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{cotacao_id}", response_model=CotacaoResponse)
async def obter_cotacao(
    cotacao_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Obtém detalhes de uma cotação"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        cotacao = db.query(Cotacao).filter(
            Cotacao.id == cotacao_id,
            Cotacao.tenant_id == tenant_id
        ).first()
        
        if not cotacao:
            raise HTTPException(status_code=404, detail="Cotação não encontrada")
        
        return cotacao
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao obter cotação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=CotacaoResponse)
async def criar_cotacao(
    cotacao_data: CriarCotacaoRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Cria uma nova cotação"""
    try:
        tenant_id = get_current_tenant_id(request)
        numero = gerar_numero_cotacao()
        
        # Pegar cliente_id do campo 'cliente' ou 'cliente_id'
        cliente_id = cotacao_data.cliente or cotacao_data.cliente_id
        
        cotacao = Cotacao(
            numero=numero,
            cliente_id=int(cliente_id) if cliente_id else None,
            cliente_nome=cotacao_data.cliente_nome,
            origem_cidade=cotacao_data.origem_cidade,
            origem_uf=cotacao_data.origem_uf,
            origem_cep=cotacao_data.origem_cep,
            origem_logradouro=cotacao_data.origem_logradouro,
            destino_cidade=cotacao_data.destino_cidade,
            destino_uf=cotacao_data.destino_uf,
            destino_cep=cotacao_data.destino_cep,
            destino_logradouro=cotacao_data.destino_logradouro,
            tipo_carga=cotacao_data.tipo_carga,
            modal=cotacao_data.modal,
            peso_kg=cotacao_data.peso_kg or 0,
            cubagem_m3=cotacao_data.cubagem_m3,
            quantidade_volumes=cotacao_data.quantidade_volumes or 1,
            valor_mercadoria=cotacao_data.valor_mercadoria or 0,
            prazo_estimado=cotacao_data.prazo_estimado or 5,
            valor_frete=cotacao_data.valor_frete or 0,
            valor_seguro=cotacao_data.valor_seguro or 0,
            valor_adicional=cotacao_data.valor_adicional or 0,
            validade=cotacao_data.validade,
            status="rascunho",
            urgente=cotacao_data.urgente or False,
            observacoes=cotacao_data.observacoes,
            tenant_id=tenant_id
        )
        
        db.add(cotacao)
        db.commit()
        db.refresh(cotacao)
        
        logger.info(f"✅ Cotação criada: {numero} (ID: {cotacao.id})")
        
        return cotacao
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao criar cotação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{cotacao_id}", response_model=CotacaoResponse)
async def atualizar_cotacao(
    cotacao_id: int,
    cotacao_data: AtualizarCotacaoRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Atualiza uma cotação existente"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        cotacao = db.query(Cotacao).filter(
            Cotacao.id == cotacao_id,
            Cotacao.tenant_id == tenant_id
        ).first()
        
        if not cotacao:
            raise HTTPException(status_code=404, detail="Cotação não encontrada")
        
        # Só permite editar cotações em rascunho ou enviada
        if cotacao.status not in ["rascunho", "enviada"]:
            raise HTTPException(
                status_code=400,
                detail=f"Não é possível editar cotação com status '{cotacao.status}'"
            )
        
        # Atualizar campos fornecidos
        update_data = cotacao_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None and hasattr(cotacao, key):
                setattr(cotacao, key, value)
        
        db.commit()
        db.refresh(cotacao)
        
        logger.info(f"✅ Cotação atualizada: {cotacao.numero}")
        
        return cotacao
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao atualizar cotação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{cotacao_id}/enviar")
async def enviar_cotacao(
    cotacao_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Envia cotação para o cliente"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        cotacao = db.query(Cotacao).filter(
            Cotacao.id == cotacao_id,
            Cotacao.tenant_id == tenant_id
        ).first()
        
        if not cotacao:
            raise HTTPException(status_code=404, detail="Cotação não encontrada")
        
        if cotacao.status != "rascunho":
            raise HTTPException(
                status_code=400,
                detail="Apenas cotações em rascunho podem ser enviadas"
            )
        
        cotacao.status = "enviada"
        db.commit()
        
        logger.info(f"✅ Cotação enviada: {cotacao.numero}")
        
        return {
            "success": True,
            "message": "Cotação enviada com sucesso",
            "data": cotacao
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao enviar cotação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{cotacao_id}/aprovar")
async def aprovar_cotacao(
    cotacao_id: int,
    aprovar_data: AprovarCotacaoRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Aprova uma cotação e opcionalmente cria pedido"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        cotacao = db.query(Cotacao).filter(
            Cotacao.id == cotacao_id,
            Cotacao.tenant_id == tenant_id
        ).first()
        
        if not cotacao:
            raise HTTPException(status_code=404, detail="Cotação não encontrada")
        
        if cotacao.status not in ["enviada", "em_analise"]:
            raise HTTPException(
                status_code=400,
                detail="Apenas cotações enviadas ou em análise podem ser aprovadas"
            )
        
        cotacao.status = "aprovada"
        db.commit()
        
        logger.info(f"✅ Cotação aprovada: {cotacao.numero}")
        
        return {
            "success": True,
            "message": "Cotação aprovada com sucesso",
            "data": cotacao
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao aprovar cotação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{cotacao_id}/rejeitar")
async def rejeitar_cotacao(
    cotacao_id: int,
    rejeitar_data: RejeitarCotacaoRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Rejeita uma cotação"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        cotacao = db.query(Cotacao).filter(
            Cotacao.id == cotacao_id,
            Cotacao.tenant_id == tenant_id
        ).first()
        
        if not cotacao:
            raise HTTPException(status_code=404, detail="Cotação não encontrada")
        
        if cotacao.status in ["convertida", "rejeitada"]:
            raise HTTPException(
                status_code=400,
                detail=f"Não é possível rejeitar cotação com status '{cotacao.status}'"
            )
        
        cotacao.status = "rejeitada"
        db.commit()
        
        logger.info(f"✅ Cotação rejeitada: {cotacao.numero}")
        
        return {
            "success": True,
            "message": "Cotação rejeitada",
            "data": cotacao
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao rejeitar cotação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{cotacao_id}/duplicar")
async def duplicar_cotacao(
    cotacao_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Cria cópia de uma cotação"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        cotacao_original = db.query(Cotacao).filter(
            Cotacao.id == cotacao_id,
            Cotacao.tenant_id == tenant_id
        ).first()
        
        if not cotacao_original:
            raise HTTPException(status_code=404, detail="Cotação não encontrada")
        
        novo_numero = gerar_numero_cotacao()
        
        nova_cotacao = Cotacao(
            numero=novo_numero,
            cliente_id=cotacao_original.cliente_id,
            cliente_nome=cotacao_original.cliente_nome,
            origem_cidade=cotacao_original.origem_cidade,
            origem_uf=cotacao_original.origem_uf,
            origem_cep=cotacao_original.origem_cep,
            origem_logradouro=cotacao_original.origem_logradouro,
            destino_cidade=cotacao_original.destino_cidade,
            destino_uf=cotacao_original.destino_uf,
            destino_cep=cotacao_original.destino_cep,
            destino_logradouro=cotacao_original.destino_logradouro,
            tipo_carga=cotacao_original.tipo_carga,
            modal=cotacao_original.modal,
            peso_kg=cotacao_original.peso_kg,
            cubagem_m3=cotacao_original.cubagem_m3,
            quantidade_volumes=cotacao_original.quantidade_volumes,
            valor_mercadoria=cotacao_original.valor_mercadoria,
            prazo_estimado=cotacao_original.prazo_estimado,
            valor_frete=cotacao_original.valor_frete,
            valor_seguro=cotacao_original.valor_seguro,
            valor_adicional=cotacao_original.valor_adicional,
            status="rascunho",
            urgente=cotacao_original.urgente,
            observacoes=cotacao_original.observacoes,
            tenant_id=tenant_id
        )
        
        db.add(nova_cotacao)
        db.commit()
        db.refresh(nova_cotacao)
        
        logger.info(f"✅ Cotação duplicada: {cotacao_original.numero} -> {novo_numero}")
        
        return {
            "success": True,
            "message": "Cotação duplicada com sucesso",
            "data": nova_cotacao
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao duplicar cotação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{cotacao_id}")
async def excluir_cotacao(
    cotacao_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Exclui uma cotação (apenas rascunhos)"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        cotacao = db.query(Cotacao).filter(
            Cotacao.id == cotacao_id,
            Cotacao.tenant_id == tenant_id
        ).first()
        
        if not cotacao:
            raise HTTPException(status_code=404, detail="Cotação não encontrada")
        
        if cotacao.status != "rascunho":
            raise HTTPException(
                status_code=400,
                detail="Apenas cotações em rascunho podem ser excluídas"
            )
        
        db.delete(cotacao)
        db.commit()
        
        logger.info(f"✅ Cotação excluída: {cotacao.numero}")
        
        return {
            "success": True,
            "message": "Cotação excluída com sucesso"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao excluir cotação: {e}")
        raise HTTPException(status_code=500, detail=str(e))
