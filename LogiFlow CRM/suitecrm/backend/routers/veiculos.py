"""
LogiFlow CRM - Veículos Router
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


class TipoVeiculo(str, Enum):
    VUC = "vuc"
    TOCO = "toco"
    TRUCK = "truck"
    CARRETA_SIMPLES = "carreta_simples"
    CARRETA_LS = "carreta_ls"
    BITREM = "bitrem"
    VAN = "van"
    FIORINO = "fiorino"
    UTILITARIO = "utilitario"


class VeiculoStatus(str, Enum):
    DISPONIVEL = "disponivel"
    EM_VIAGEM = "em_viagem"
    MANUTENCAO = "manutencao"
    INATIVO = "inativo"


class VeiculoCreate(BaseModel):
    placa: str
    tipo_veiculo: TipoVeiculo
    marca: Optional[str] = None
    modelo: Optional[str] = None
    ano_fabricacao: Optional[int] = None
    capacidade_kg: Optional[Decimal] = None
    renavam: Optional[str] = None
    observacoes: Optional[str] = None


class VeiculoUpdate(BaseModel):
    status: Optional[VeiculoStatus] = None
    km_atual: Optional[int] = None
    ultima_manutencao: Optional[date] = None
    proxima_manutencao: Optional[date] = None


class VeiculoResponse(BaseModel):
    id: str
    nome: str
    placa: str
    tipo_veiculo: str
    marca: Optional[str]
    modelo: Optional[str]
    capacidade_kg: float
    status: str
    status_manutencao: str
    km_atual: int
    ultima_manutencao: Optional[str]
    created_at: str


class VeiculoList(BaseModel):
    total: int
    page: int
    items: List[VeiculoResponse]


@router.get("/", response_model=VeiculoList)
async def listar_veiculos(
    request: Request,
    page: int = 1,
    status: Optional[VeiculoStatus] = None,
    tipo: Optional[TipoVeiculo] = None
):
    """Lista veículos com filtros"""
    suitecrm = request.app.state.suitecrm
    
    try:
        filters = {}
        if status:
            filters["status"] = status.value
        if tipo:
            filters["tipo_veiculo"] = tipo.value
        
        result = await suitecrm.list_records(
            "Veiculos", 
            page=page, 
            filters=filters if filters else None
        )
        
        items = []
        for record in result.get("data", []):
            mapped = SuiteCRMMapper.veiculo_from_suitecrm(record)
            items.append(VeiculoResponse(**mapped))
        
        meta = result.get("meta", {})
        total = meta.get("total-records", len(items))
        
        return VeiculoList(total=total, page=page, items=items)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/disponiveis")
async def listar_veiculos_disponiveis(request: Request):
    """Lista veículos disponíveis para atribuição"""
    suitecrm = request.app.state.suitecrm
    
    try:
        result = await suitecrm.listar_veiculos_disponiveis()
        
        items = []
        for record in result.get("data", []):
            mapped = SuiteCRMMapper.veiculo_from_suitecrm(record)
            items.append({
                "id": mapped["id"],
                "nome": mapped["nome"],
                "placa": mapped["placa"],
                "tipo_veiculo": mapped["tipo_veiculo"],
                "capacidade_kg": mapped["capacidade_kg"]
            })
        
        return {"items": items, "total": len(items)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{veiculo_id}", response_model=VeiculoResponse)
async def obter_veiculo(request: Request, veiculo_id: str):
    """Obtém detalhes de um veículo"""
    suitecrm = request.app.state.suitecrm
    
    try:
        result = await suitecrm.get_record("Veiculos", veiculo_id)
        
        if not result.get("data"):
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        
        mapped = SuiteCRMMapper.veiculo_from_suitecrm(result["data"])
        return VeiculoResponse(**mapped)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=VeiculoResponse)
async def criar_veiculo(request: Request, veiculo: VeiculoCreate):
    """Cria novo veículo"""
    suitecrm = request.app.state.suitecrm
    
    try:
        dados = {
            "name": f"{veiculo.placa} - {veiculo.modelo or veiculo.tipo_veiculo.value}",
            "placa": veiculo.placa,
            "tipo_veiculo": veiculo.tipo_veiculo.value,
            "marca": veiculo.marca or "",
            "modelo": veiculo.modelo or "",
            "ano_fabricacao": str(veiculo.ano_fabricacao) if veiculo.ano_fabricacao else "",
            "capacidade_kg": str(veiculo.capacidade_kg) if veiculo.capacidade_kg else "0",
            "renavam": veiculo.renavam or "",
            "status": "disponivel",
            "status_manutencao": "ok",
            "observacoes": veiculo.observacoes or "",
        }
        
        result = await suitecrm.create_record("Veiculos", dados)
        
        if not result.get("data"):
            raise HTTPException(status_code=500, detail="Erro ao criar veículo")
        
        mapped = SuiteCRMMapper.veiculo_from_suitecrm(result["data"])
        return VeiculoResponse(**mapped)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{veiculo_id}", response_model=VeiculoResponse)
async def atualizar_veiculo(request: Request, veiculo_id: str, veiculo: VeiculoUpdate):
    """Atualiza dados de um veículo"""
    suitecrm = request.app.state.suitecrm
    
    try:
        dados = {}
        if veiculo.status:
            dados["status"] = veiculo.status.value
        if veiculo.km_atual:
            dados["km_atual"] = str(veiculo.km_atual)
        if veiculo.ultima_manutencao:
            dados["ultima_manutencao"] = str(veiculo.ultima_manutencao)
        if veiculo.proxima_manutencao:
            dados["proxima_manutencao"] = str(veiculo.proxima_manutencao)
        
        if not dados:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        result = await suitecrm.update_record("Veiculos", veiculo_id, dados)
        
        if not result.get("data"):
            raise HTTPException(status_code=500, detail="Erro ao atualizar veículo")
        
        mapped = SuiteCRMMapper.veiculo_from_suitecrm(result["data"])
        return VeiculoResponse(**mapped)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{veiculo_id}/status")
async def atualizar_status_veiculo(
    request: Request,
    veiculo_id: str,
    status: VeiculoStatus
):
    """Atualiza status do veículo"""
    suitecrm = request.app.state.suitecrm
    
    try:
        await suitecrm.update_record("Veiculos", veiculo_id, {"status": status.value})
        return {"message": f"Status atualizado para {status.value}", "veiculo_id": veiculo_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
