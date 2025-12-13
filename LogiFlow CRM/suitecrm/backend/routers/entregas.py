"""
LogiFlow CRM - Entregas Router
"""

from fastapi import APIRouter, HTTPException, Request, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

router = APIRouter()


class EntregaStatus(str, Enum):
    AGUARDANDO = "aguardando"
    EM_ROTA = "em_rota"
    CHEGOU_DESTINO = "chegou_destino"
    ENTREGUE = "entregue"
    TENTATIVA_FALHA = "tentativa_falha"
    DEVOLVIDO = "devolvido"


class AtualizarPosicao(BaseModel):
    latitude: float
    longitude: float
    status: Optional[EntregaStatus] = None
    observacao: Optional[str] = None


class EntregaResponse(BaseModel):
    id: str
    pedido_id: str
    numero_pedido: str
    status: EntregaStatus
    local_atual: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    ultimo_evento: Optional[str]
    data_evento: Optional[datetime]
    previsao_entrega: datetime
    destinatario: str
    endereco_entrega: str


class EventoEntrega(BaseModel):
    timestamp: datetime
    status: str
    local: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    observacao: Optional[str]
    foto_url: Optional[str]


@router.get("/ativas")
async def listar_entregas_ativas(request: Request):
    """Lista entregas em andamento (para mapa)"""
    # TODO: Implementar busca
    return {
        "total": 0,
        "entregas": []
    }


@router.get("/{entrega_id}", response_model=EntregaResponse)
async def obter_entrega(request: Request, entrega_id: str):
    """Obtém detalhes de uma entrega"""
    raise HTTPException(status_code=404, detail="Entrega não encontrada")


@router.get("/{entrega_id}/rastreio")
async def rastreio_entrega(request: Request, entrega_id: str):
    """Retorna histórico de rastreio da entrega (público)"""
    # TODO: Implementar rastreio
    return {
        "entrega_id": entrega_id,
        "status_atual": "em_rota",
        "previsao": None,
        "eventos": []
    }


@router.post("/{entrega_id}/posicao")
async def atualizar_posicao(
    request: Request,
    entrega_id: str,
    dados: AtualizarPosicao
):
    """
    Atualiza posição da entrega (chamado pelo app do motorista)
    """
    suitecrm = request.app.state.suitecrm
    
    try:
        attributes = {
            "latitude": dados.latitude,
            "longitude": dados.longitude,
            "data_evento": datetime.now().isoformat()
        }
        
        if dados.status:
            attributes["status"] = dados.status.value
        
        if dados.observacao:
            attributes["ultimo_evento"] = dados.observacao
        
        await suitecrm.update_record("Entregas", entrega_id, attributes)
        
        return {"message": "Posição atualizada", "entrega_id": entrega_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{entrega_id}/comprovante")
async def enviar_comprovante(
    request: Request,
    entrega_id: str,
    foto: UploadFile = File(...),
    assinatura: Optional[UploadFile] = File(None),
    recebedor: Optional[str] = None,
    documento: Optional[str] = None
):
    """
    Envia comprovante de entrega (foto + assinatura)
    """
    # TODO: Implementar upload para S3 e registro
    
    return {
        "message": "Comprovante recebido",
        "entrega_id": entrega_id,
        "foto_url": None,
        "assinatura_url": None
    }


@router.patch("/{entrega_id}/finalizar")
async def finalizar_entrega(
    request: Request,
    entrega_id: str,
    sucesso: bool = True,
    observacao: Optional[str] = None
):
    """Finaliza a entrega"""
    suitecrm = request.app.state.suitecrm
    
    status = "Entregue" if sucesso else "Tentativa Falha"
    
    try:
        await suitecrm.atualizar_status_entrega(
            entrega_id,
            status=status,
            local=observacao
        )
        
        return {
            "message": f"Entrega finalizada: {status}",
            "entrega_id": entrega_id,
            "sucesso": sucesso
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
