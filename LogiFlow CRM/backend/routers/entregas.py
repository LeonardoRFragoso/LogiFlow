"""
Router para gerenciamento de entregas
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()


class EntregaBase(BaseModel):
    codigo: str
    cliente_id: int
    cliente_nome: str
    endereco_entrega: str
    cidade: str
    uf: str
    motorista_id: Optional[int] = None
    motorista_nome: Optional[str] = None
    veiculo_placa: Optional[str] = None
    status: str = "aguardando_coleta"
    previsao_entrega: datetime
    observacoes: Optional[str] = None


class EntregaCreate(EntregaBase):
    pass


class EntregaUpdate(BaseModel):
    status: Optional[str] = None
    motorista_id: Optional[int] = None
    motorista_nome: Optional[str] = None
    veiculo_placa: Optional[str] = None
    observacoes: Optional[str] = None


class EntregaResponse(EntregaBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Mock de dados
entregas_mock = [
    {
        "id": 1,
        "codigo": "ENT-2024-001",
        "cliente_id": 1,
        "cliente_nome": "Alpha Trans",
        "endereco_entrega": "Rua das Entregas, 123",
        "cidade": "São Paulo",
        "uf": "SP",
        "motorista_id": 1,
        "motorista_nome": "João Silva",
        "veiculo_placa": "ABC-1234",
        "status": "em_transito",
        "previsao_entrega": (datetime.now() + timedelta(days=2)).isoformat(),
        "observacoes": "Entregar no período da manhã",
        "created_at": datetime.now().isoformat(),
        "updated_at": None
    },
    {
        "id": 2,
        "codigo": "ENT-2024-002",
        "cliente_id": 2,
        "cliente_nome": "Beta Log",
        "endereco_entrega": "Av. Central, 456",
        "cidade": "Rio de Janeiro",
        "uf": "RJ",
        "motorista_id": 2,
        "motorista_nome": "Maria Santos",
        "veiculo_placa": "DEF-5678",
        "status": "saiu_para_entrega",
        "previsao_entrega": datetime.now().isoformat(),
        "observacoes": None,
        "created_at": datetime.now().isoformat(),
        "updated_at": None
    },
    {
        "id": 3,
        "codigo": "ENT-2024-003",
        "cliente_id": 1,
        "cliente_nome": "Alpha Trans",
        "endereco_entrega": "Rua Comercial, 789",
        "cidade": "Campinas",
        "uf": "SP",
        "motorista_id": None,
        "motorista_nome": None,
        "veiculo_placa": None,
        "status": "aguardando_coleta",
        "previsao_entrega": (datetime.now() + timedelta(days=5)).isoformat(),
        "observacoes": None,
        "created_at": datetime.now().isoformat(),
        "updated_at": None
    }
]


@router.get("/", response_model=List[EntregaResponse])
async def listar_entregas(
    status: Optional[str] = None,
    motorista_id: Optional[int] = None,
    cliente_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Lista todas as entregas"""
    entregas = entregas_mock.copy()
    
    if status:
        entregas = [e for e in entregas if e.get("status") == status]
    
    if motorista_id:
        entregas = [e for e in entregas if e.get("motorista_id") == motorista_id]
    
    if cliente_id:
        entregas = [e for e in entregas if e.get("cliente_id") == cliente_id]
    
    return {"data": entregas, "total": len(entregas)}


@router.get("/stats")
async def obter_estatisticas_entregas(db: Session = Depends(get_db)):
    """Obtém estatísticas das entregas"""
    total = len(entregas_mock)
    em_transito = len([e for e in entregas_mock if e["status"] == "em_transito"])
    entregues = len([e for e in entregas_mock if e["status"] == "entregue"])
    atrasadas = len([e for e in entregas_mock if e["status"] in ["atrasada", "pendente"]])
    
    return {
        "total": total,
        "emTransito": em_transito,
        "entregues": entregues,
        "atrasadas": atrasadas
    }


@router.get("/{entrega_id}", response_model=EntregaResponse)
async def obter_entrega(entrega_id: int, db: Session = Depends(get_db)):
    """Obtém detalhes de uma entrega específica"""
    entrega = next((e for e in entregas_mock if e["id"] == entrega_id), None)
    
    if not entrega:
        raise HTTPException(status_code=404, detail="Entrega não encontrada")
    
    return entrega


@router.post("/", response_model=EntregaResponse, status_code=201)
async def criar_entrega(entrega: EntregaCreate, db: Session = Depends(get_db)):
    """Cria uma nova entrega"""
    nova_entrega = {
        "id": len(entregas_mock) + 1,
        **entrega.dict(),
        "created_at": datetime.now().isoformat(),
        "updated_at": None
    }
    
    entregas_mock.append(nova_entrega)
    return nova_entrega


@router.patch("/{entrega_id}", response_model=EntregaResponse)
async def atualizar_entrega(
    entrega_id: int,
    entrega: EntregaUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza uma entrega existente"""
    entrega_existente = next((e for e in entregas_mock if e["id"] == entrega_id), None)
    
    if not entrega_existente:
        raise HTTPException(status_code=404, detail="Entrega não encontrada")
    
    for key, value in entrega.dict(exclude_unset=True).items():
        if value is not None:
            entrega_existente[key] = value
    
    entrega_existente["updated_at"] = datetime.now().isoformat()
    
    return entrega_existente


@router.delete("/{entrega_id}", status_code=204)
async def excluir_entrega(entrega_id: int, db: Session = Depends(get_db)):
    """Exclui uma entrega"""
    entrega_idx = next((i for i, e in enumerate(entregas_mock) if e["id"] == entrega_id), None)
    
    if entrega_idx is None:
        raise HTTPException(status_code=404, detail="Entrega não encontrada")
    
    entregas_mock.pop(entrega_idx)
    return None

