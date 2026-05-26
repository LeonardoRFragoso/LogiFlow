"""
Router para gerenciamento de clientes
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db
from models import Cliente
from middleware.tenant import get_current_tenant_id
from loguru import logger

router = APIRouter()


class ClienteBase(BaseModel):
    # Dados da Empresa
    razao_social: str
    nome_fantasia: Optional[str] = None
    cnpj: Optional[str] = None
    ie: Optional[str] = None  # Inscrição Estadual (alias: inscricao_estadual)
    
    # Contato
    contato_nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    celular: Optional[str] = None
    
    # Endereço
    cep: Optional[str] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    
    # Comercial
    condicao_pagamento: Optional[str] = "30_dias"
    limite_credito: Optional[float] = 0
    
    # Status
    ativo: bool = True
    observacoes: Optional[str] = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    # Todos os campos opcionais para update parcial
    razao_social: Optional[str] = None
    nome_fantasia: Optional[str] = None
    cnpj: Optional[str] = None
    ie: Optional[str] = None
    contato_nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    celular: Optional[str] = None
    cep: Optional[str] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    condicao_pagamento: Optional[str] = None
    limite_credito: Optional[float] = None
    ativo: Optional[bool] = None
    observacoes: Optional[str] = None


class ClienteResponse(BaseModel):
    id: int
    razao_social: str
    nome_fantasia: Optional[str] = None
    cnpj: Optional[str] = None
    ie: Optional[str] = None
    contato_nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    celular: Optional[str] = None
    cep: Optional[str] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    condicao_pagamento: Optional[str] = None
    limite_credito: Optional[float] = None
    ativo: bool = True
    observacoes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Mock de dados para desenvolvimento
clientes_mock = [
    {
        "id": 1,
        "razao_social": "Transportadora Alpha Ltda",
        "nome_fantasia": "Alpha Trans",
        "cnpj": "12.345.678/0001-90",
        "ie": "123.456.789.012",
        "telefone": "(11) 3456-7890",
        "email": "contato@alpha.com.br",
        "endereco": "Rua das Flores",
        "numero": "123",
        "complemento": "Sala 45",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "uf": "SP",
        "cep": "01234-567",
        "ativo": True,
        "created_at": datetime.now().isoformat(),
        "updated_at": None
    },
    {
        "id": 2,
        "razao_social": "Beta Logística S.A.",
        "nome_fantasia": "Beta Log",
        "cnpj": "98.765.432/0001-10",
        "ie": "987.654.321.098",
        "telefone": "(21) 2345-6789",
        "email": "contato@betalog.com.br",
        "endereco": "Av. Principal",
        "numero": "456",
        "complemento": None,
        "bairro": "Industrial",
        "cidade": "Rio de Janeiro",
        "uf": "RJ",
        "cep": "20123-456",
        "ativo": True,
        "created_at": datetime.now().isoformat(),
        "updated_at": None
    }
]


@router.get("/", response_model=List[ClienteResponse])
async def listar_clientes(
    request: Request,
    status: Optional[str] = None,
    cidade: Optional[str] = None,
    uf: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista clientes do tenant atual"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        # Construir query base filtrando por tenant
        query = db.query(Cliente).filter(Cliente.tenant_id == tenant_id)
        
        # Aplicar filtros adicionais
        if status == "ativo":
            query = query.filter(Cliente.ativo == True)
        elif status == "inativo":
            query = query.filter(Cliente.ativo == False)
        
        if cidade:
            query = query.filter(Cliente.cidade.ilike(f"%{cidade}%"))
        
        if uf:
            query = query.filter(Cliente.uf.ilike(f"%{uf}%"))
        
        # Aplicar paginação
        total = query.count()
        clientes = query.offset(skip).limit(limit).all()
        
        logger.info(f"✅ Listados {len(clientes)} clientes do tenant {tenant_id}")
        
        return clientes
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao listar clientes: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{cliente_id}", response_model=ClienteResponse)
async def obter_cliente(
    cliente_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Obtém detalhes de um cliente específico do tenant atual"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        cliente = db.query(Cliente).filter(
            Cliente.id == cliente_id,
            Cliente.tenant_id == tenant_id
        ).first()
        
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        logger.info(f"✅ Cliente {cliente_id} obtido do tenant {tenant_id}")
        return cliente
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao obter cliente: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=ClienteResponse, status_code=201)
async def criar_cliente(
    cliente: ClienteCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Cria um novo cliente para o tenant atual"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        novo_cliente = Cliente(
            **cliente.dict(),
            tenant_id=tenant_id
        )
        
        db.add(novo_cliente)
        db.commit()
        db.refresh(novo_cliente)
        
        logger.info(f"✅ Cliente {novo_cliente.id} criado para tenant {tenant_id}")
        return novo_cliente
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao criar cliente: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{cliente_id}", response_model=ClienteResponse)
async def atualizar_cliente(
    cliente_id: str,
    cliente_data: ClienteUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Atualiza um cliente do tenant atual"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        cliente = db.query(Cliente).filter(
            Cliente.id == cliente_id,
            Cliente.tenant_id == tenant_id
        ).first()
        
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        # Atualizar campos
        for key, value in cliente_data.dict(exclude_unset=True).items():
            setattr(cliente, key, value)
        
        db.commit()
        db.refresh(cliente)
        
        logger.info(f"✅ Cliente {cliente_id} atualizado no tenant {tenant_id}")
        return cliente
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao atualizar cliente: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{cliente_id}", status_code=204)
async def excluir_cliente(
    cliente_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Deleta um cliente do tenant atual (soft delete)"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        cliente = db.query(Cliente).filter(
            Cliente.id == cliente_id,
            Cliente.tenant_id == tenant_id
        ).first()
        
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        cliente.ativo = False
        db.commit()
        
        logger.info(f"✅ Cliente {cliente_id} deletado (soft delete) do tenant {tenant_id}")
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao deletar cliente: {e}")
        raise HTTPException(status_code=500, detail=str(e))

