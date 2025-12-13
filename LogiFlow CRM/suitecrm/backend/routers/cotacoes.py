"""
LogiFlow CRM - Cotações Router
Orquestra chamadas para SuiteCRM API V8
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from decimal import Decimal
from enum import Enum

from integrations.suitecrm import SuiteCRMMapper

router = APIRouter()


class ModalType(str, Enum):
    RODOVIARIO = "rodoviario"
    AEREO = "aereo"
    MARITIMO = "maritimo"
    FERROVIARIO = "ferroviario"


class CargaType(str, Enum):
    GERAL = "geral"
    FRACIONADA = "fracionada"
    LOTACAO = "lotacao"
    CONTAINER = "container"
    GRANEL = "granel"
    REFRIGERADA = "refrigerada"


class CotacaoStatus(str, Enum):
    ABERTA = "aberta"
    APROVADA = "aprovada"
    PERDIDA = "perdida"
    EXPIRADA = "expirada"


class CotacaoCreate(BaseModel):
    cliente_id: str
    origem: str
    destino: str
    tipo_carga: CargaType
    peso_kg: Decimal
    cubagem_m3: Optional[Decimal] = None
    modal: ModalType = ModalType.RODOVIARIO
    prazo_estimado: int  # dias
    valor_proposta: Decimal
    validade: date
    observacoes: Optional[str] = None


class CotacaoResponse(BaseModel):
    id: str
    numero: str
    cliente_id: str
    cliente_nome: str
    origem: str
    destino: str
    tipo_carga: CargaType
    peso_kg: Decimal
    cubagem_m3: Optional[Decimal]
    modal: ModalType
    prazo_estimado: int
    valor_proposta: Decimal
    validade: date
    status: CotacaoStatus
    observacoes: Optional[str]
    created_at: str
    updated_at: str


class CotacaoList(BaseModel):
    total: int
    page: int
    items: List[CotacaoResponse]


@router.get("/", response_model=CotacaoList)
async def listar_cotacoes(
    request: Request,
    page: int = 1,
    cliente_id: Optional[str] = None,
    status: Optional[CotacaoStatus] = None
):
    """Lista cotações com filtros"""
    suitecrm = request.app.state.suitecrm
    
    try:
        filters = {}
        if cliente_id:
            filters["cliente_id"] = cliente_id
        if status:
            filters["status"] = status.value
        
        result = await suitecrm.list_records("Cotacoes", page=page, filters=filters if filters else None)
        
        items = []
        for record in result.get("data", []):
            mapped = SuiteCRMMapper.cotacao_from_suitecrm(record)
            items.append(CotacaoResponse(**mapped))
        
        meta = result.get("meta", {})
        total = meta.get("total-records", len(items))
        
        return CotacaoList(total=total, page=page, items=items)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{cotacao_id}", response_model=CotacaoResponse)
async def obter_cotacao(request: Request, cotacao_id: str):
    """Obtém detalhes de uma cotação"""
    suitecrm = request.app.state.suitecrm
    
    try:
        result = await suitecrm.get_record("Cotacoes", cotacao_id)
        
        if not result.get("data"):
            raise HTTPException(status_code=404, detail="Cotação não encontrada")
        
        mapped = SuiteCRMMapper.cotacao_from_suitecrm(result["data"])
        return CotacaoResponse(**mapped)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=CotacaoResponse)
async def criar_cotacao(request: Request, cotacao: CotacaoCreate):
    """Cria nova cotação"""
    suitecrm = request.app.state.suitecrm
    
    try:
        # Converter dados para formato SuiteCRM
        dados = SuiteCRMMapper.cotacao_to_suitecrm(cotacao.model_dump())
        
        result = await suitecrm.create_record("Cotacoes", dados)
        
        if not result.get("data"):
            raise HTTPException(status_code=500, detail="Erro ao criar cotação")
        
        mapped = SuiteCRMMapper.cotacao_from_suitecrm(result["data"])
        return CotacaoResponse(**mapped)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{cotacao_id}/aprovar")
async def aprovar_cotacao(request: Request, cotacao_id: str):
    """
    Aprova cotação e cria pedido automaticamente
    
    Fluxo:
    1. Atualiza status para 'aprovada'
    2. Logic hook do SuiteCRM cria o pedido
    3. Retorna dados do pedido criado
    """
    suitecrm = request.app.state.suitecrm
    
    try:
        # Atualizar status
        await suitecrm.update_record("Cotacoes", cotacao_id, {"status": "Aprovada"})
        
        return {
            "message": "Cotação aprovada com sucesso",
            "cotacao_id": cotacao_id,
            "pedido_criado": True  # Logic hook cria automaticamente
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{cotacao_id}/perder")
async def marcar_perdida(
    request: Request,
    cotacao_id: str,
    motivo: Optional[str] = None
):
    """Marca cotação como perdida"""
    suitecrm = request.app.state.suitecrm
    
    try:
        attributes = {"status": "Perdida"}
        if motivo:
            attributes["motivo_perda"] = motivo
        
        await suitecrm.update_record("Cotacoes", cotacao_id, attributes)
        
        return {"message": "Cotação marcada como perdida", "cotacao_id": cotacao_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
