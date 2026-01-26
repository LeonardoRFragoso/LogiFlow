"""
Router de Cotações - API REST usando Clean Architecture
"""
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from infrastructure.persistence.database import get_db
from infrastructure.repositories.cliente_repository import ClienteRepository
from infrastructure.repositories.cotacao_repository import CotacaoRepository
from application.dtos.cotacao_dto import CotacaoCreateDTO, CotacaoResponseDTO
from application.use_cases.cotacao_use_cases import (
    CriarCotacaoUseCase,
    EnviarCotacaoUseCase,
    AprovarCotacaoUseCase,
)
from domain.entities.cotacao import StatusCotacao
from domain.exceptions import EntityNotFoundException, BusinessRuleException, ValidationException


router = APIRouter(prefix="/v2/cotacoes", tags=["Cotações v2"])


def get_cotacao_repository(db: Session = Depends(get_db)) -> CotacaoRepository:
    return CotacaoRepository(db)


def get_cliente_repository(db: Session = Depends(get_db)) -> ClienteRepository:
    return ClienteRepository(db)


@router.get(
    "/",
    response_model=dict,
    summary="Listar cotações",
    description="Lista todas as cotações com paginação e filtros"
)
async def listar_cotacoes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    cliente_id: Optional[UUID] = Query(None, description="Filtrar por cliente"),
    repo: CotacaoRepository = Depends(get_cotacao_repository)
):
    """Lista cotações com paginação e filtros"""
    if cliente_id:
        cotacoes = await repo.get_by_cliente(cliente_id, skip, limit)
    elif status:
        try:
            status_enum = StatusCotacao(status)
            cotacoes = await repo.get_by_status(status_enum, skip, limit)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Status inválido. Valores permitidos: {[s.value for s in StatusCotacao]}"
            )
    else:
        cotacoes = await repo.get_all(skip, limit)
    
    total = await repo.count()
    
    # Converter entidades para response (simplificado)
    data = []
    for cot in cotacoes:
        data.append({
            "id": str(cot.id),
            "numero": cot.numero,
            "cliente_id": str(cot.cliente_id),
            "status": cot.status.value,
            "tipo_frete": cot.tipo_frete.value,
            "tipo_carga": cot.tipo_carga.value,
            "valor_total": float(cot.valor_total),
            "peso_total": float(cot.peso_total),
            "validade": cot.validade.isoformat() if cot.validade else None,
            "created_at": cot.created_at.isoformat(),
        })
    
    return {
        "data": data,
        "pagination": {"skip": skip, "limit": limit, "total": total}
    }


@router.get(
    "/{cotacao_id}",
    summary="Buscar cotação por ID",
    responses={404: {"description": "Cotação não encontrada"}}
)
async def buscar_cotacao(
    cotacao_id: UUID,
    repo: CotacaoRepository = Depends(get_cotacao_repository)
):
    """Retorna detalhes de uma cotação específica"""
    cotacao = await repo.get_by_id(cotacao_id)
    
    if not cotacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cotação não encontrada: {cotacao_id}"
        )
    
    return {
        "id": str(cotacao.id),
        "numero": cotacao.numero,
        "cliente_id": str(cotacao.cliente_id),
        "origem": {
            "logradouro": cotacao.origem.logradouro,
            "numero": cotacao.origem.numero,
            "bairro": cotacao.origem.bairro,
            "cidade": cotacao.origem.cidade,
            "uf": cotacao.origem.uf,
            "cep": cotacao.origem.cep,
        },
        "destino": {
            "logradouro": cotacao.destino.logradouro,
            "numero": cotacao.destino.numero,
            "bairro": cotacao.destino.bairro,
            "cidade": cotacao.destino.cidade,
            "uf": cotacao.destino.uf,
            "cep": cotacao.destino.cep,
        },
        "itens": [
            {
                "descricao": item.descricao,
                "quantidade": item.quantidade,
                "peso_kg": float(item.peso_kg),
                "volume_m3": float(item.volume_m3) if item.volume_m3 else None,
            }
            for item in cotacao.itens
        ],
        "tipo_frete": cotacao.tipo_frete.value,
        "tipo_carga": cotacao.tipo_carga.value,
        "status": cotacao.status.value,
        "valor_frete": float(cotacao.valor_frete),
        "valor_seguro": float(cotacao.valor_seguro),
        "valor_total": float(cotacao.valor_total),
        "peso_total": float(cotacao.peso_total),
        "volume_total": float(cotacao.volume_total),
        "validade": cotacao.validade.isoformat() if cotacao.validade else None,
        "observacoes": cotacao.observacoes,
        "created_at": cotacao.created_at.isoformat(),
        "updated_at": cotacao.updated_at.isoformat(),
    }


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova cotação",
    responses={
        400: {"description": "Dados inválidos"},
        404: {"description": "Cliente não encontrado"}
    }
)
async def criar_cotacao(
    dto: CotacaoCreateDTO,
    cotacao_repo: CotacaoRepository = Depends(get_cotacao_repository),
    cliente_repo: ClienteRepository = Depends(get_cliente_repository)
):
    """Cria uma nova cotação de frete"""
    use_case = CriarCotacaoUseCase(cotacao_repo, cliente_repo)
    
    try:
        result = await use_case.execute(dto)
        return result
    except EntityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )


