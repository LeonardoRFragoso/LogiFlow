"""
LogiFlow CRM - Router Cotações
Endpoints para gestão de cotações de frete
"""

from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date
from enum import Enum
from decimal import Decimal
import logging
import uuid

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
# Schemas
# ========================================

class EnderecoSchema(BaseModel):
    cep: str
    logradouro: str
    numero: str
    complemento: Optional[str] = None
    bairro: str
    cidade: str
    uf: str = Field(..., max_length=2)
    
    @validator('uf')
    def uf_uppercase(cls, v):
        return v.upper()


class ItemCotacao(BaseModel):
    descricao: str
    quantidade: int = Field(..., ge=1)
    peso_kg: float = Field(..., gt=0)
    volume_m3: Optional[float] = None
    valor_mercadoria: Optional[float] = None
    observacao: Optional[str] = None


class CriarCotacaoRequest(BaseModel):
    cliente_id: str = Field(..., description="ID do cliente no SuiteCRM")
    cliente_nome: Optional[str] = None
    
    origem: EnderecoSchema
    destino: EnderecoSchema
    
    tipo_frete: TipoFrete = TipoFrete.CIF
    tipo_carga: TipoCarga = TipoCarga.FRACIONADA
    modal: ModalTransporte = ModalTransporte.RODOVIARIO
    
    itens: List[ItemCotacao] = Field(..., min_items=1)
    
    peso_total_kg: Optional[float] = None
    volume_total_m3: Optional[float] = None
    valor_mercadoria: Optional[float] = None
    
    data_coleta_desejada: Optional[date] = None
    urgente: bool = False
    
    observacoes: Optional[str] = None
    
    # Valores (podem ser calculados automaticamente)
    valor_frete: Optional[float] = None
    valor_seguro: Optional[float] = None
    valor_pedagio: Optional[float] = None
    valor_outros: Optional[float] = None
    desconto: Optional[float] = None
    valor_total: Optional[float] = None


class AtualizarCotacaoRequest(BaseModel):
    cliente_id: Optional[str] = None
    origem: Optional[EnderecoSchema] = None
    destino: Optional[EnderecoSchema] = None
    tipo_frete: Optional[TipoFrete] = None
    tipo_carga: Optional[TipoCarga] = None
    modal: Optional[ModalTransporte] = None
    itens: Optional[List[ItemCotacao]] = None
    peso_total_kg: Optional[float] = None
    volume_total_m3: Optional[float] = None
    valor_mercadoria: Optional[float] = None
    data_coleta_desejada: Optional[date] = None
    urgente: Optional[bool] = None
    observacoes: Optional[str] = None
    valor_frete: Optional[float] = None
    valor_seguro: Optional[float] = None
    valor_pedagio: Optional[float] = None
    valor_outros: Optional[float] = None
    desconto: Optional[float] = None
    valor_total: Optional[float] = None


class AprovarCotacaoRequest(BaseModel):
    observacao: Optional[str] = None
    criar_pedido: bool = True


class RejeitarCotacaoRequest(BaseModel):
    motivo: str = Field(..., min_length=5)


class CotacaoResponse(BaseModel):
    id: str
    numero: str
    cliente_id: str
    cliente_nome: Optional[str]
    status: StatusCotacao
    origem: EnderecoSchema
    destino: EnderecoSchema
    tipo_frete: TipoFrete
    tipo_carga: TipoCarga
    modal: ModalTransporte
    itens: List[ItemCotacao]
    peso_total_kg: float
    volume_total_m3: Optional[float]
    valor_mercadoria: Optional[float]
    data_coleta_desejada: Optional[date]
    urgente: bool
    observacoes: Optional[str]
    valor_frete: float
    valor_seguro: float
    valor_pedagio: float
    valor_outros: float
    desconto: float
    valor_total: float
    validade: date
    criado_em: datetime
    atualizado_em: datetime
    criado_por: Optional[str]


