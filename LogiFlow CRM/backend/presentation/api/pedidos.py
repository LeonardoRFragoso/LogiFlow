"""
Router de Pedidos - API REST usando Clean Architecture
"""
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from infrastructure.persistence.database import get_db
from infrastructure.repositories.pedido_repository import PedidoRepository
from application.dtos.pedido_dto import PedidoCreateDTO, PedidoResponseDTO
from domain.entities.pedido import StatusPedido
from domain.exceptions import EntityNotFoundException, BusinessRuleException


router = APIRouter(prefix="/v2/pedidos", tags=["Pedidos v2"])


def get_pedido_repository(db: Session = Depends(get_db)) -> PedidoRepository:
    return PedidoRepository(db)


@router.get(
    "/",
    response_model=dict,
    summary="Listar pedidos",
    description="Lista todos os pedidos com paginação e filtros"
)
async def listar_pedidos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status_pedido: Optional[str] = Query(None, alias="status", description="Filtrar por status"),
    cliente_id: Optional[UUID] = Query(None, description="Filtrar por cliente"),
    motorista_id: Optional[UUID] = Query(None, description="Filtrar por motorista"),
    repo: PedidoRepository = Depends(get_pedido_repository)
):
    """Lista pedidos com paginação e filtros"""
    if cliente_id:
        pedidos = await repo.get_by_cliente(cliente_id, skip, limit)
    elif motorista_id:
        pedidos = await repo.get_by_motorista(motorista_id, skip, limit)
    elif status_pedido:
        try:
            status_enum = StatusPedido(status_pedido)
            pedidos = await repo.get_by_status(status_enum, skip, limit)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Status inválido. Valores permitidos: {[s.value for s in StatusPedido]}"
            )
    else:
        pedidos = await repo.get_all(skip, limit)
    
    total = await repo.count()
    
    data = []
    for ped in pedidos:
        data.append({
            "id": str(ped.id),
            "numero": ped.numero,
            "cliente_id": str(ped.cliente_id),
            "status": ped.status.value,
            "origem_cidade": ped.origem.cidade,
            "destino_cidade": ped.destino.cidade,
            "valor_total": float(ped.valor_total),
            "peso_kg": float(ped.peso_kg),
            "data_coleta_prevista": ped.data_coleta_prevista.isoformat() if ped.data_coleta_prevista else None,
            "data_entrega_prevista": ped.data_entrega_prevista.isoformat() if ped.data_entrega_prevista else None,
            "created_at": ped.created_at.isoformat(),
        })
    
    return {
        "data": data,
        "pagination": {"skip": skip, "limit": limit, "total": total}
    }


@router.get(
    "/em-transito",
    summary="Listar pedidos em trânsito",
)
async def listar_em_transito(
    repo: PedidoRepository = Depends(get_pedido_repository)
):
    """Lista todos os pedidos que estão em movimento"""
    pedidos = await repo.get_em_transito()
    
    return {
        "data": [
            {
                "id": str(p.id),
                "numero": p.numero,
                "status": p.status.value,
                "origem": f"{p.origem.cidade}/{p.origem.uf}",
                "destino": f"{p.destino.cidade}/{p.destino.uf}",
                "motorista_id": str(p.motorista_id) if p.motorista_id else None,
                "data_coleta": p.data_coleta_realizada.isoformat() if p.data_coleta_realizada else None,
            }
            for p in pedidos
        ],
        "total": len(pedidos)
    }


@router.get(
    "/{pedido_id}",
    summary="Buscar pedido por ID",
    responses={404: {"description": "Pedido não encontrado"}}
)
async def buscar_pedido(
    pedido_id: UUID,
    repo: PedidoRepository = Depends(get_pedido_repository)
):
    """Retorna detalhes de um pedido específico"""
    pedido = await repo.get_by_id(pedido_id)
    
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido não encontrado: {pedido_id}"
        )
    
    return {
        "id": str(pedido.id),
        "numero": pedido.numero,
        "cliente_id": str(pedido.cliente_id),
        "cotacao_id": str(pedido.cotacao_id) if pedido.cotacao_id else None,
        "origem": {
            "logradouro": pedido.origem.logradouro,
            "numero": pedido.origem.numero,
            "bairro": pedido.origem.bairro,
            "cidade": pedido.origem.cidade,
            "uf": pedido.origem.uf,
            "cep": pedido.origem.cep,
        },
        "destino": {
            "logradouro": pedido.destino.logradouro,
            "numero": pedido.destino.numero,
            "bairro": pedido.destino.bairro,
            "cidade": pedido.destino.cidade,
            "uf": pedido.destino.uf,
            "cep": pedido.destino.cep,
        },
        "status": pedido.status.value,
        "peso_kg": float(pedido.peso_kg),
        "volume_m3": float(pedido.volume_m3),
        "valor_mercadoria": float(pedido.valor_mercadoria),
        "descricao_carga": pedido.descricao_carga,
        "valor_frete": float(pedido.valor_frete),
        "valor_seguro": float(pedido.valor_seguro),
        "valor_total": float(pedido.valor_total),
        "motorista_id": str(pedido.motorista_id) if pedido.motorista_id else None,
        "veiculo_id": str(pedido.veiculo_id) if pedido.veiculo_id else None,
        "cte_numero": pedido.cte_numero,
        "cte_chave": pedido.cte_chave,
        "datas": {
            "coleta_prevista": pedido.data_coleta_prevista.isoformat() if pedido.data_coleta_prevista else None,
            "coleta_realizada": pedido.data_coleta_realizada.isoformat() if pedido.data_coleta_realizada else None,
            "entrega_prevista": pedido.data_entrega_prevista.isoformat() if pedido.data_entrega_prevista else None,
            "entrega_realizada": pedido.data_entrega_realizada.isoformat() if pedido.data_entrega_realizada else None,
        },
        "observacoes": pedido.observacoes,
        "created_at": pedido.created_at.isoformat(),
        "updated_at": pedido.updated_at.isoformat(),
    }


