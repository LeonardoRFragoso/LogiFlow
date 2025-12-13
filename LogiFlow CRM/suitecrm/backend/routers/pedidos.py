"""
LogiFlow CRM - Pedidos de Frete Router
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal
from enum import Enum

router = APIRouter()


class StatusOperacional(str, Enum):
    EM_PLANEJAMENTO = "em_planejamento"
    AGUARDANDO_COLETA = "aguardando_coleta"
    EM_COLETA = "em_coleta"
    EM_TRANSITO = "em_transito"
    EM_ENTREGA = "em_entrega"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"


class SLAStatus(str, Enum):
    VERDE = "verde"  # No prazo
    AMARELO = "amarelo"  # Atenção
    VERMELHO = "vermelho"  # Atrasado


class PedidoResponse(BaseModel):
    id: str
    numero_pedido: str
    data_pedido: date
    cliente_id: str
    cliente_nome: str
    cotacao_id: Optional[str]
    valor_contratado: Decimal
    motorista_id: Optional[str]
    motorista_nome: Optional[str]
    veiculo_id: Optional[str]
    veiculo_placa: Optional[str]
    status_operacional: StatusOperacional
    previsao_entrega: date
    data_entrega_real: Optional[date]
    sla_status: SLAStatus
    origem: str
    destino: str


class PedidoList(BaseModel):
    total: int
    page: int
    items: List[PedidoResponse]


class AtribuirMotorista(BaseModel):
    motorista_id: str
    veiculo_id: str
    previsao_coleta: datetime


@router.get("/", response_model=PedidoList)
async def listar_pedidos(
    request: Request,
    page: int = 1,
    status: Optional[StatusOperacional] = None,
    motorista_id: Optional[str] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None
):
    """Lista pedidos com filtros"""
    suitecrm = request.app.state.suitecrm
    
    try:
        result = await suitecrm.listar_pedidos(
            page=page,
            status=status.value if status else None
        )
        return PedidoList(total=0, page=page, items=[])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard")
async def dashboard_operacional(request: Request):
    """Retorna métricas para dashboard operacional"""
    # TODO: Implementar queries de dashboard
    return {
        "em_transito": 0,
        "entregas_hoje": 0,
        "atrasados": 0,
        "sla": {
            "verde": 0,
            "amarelo": 0,
            "vermelho": 0
        },
        "entregas_semana": [],
        "top_motoristas": []
    }


@router.get("/{pedido_id}", response_model=PedidoResponse)
async def obter_pedido(request: Request, pedido_id: str):
    """Obtém detalhes de um pedido"""
    raise HTTPException(status_code=404, detail="Pedido não encontrado")


@router.patch("/{pedido_id}/atribuir")
async def atribuir_motorista(
    request: Request,
    pedido_id: str,
    dados: AtribuirMotorista
):
    """Atribui motorista e veículo ao pedido"""
    suitecrm = request.app.state.suitecrm
    
    try:
        await suitecrm.update_record("PedidosFrete", pedido_id, {
            "motorista_id": dados.motorista_id,
            "veiculo_id": dados.veiculo_id,
            "status_operacional": "Aguardando Coleta"
        })
        
        return {
            "message": "Motorista atribuído com sucesso",
            "pedido_id": pedido_id,
            "motorista_id": dados.motorista_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{pedido_id}/status")
async def atualizar_status(
    request: Request,
    pedido_id: str,
    novo_status: StatusOperacional,
    observacao: Optional[str] = None
):
    """Atualiza status operacional do pedido"""
    suitecrm = request.app.state.suitecrm
    
    try:
        attributes = {"status_operacional": novo_status.value}
        
        if novo_status == StatusOperacional.ENTREGUE:
            attributes["data_entrega_real"] = datetime.now().isoformat()
        
        await suitecrm.update_record("PedidosFrete", pedido_id, attributes)
        
        return {
            "message": f"Status atualizado para {novo_status.value}",
            "pedido_id": pedido_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{pedido_id}/timeline")
async def timeline_pedido(request: Request, pedido_id: str):
    """Retorna timeline de eventos do pedido"""
    # TODO: Buscar eventos relacionados
    return {
        "pedido_id": pedido_id,
        "eventos": []
    }