@router.post(
    "/{cotacao_id}/enviar",
    summary="Enviar cotação para cliente",
    responses={
        400: {"description": "Operação não permitida"},
        404: {"description": "Cotação não encontrada"}
    }
)
async def enviar_cotacao(
    cotacao_id: UUID,
    repo: CotacaoRepository = Depends(get_cotacao_repository)
):
    """Envia a cotação para o cliente (muda status para 'enviada')"""
    use_case = EnviarCotacaoUseCase(repo)
    
    try:
        result = await use_case.execute(cotacao_id)
        return {"message": "Cotação enviada com sucesso", "cotacao": result}
    except EntityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
    except BusinessRuleException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )


@router.post(
    "/{cotacao_id}/aprovar",
    summary="Aprovar cotação",
    responses={
        400: {"description": "Operação não permitida"},
        404: {"description": "Cotação não encontrada"}
    }
)
async def aprovar_cotacao(
    cotacao_id: UUID,
    repo: CotacaoRepository = Depends(get_cotacao_repository)
):
    """Aprova a cotação (cliente aceitou)"""
    use_case = AprovarCotacaoUseCase(repo)
    
    try:
        result = await use_case.execute(cotacao_id)
        return {"message": "Cotação aprovada com sucesso", "cotacao": result}
    except EntityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
    except BusinessRuleException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )


@router.post(
    "/{cotacao_id}/rejeitar",
    summary="Rejeitar cotação",
    responses={
        400: {"description": "Operação não permitida"},
        404: {"description": "Cotação não encontrada"}
    }
)
async def rejeitar_cotacao(
    cotacao_id: UUID,
    repo: CotacaoRepository = Depends(get_cotacao_repository)
):
    """Rejeita a cotação (cliente recusou)"""
    cotacao = await repo.get_by_id(cotacao_id)
    
    if not cotacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cotação não encontrada: {cotacao_id}"
        )
    
    try:
        cotacao.rejeitar()
        await repo.update(cotacao)
        return {"message": "Cotação rejeitada", "status": cotacao.status.value}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/expiradas/",
    summary="Listar cotações expiradas",
)
async def listar_expiradas(
    repo: CotacaoRepository = Depends(get_cotacao_repository)
):
    """Lista todas as cotações que expiraram"""
    cotacoes = await repo.get_expiradas()
    
    return {
        "data": [
            {
                "id": str(c.id),
                "numero": c.numero,
                "cliente_id": str(c.cliente_id),
                "validade": c.validade.isoformat() if c.validade else None,
                "valor_total": float(c.valor_total),
            }
            for c in cotacoes
        ],
        "total": len(cotacoes)
    }
