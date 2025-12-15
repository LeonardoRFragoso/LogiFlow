"""
Router para gerenciamento de clientes
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()


class ClienteBase(BaseModel):
    razao_social: str
    nome_fantasia: Optional[str] = None
    cnpj: str
    ie: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: str
    uf: str
    cep: str
    ativo: bool = True


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(ClienteBase):
    pass


class ClienteResponse(ClienteBase):
    id: int
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
    status: Optional[str] = None,
    cidade: Optional[str] = None,
    uf: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lista todos os clientes"""
    # TODO: Implementar consulta real ao banco de dados
    clientes = clientes_mock.copy()
    
    # Filtros
    if status == "ativo":
        clientes = [c for c in clientes if c.get("ativo", True)]
    elif status == "inativo":
        clientes = [c for c in clientes if not c.get("ativo", True)]
    
    if cidade:
        clientes = [c for c in clientes if c.get("cidade", "").lower() == cidade.lower()]
    
    if uf:
        clientes = [c for c in clientes if c.get("uf", "").upper() == uf.upper()]
    
    return {"data": clientes, "total": len(clientes)}


@router.get("/{cliente_id}", response_model=ClienteResponse)
async def obter_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Obtém detalhes de um cliente específico"""
    # TODO: Implementar consulta real ao banco de dados
    cliente = next((c for c in clientes_mock if c["id"] == cliente_id), None)
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    return cliente


@router.post("/", response_model=ClienteResponse, status_code=201)
async def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """Cria um novo cliente"""
    # TODO: Implementar criação real no banco de dados
    novo_cliente = {
        "id": len(clientes_mock) + 1,
        **cliente.dict(),
        "created_at": datetime.now().isoformat(),
        "updated_at": None
    }
    
    clientes_mock.append(novo_cliente)
    return novo_cliente


@router.put("/{cliente_id}", response_model=ClienteResponse)
async def atualizar_cliente(
    cliente_id: int,
    cliente: ClienteUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um cliente existente"""
    # TODO: Implementar atualização real no banco de dados
    cliente_existente = next((c for c in clientes_mock if c["id"] == cliente_id), None)
    
    if not cliente_existente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    cliente_existente.update(cliente.dict())
    cliente_existente["updated_at"] = datetime.now().isoformat()
    
    return cliente_existente


@router.delete("/{cliente_id}", status_code=204)
async def excluir_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Exclui um cliente (soft delete)"""
    # TODO: Implementar exclusão real no banco de dados
    cliente = next((c for c in clientes_mock if c["id"] == cliente_id), None)
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    cliente["ativo"] = False
    cliente["updated_at"] = datetime.now().isoformat()
    
    return None

