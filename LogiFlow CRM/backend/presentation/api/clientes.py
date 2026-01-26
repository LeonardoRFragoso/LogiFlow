"""
Router de Clientes - API REST usando Clean Architecture
"""
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from infrastructure.persistence.database import get_db
from infrastructure.repositories.cliente_repository import ClienteRepository
from application.dtos.cliente_dto import (
    ClienteCreateDTO,
    ClienteUpdateDTO,
    ClienteResponseDTO,
)
from application.use_cases.cliente_use_cases import (
    CriarClienteUseCase,
    AtualizarClienteUseCase,
    BuscarClienteUseCase,
    ListarClientesUseCase,
)
from domain.exceptions import EntityNotFoundException, ValidationException


router = APIRouter(prefix="/v2/clientes", tags=["Clientes v2"])


def get_cliente_repository(db: Session = Depends(get_db)) -> ClienteRepository:
    """Dependency: Repository de clientes"""
    return ClienteRepository(db)


@router.get(
    "/",
    response_model=dict,
    summary="Listar clientes",
    description="Lista todos os clientes com paginação e filtros opcionais"
)
async def listar_clientes(
    skip: int = Query(0, ge=0, description="Registros a pular"),
    limit: int = Query(100, ge=1, le=500, description="Limite de registros"),
    apenas_ativos: bool = Query(False, description="Filtrar apenas clientes ativos"),
    busca: Optional[str] = Query(None, description="Termo de busca (nome, documento, email)"),
    repo: ClienteRepository = Depends(get_cliente_repository)
):
    """Lista clientes com paginação e filtros"""
    use_case = ListarClientesUseCase(repo)
    
    clientes = await use_case.execute(
        skip=skip,
        limit=limit,
        apenas_ativos=apenas_ativos,
        termo_busca=busca
    )
    
    total = await repo.count()
    
    return {
        "data": clientes,
        "pagination": {
            "skip": skip,
            "limit": limit,
            "total": total
        }
    }


@router.get(
    "/{cliente_id}",
    response_model=ClienteResponseDTO,
    summary="Buscar cliente por ID",
    responses={404: {"description": "Cliente não encontrado"}}
)
async def buscar_cliente(
    cliente_id: UUID,
    repo: ClienteRepository = Depends(get_cliente_repository)
):
    """Retorna detalhes de um cliente específico"""
    use_case = BuscarClienteUseCase(repo)
    
    try:
        return await use_case.execute(cliente_id)
    except EntityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )


@router.post(
    "/",
    response_model=ClienteResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo cliente",
    responses={
        400: {"description": "Dados inválidos"},
        409: {"description": "Cliente já existe (documento duplicado)"}
    }
)
async def criar_cliente(
    dto: ClienteCreateDTO,
    repo: ClienteRepository = Depends(get_cliente_repository)
):
    """Cria um novo cliente no sistema"""
    use_case = CriarClienteUseCase(repo)
    
    try:
        return await use_case.execute(dto)
    except ValidationException as e:
        if "Já existe cliente" in e.message:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=e.message
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )


@router.put(
    "/{cliente_id}",
    response_model=ClienteResponseDTO,
    summary="Atualizar cliente",
    responses={404: {"description": "Cliente não encontrado"}}
)
async def atualizar_cliente(
    cliente_id: UUID,
    dto: ClienteUpdateDTO,
    repo: ClienteRepository = Depends(get_cliente_repository)
):
    """Atualiza dados de um cliente existente"""
    use_case = AtualizarClienteUseCase(repo)
    
    try:
        return await use_case.execute(cliente_id, dto)
    except EntityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )


@router.patch(
    "/{cliente_id}/ativar",
    response_model=ClienteResponseDTO,
    summary="Ativar cliente"
)
async def ativar_cliente(
    cliente_id: UUID,
    repo: ClienteRepository = Depends(get_cliente_repository)
):
    """Ativa um cliente desativado"""
    use_case = AtualizarClienteUseCase(repo)
    dto = ClienteUpdateDTO(ativo=True)
    
    try:
        return await use_case.execute(cliente_id, dto)
    except EntityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )


@router.patch(
    "/{cliente_id}/desativar",
    response_model=ClienteResponseDTO,
    summary="Desativar cliente"
)
async def desativar_cliente(
    cliente_id: UUID,
    repo: ClienteRepository = Depends(get_cliente_repository)
):
    """Desativa um cliente (soft delete)"""
    use_case = AtualizarClienteUseCase(repo)
    dto = ClienteUpdateDTO(ativo=False)
    
    try:
        return await use_case.execute(cliente_id, dto)
    except EntityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )


@router.delete(
    "/{cliente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir cliente",
    responses={404: {"description": "Cliente não encontrado"}}
)
async def excluir_cliente(
    cliente_id: UUID,
    repo: ClienteRepository = Depends(get_cliente_repository)
):
    """Remove permanentemente um cliente"""
    deleted = await repo.delete(cliente_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente não encontrado: {cliente_id}"
        )
    
    return None
