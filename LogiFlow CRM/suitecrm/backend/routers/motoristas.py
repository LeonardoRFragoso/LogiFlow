"""
LogiFlow CRM - Motoristas Router
Orquestra chamadas para SuiteCRM API V8
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from enum import Enum

from integrations.suitecrm import SuiteCRMMapper

router = APIRouter()


class MotoristaStatus(str, Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    FERIAS = "ferias"
    AFASTADO = "afastado"


class CNHCategoria(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    AB = "AB"
    AC = "AC"
    AD = "AD"
    AE = "AE"


class MotoristaCreate(BaseModel):
    nome: str
    cpf: str
    cnh_numero: str
    cnh_categoria: CNHCategoria
    cnh_validade: date
    celular: str
    email: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    observacoes: Optional[str] = None


class MotoristaUpdate(BaseModel):
    nome: Optional[str] = None
    celular: Optional[str] = None
    email: Optional[str] = None
    cnh_validade: Optional[date] = None
    status: Optional[MotoristaStatus] = None


class MotoristaResponse(BaseModel):
    id: str
    nome: str
    cpf: str
    cnh_numero: str
    cnh_categoria: str
    cnh_validade: Optional[str]
    celular: str
    email: Optional[str]
    status: str
    disponibilidade: str
    created_at: str


class MotoristaList(BaseModel):
    total: int
    page: int
    items: List[MotoristaResponse]


@router.get("/", response_model=MotoristaList)
async def listar_motoristas(
    request: Request,
    page: int = 1,
    status: Optional[MotoristaStatus] = None,
    disponivel: bool = False
):
    """Lista motoristas com filtros"""
    suitecrm = request.app.state.suitecrm
    
    try:
        filters = {}
        if status:
            filters["status"] = status.value
        if disponivel:
            filters["disponibilidade"] = "disponivel"
        
        result = await suitecrm.list_records(
            "Motoristas", 
            page=page, 
            filters=filters if filters else None
        )
        
        items = []
        for record in result.get("data", []):
            mapped = SuiteCRMMapper.motorista_from_suitecrm(record)
            items.append(MotoristaResponse(**mapped))
        
        meta = result.get("meta", {})
        total = meta.get("total-records", len(items))
        
        return MotoristaList(total=total, page=page, items=items)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/disponiveis")
async def listar_motoristas_disponiveis(request: Request):
    """Lista motoristas disponíveis para atribuição"""
    suitecrm = request.app.state.suitecrm
    
    try:
        result = await suitecrm.listar_motoristas_ativos()
        
        items = []
        for record in result.get("data", []):
            mapped = SuiteCRMMapper.motorista_from_suitecrm(record)
            if mapped.get("disponibilidade") == "disponivel":
                items.append({
                    "id": mapped["id"],
                    "nome": mapped["nome"],
                    "celular": mapped["celular"],
                    "cnh_categoria": mapped["cnh_categoria"]
                })
        
        return {"items": items, "total": len(items)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{motorista_id}", response_model=MotoristaResponse)
async def obter_motorista(request: Request, motorista_id: str):
    """Obtém detalhes de um motorista"""
    suitecrm = request.app.state.suitecrm
    
    try:
        result = await suitecrm.get_record("Motoristas", motorista_id)
        
        if not result.get("data"):
            raise HTTPException(status_code=404, detail="Motorista não encontrado")
        
        mapped = SuiteCRMMapper.motorista_from_suitecrm(result["data"])
        return MotoristaResponse(**mapped)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=MotoristaResponse)
async def criar_motorista(request: Request, motorista: MotoristaCreate):
    """Cria novo motorista"""
    suitecrm = request.app.state.suitecrm
    
    try:
        dados = {
            "name": motorista.nome,
            "cpf": motorista.cpf,
            "cnh_numero": motorista.cnh_numero,
            "cnh_categoria": motorista.cnh_categoria.value,
            "cnh_validade": str(motorista.cnh_validade),
            "celular": motorista.celular,
            "email": motorista.email or "",
            "endereco": motorista.endereco or "",
            "cidade": motorista.cidade or "",
            "uf": motorista.uf or "",
            "status": "ativo",
            "disponibilidade": "disponivel",
            "observacoes": motorista.observacoes or "",
        }
        
        result = await suitecrm.create_record("Motoristas", dados)
        
        if not result.get("data"):
            raise HTTPException(status_code=500, detail="Erro ao criar motorista")
        
        mapped = SuiteCRMMapper.motorista_from_suitecrm(result["data"])
        return MotoristaResponse(**mapped)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{motorista_id}", response_model=MotoristaResponse)
async def atualizar_motorista(request: Request, motorista_id: str, motorista: MotoristaUpdate):
    """Atualiza dados de um motorista"""
    suitecrm = request.app.state.suitecrm
    
    try:
        dados = {}
        if motorista.nome:
            dados["name"] = motorista.nome
        if motorista.celular:
            dados["celular"] = motorista.celular
        if motorista.email:
            dados["email"] = motorista.email
        if motorista.cnh_validade:
            dados["cnh_validade"] = str(motorista.cnh_validade)
        if motorista.status:
            dados["status"] = motorista.status.value
        
        if not dados:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        result = await suitecrm.update_record("Motoristas", motorista_id, dados)
        
        if not result.get("data"):
            raise HTTPException(status_code=500, detail="Erro ao atualizar motorista")
        
        mapped = SuiteCRMMapper.motorista_from_suitecrm(result["data"])
        return MotoristaResponse(**mapped)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cnh-vencendo")
async def motoristas_cnh_vencendo(request: Request, dias: int = 30):
    """Lista motoristas com CNH vencendo nos próximos dias"""
    suitecrm = request.app.state.suitecrm
    
    try:
        from datetime import datetime, timedelta
        
        data_limite = (datetime.now() + timedelta(days=dias)).strftime("%Y-%m-%d")
        
        result = await suitecrm.list_records(
            "Motoristas",
            filters={"status": "ativo"}
        )
        
        items = []
        for record in result.get("data", []):
            mapped = SuiteCRMMapper.motorista_from_suitecrm(record)
            if mapped.get("cnh_validade") and mapped["cnh_validade"] <= data_limite:
                items.append({
                    "id": mapped["id"],
                    "nome": mapped["nome"],
                    "cnh_validade": mapped["cnh_validade"],
                    "celular": mapped["celular"]
                })
        
        return {
            "alerta": f"Motoristas com CNH vencendo em {dias} dias",
            "total": len(items),
            "items": items
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