@router.post(
    "/{pedido_id}/coletar",
    summary="Registrar coleta do pedido",
    responses={
        400: {"description": "Operação não permitida"},
        404: {"description": "Pedido não encontrado"}
    }
)
async def coletar_pedido(
    pedido_id: UUID,
    repo: PedidoRepository = Depends(get_pedido_repository)
):
    """Registra que o pedido foi coletado"""
    pedido = await repo.get_by_id(pedido_id)
    
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido não encontrado: {pedido_id}"
        )
    
    try:
        pedido.coletar()
        await repo.update(pedido)
        return {
            "message": "Pedido coletado com sucesso",
            "status": pedido.status.value,
            "data_coleta": pedido.data_coleta_realizada.isoformat()
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/{pedido_id}/iniciar-transporte",
    summary="Iniciar transporte do pedido",
)
async def iniciar_transporte(
    pedido_id: UUID,
    repo: PedidoRepository = Depends(get_pedido_repository)
):
    """Marca o pedido como em trânsito"""
    pedido = await repo.get_by_id(pedido_id)
    
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido não encontrado: {pedido_id}"
        )
    
    try:
        pedido.iniciar_transporte()
        await repo.update(pedido)
        return {"message": "Transporte iniciado", "status": pedido.status.value}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/{pedido_id}/sair-entrega",
    summary="Marcar saída para entrega",
)
async def sair_para_entrega(
    pedido_id: UUID,
    repo: PedidoRepository = Depends(get_pedido_repository)
):
    """Marca que o pedido saiu para entrega final"""
    pedido = await repo.get_by_id(pedido_id)
    
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido não encontrado: {pedido_id}"
        )
    
    try:
        pedido.sair_para_entrega()
        await repo.update(pedido)
        return {"message": "Saiu para entrega", "status": pedido.status.value}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/{pedido_id}/entregar",
    summary="Registrar entrega do pedido",
)
async def entregar_pedido(
    pedido_id: UUID,
    repo: PedidoRepository = Depends(get_pedido_repository)
):
    """Registra que o pedido foi entregue"""
    pedido = await repo.get_by_id(pedido_id)
    
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido não encontrado: {pedido_id}"
        )
    
    try:
        pedido.entregar()
        await repo.update(pedido)
        return {
            "message": "Pedido entregue com sucesso",
            "status": pedido.status.value,
            "data_entrega": pedido.data_entrega_realizada.isoformat()
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/{pedido_id}/cancelar",
    summary="Cancelar pedido",
)
async def cancelar_pedido(
    pedido_id: UUID,
    motivo: Optional[str] = Query(None, description="Motivo do cancelamento"),
    repo: PedidoRepository = Depends(get_pedido_repository)
):
    """Cancela o pedido"""
    pedido = await repo.get_by_id(pedido_id)
    
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido não encontrado: {pedido_id}"
        )
    
    try:
        pedido.cancelar(motivo)
        await repo.update(pedido)
        return {"message": "Pedido cancelado", "status": pedido.status.value}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch(
    "/{pedido_id}/atribuir-motorista",
    summary="Atribuir motorista ao pedido",
)
async def atribuir_motorista(
    pedido_id: UUID,
    motorista_id: UUID,
    veiculo_id: UUID,
    repo: PedidoRepository = Depends(get_pedido_repository)
):
    """Atribui um motorista e veículo ao pedido"""
    pedido = await repo.get_by_id(pedido_id)
    
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido não encontrado: {pedido_id}"
        )
    
    pedido.atribuir_motorista(motorista_id, veiculo_id)
    await repo.update(pedido)
    
    return {
        "message": "Motorista atribuído",
        "motorista_id": str(motorista_id),
        "veiculo_id": str(veiculo_id)
    }