# ========================================
# Storage Simulado (substituir por SuiteCRM API)
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
    status: Optional[StatusCotacao] = None,
    cliente_id: Optional[str] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    urgente: Optional[bool] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100)
):
    """Lista cotações com filtros opcionais"""
    try:
        cotacoes = list(cotacoes_db.values())
        
        # Aplicar filtros
        if status:
            cotacoes = [c for c in cotacoes if c["status"] == status.value]
        if cliente_id:
            cotacoes = [c for c in cotacoes if c["cliente_id"] == cliente_id]
        if urgente is not None:
            cotacoes = [c for c in cotacoes if c["urgente"] == urgente]
        if data_inicio:
            cotacoes = [c for c in cotacoes if c["criado_em"].date() >= data_inicio]
        if data_fim:
            cotacoes = [c for c in cotacoes if c["criado_em"].date() <= data_fim]
        
        # Ordenar por data (mais recentes primeiro)
        cotacoes.sort(key=lambda x: x["criado_em"], reverse=True)
        
        # Paginação
        total = len(cotacoes)
        start = (page - 1) * per_page
        end = start + per_page
        cotacoes_paginadas = cotacoes[start:end]
        
        return {
            "success": True,
            "data": cotacoes_paginadas,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "pages": (total + per_page - 1) // per_page
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar cotações: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/estatisticas")
async def estatisticas_cotacoes():
    """Retorna estatísticas das cotações"""
    try:
        cotacoes = list(cotacoes_db.values())
        
        total = len(cotacoes)
        por_status = {}
        valor_total = 0
        
        for c in cotacoes:
            status = c["status"]
            por_status[status] = por_status.get(status, 0) + 1
            if c["status"] in ["aprovada", "convertida"]:
                valor_total += c.get("valor_total", 0)
        
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
        logger.error(f"Erro ao gerar estatísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{cotacao_id}")
async def obter_cotacao(cotacao_id: str = Path(...)):
    """Obtém detalhes de uma cotação"""
    try:
        if cotacao_id not in cotacoes_db:
            raise HTTPException(status_code=404, detail="Cotação não encontrada")
        
        return {
            "success": True,
            "data": cotacoes_db[cotacao_id]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter cotação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("")
async def criar_cotacao(request: CriarCotacaoRequest):
    """Cria uma nova cotação"""
    try:
        cotacao_id = str(uuid.uuid4())
        numero = gerar_numero_cotacao()
        now = datetime.utcnow()
        
        # Calcular totais
        peso_total = request.peso_total_kg or sum(item.peso_kg * item.quantidade for item in request.itens)
        volume_total = request.volume_total_m3
        
        # Calcular valor total
        valor_frete = request.valor_frete or 0
        valor_seguro = request.valor_seguro or 0
        valor_pedagio = request.valor_pedagio or 0
        valor_outros = request.valor_outros or 0
        desconto = request.desconto or 0
        valor_total = request.valor_total or (valor_frete + valor_seguro + valor_pedagio + valor_outros - desconto)
        
        cotacao = {
            "id": cotacao_id,
            "numero": numero,
            "cliente_id": request.cliente_id,
            "cliente_nome": request.cliente_nome,
            "status": StatusCotacao.RASCUNHO.value,
            "origem": request.origem.dict(),
            "destino": request.destino.dict(),
            "tipo_frete": request.tipo_frete.value,
            "tipo_carga": request.tipo_carga.value,
            "modal": request.modal.value,
            "itens": [item.dict() for item in request.itens],
            "peso_total_kg": peso_total,
            "volume_total_m3": volume_total,
            "valor_mercadoria": request.valor_mercadoria,
            "data_coleta_desejada": request.data_coleta_desejada.isoformat() if request.data_coleta_desejada else None,
            "urgente": request.urgente,
            "observacoes": request.observacoes,
            "valor_frete": valor_frete,
            "valor_seguro": valor_seguro,
            "valor_pedagio": valor_pedagio,
            "valor_outros": valor_outros,
            "desconto": desconto,
            "valor_total": valor_total,
            "validade": (now + timedelta(days=15)).date().isoformat(),
            "criado_em": now,
            "atualizado_em": now,
            "criado_por": None  # TODO: pegar do token JWT
        }
        
        cotacoes_db[cotacao_id] = cotacao
        
        logger.info(f"Cotação criada: {numero}")
        
        return {
            "success": True,
            "message": "Cotação criada com sucesso",
            "data": cotacao
        }
        
    except Exception as e:
        logger.error(f"Erro ao criar cotação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{cotacao_id}")
async def atualizar_cotacao(
    cotacao_id: str,
    request: AtualizarCotacaoRequest
):
    """Atualiza uma cotação existente"""
    try:
        if cotacao_id not in cotacoes_db:
            raise HTTPException(status_code=404, detail="Cotação não encontrada")
        
        cotacao = cotacoes_db[cotacao_id]
        
        # Só permite editar cotações em rascunho ou enviada
        if cotacao["status"] not in [StatusCotacao.RASCUNHO.value, StatusCotacao.ENVIADA.value]:
            raise HTTPException(
                status_code=400,
                detail=f"Não é possível editar cotação com status '{cotacao['status']}'"
            )
        
        # Atualizar campos fornecidos
        update_data = request.dict(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                if hasattr(value, 'dict'):
                    cotacao[key] = value.dict()
                elif hasattr(value, 'value'):
                    cotacao[key] = value.value
                elif isinstance(value, list):
                    cotacao[key] = [item.dict() if hasattr(item, 'dict') else item for item in value]
                elif isinstance(value, date):
                    cotacao[key] = value.isoformat()
                else:
                    cotacao[key] = value
        
        cotacao["atualizado_em"] = datetime.utcnow()
        
        return {
            "success": True,
            "message": "Cotação atualizada com sucesso",
            "data": cotacao
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar cotação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{cotacao_id}/enviar")
async def enviar_cotacao(cotacao_id: str):
    """Envia cotação para o cliente"""
    try:
        if cotacao_id not in cotacoes_db:
            raise HTTPException(status_code=404, detail="Cotação não encontrada")
        
        cotacao = cotacoes_db[cotacao_id]
        
        if cotacao["status"] != StatusCotacao.RASCUNHO.value:
            raise HTTPException(
                status_code=400,
                detail="Apenas cotações em rascunho podem ser enviadas"
            )
        
        cotacao["status"] = StatusCotacao.ENVIADA.value
        cotacao["atualizado_em"] = datetime.utcnow()
        cotacao["enviada_em"] = datetime.utcnow()
        
        # TODO: Enviar email/WhatsApp para cliente
        
        logger.info(f"Cotação enviada: {cotacao['numero']}")
        
        return {
            "success": True,
            "message": "Cotação enviada com sucesso",
            "data": cotacao
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao enviar cotação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{cotacao_id}/aprovar")
async def aprovar_cotacao(
    cotacao_id: str,
    request: AprovarCotacaoRequest
):
    """Aprova uma cotação e opcionalmente cria pedido"""
    try:
        if cotacao_id not in cotacoes_db:
            raise HTTPException(status_code=404, detail="Cotação não encontrada")
        
        cotacao = cotacoes_db[cotacao_id]
        
        if cotacao["status"] not in [StatusCotacao.ENVIADA.value, StatusCotacao.EM_ANALISE.value]:
            raise HTTPException(
                status_code=400,
                detail="Apenas cotações enviadas ou em análise podem ser aprovadas"
            )
        
        cotacao["status"] = StatusCotacao.APROVADA.value
        cotacao["atualizado_em"] = datetime.utcnow()
        cotacao["aprovada_em"] = datetime.utcnow()
        cotacao["observacao_aprovacao"] = request.observacao
        
        pedido_id = None
        if request.criar_pedido:
            # TODO: Chamar router de pedidos para criar
            cotacao["status"] = StatusCotacao.CONVERTIDA.value
            pedido_id = str(uuid.uuid4())  # Simulado
            cotacao["pedido_id"] = pedido_id
        
        logger.info(f"Cotação aprovada: {cotacao['numero']}")
        
        return {
            "success": True,
            "message": "Cotação aprovada com sucesso",
            "data": {
                "cotacao": cotacao,
                "pedido_id": pedido_id
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao aprovar cotação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{cotacao_id}/rejeitar")
async def rejeitar_cotacao(
    cotacao_id: str,
    request: RejeitarCotacaoRequest
):
    """Rejeita uma cotação"""
    try:
        if cotacao_id not in cotacoes_db:
            raise HTTPException(status_code=404, detail="Cotação não encontrada")
        
        cotacao = cotacoes_db[cotacao_id]
        
        if cotacao["status"] in [StatusCotacao.CONVERTIDA.value, StatusCotacao.REJEITADA.value]:
            raise HTTPException(
                status_code=400,
                detail=f"Não é possível rejeitar cotação com status '{cotacao['status']}'"
            )
        
        cotacao["status"] = StatusCotacao.REJEITADA.value
        cotacao["atualizado_em"] = datetime.utcnow()
        cotacao["rejeitada_em"] = datetime.utcnow()
        cotacao["motivo_rejeicao"] = request.motivo
        
        logger.info(f"Cotação rejeitada: {cotacao['numero']}")
        
        return {
            "success": True,
            "message": "Cotação rejeitada",
            "data": cotacao
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao rejeitar cotação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{cotacao_id}/duplicar")
async def duplicar_cotacao(cotacao_id: str):
    """Cria cópia de uma cotação"""
    try:
        if cotacao_id not in cotacoes_db:
            raise HTTPException(status_code=404, detail="Cotação não encontrada")
        
        cotacao_original = cotacoes_db[cotacao_id]
        
        nova_cotacao_id = str(uuid.uuid4())
        novo_numero = gerar_numero_cotacao()
        now = datetime.utcnow()
        
        nova_cotacao = {
            **cotacao_original,
            "id": nova_cotacao_id,
            "numero": novo_numero,
            "status": StatusCotacao.RASCUNHO.value,
            "criado_em": now,
            "atualizado_em": now,
            "validade": (now + timedelta(days=15)).date().isoformat(),
            "cotacao_origem_id": cotacao_id
        }
        
        # Remover campos específicos da cotação original
        for key in ["enviada_em", "aprovada_em", "rejeitada_em", "pedido_id", 
                    "motivo_rejeicao", "observacao_aprovacao"]:
            nova_cotacao.pop(key, None)
        
        cotacoes_db[nova_cotacao_id] = nova_cotacao
        
        logger.info(f"Cotação duplicada: {cotacao_original['numero']} -> {novo_numero}")
        
        return {
            "success": True,
            "message": "Cotação duplicada com sucesso",
            "data": nova_cotacao
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao duplicar cotação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{cotacao_id}")
async def excluir_cotacao(cotacao_id: str):
    """Exclui uma cotação (apenas rascunhos)"""
    try:
        if cotacao_id not in cotacoes_db:
            raise HTTPException(status_code=404, detail="Cotação não encontrada")
        
        cotacao = cotacoes_db[cotacao_id]
        
        if cotacao["status"] != StatusCotacao.RASCUNHO.value:
            raise HTTPException(
                status_code=400,
                detail="Apenas cotações em rascunho podem ser excluídas"
            )
        
        del cotacoes_db[cotacao_id]
        
        logger.info(f"Cotação excluída: {cotacao['numero']}")
        
        return {
            "success": True,
            "message": "Cotação excluída com sucesso"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao excluir cotação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Import necessário
from datetime import timedelta
