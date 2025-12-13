"""
LogiFlow CRM - Router Motoristas
Endpoints para gestão de motoristas
"""

from fastapi import APIRouter, HTTPException, Query, Path, UploadFile, File
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date, timedelta
from enum import Enum
import logging
import uuid
import re

logger = logging.getLogger(__name__)
router = APIRouter()


# ========================================
# Enums
# ========================================

class StatusMotorista(str, Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    FERIAS = "ferias"
    AFASTADO = "afastado"
    DESLIGADO = "desligado"


class CategoriaCNH(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    AB = "AB"
    AC = "AC"
    AD = "AD"
    AE = "AE"


class TipoContrato(str, Enum):
    CLT = "clt"
    AGREGADO = "agregado"
    AUTONOMO = "autonomo"
    TERCEIRIZADO = "terceirizado"


class DisponibilidadeMotorista(str, Enum):
    DISPONIVEL = "disponivel"
    EM_VIAGEM = "em_viagem"
    EM_DESCANSO = "em_descanso"
    INDISPONIVEL = "indisponivel"


# ========================================
# Schemas
# ========================================

class EnderecoSchema(BaseModel):
    cep: str
    logradouro: str
    numero: str
    complemento: Optional[str] = None
    bairro: str
    cidade: str
    uf: str = Field(..., max_length=2)


class CNHSchema(BaseModel):
    numero: str
    categoria: CategoriaCNH
    data_emissao: date
    data_validade: date
    uf_emissao: str = Field(..., max_length=2)
    primeira_habilitacao: Optional[date] = None
    observacoes: Optional[str] = None


class ContatoEmergenciaSchema(BaseModel):
    nome: str
    telefone: str
    parentesco: Optional[str] = None


class CriarMotoristaRequest(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    cpf: str = Field(..., min_length=11, max_length=14)
    rg: Optional[str] = None
    data_nascimento: date
    telefone: str
    telefone_secundario: Optional[str] = None
    email: Optional[str] = None
    
    endereco: EnderecoSchema
    cnh: CNHSchema
    
    tipo_contrato: TipoContrato = TipoContrato.CLT
    data_admissao: Optional[date] = None
    salario: Optional[float] = None
    
    contato_emergencia: Optional[ContatoEmergenciaSchema] = None
    
    veiculo_padrao_id: Optional[str] = None
    
    observacoes: Optional[str] = None
    foto_url: Optional[str] = None
    
    @validator('cpf')
    def validar_cpf(cls, v):
        cpf = re.sub(r'[^0-9]', '', v)
        if len(cpf) != 11:
            raise ValueError('CPF deve ter 11 dígitos')
        return cpf


class AtualizarMotoristaRequest(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    telefone_secundario: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[EnderecoSchema] = None
    cnh: Optional[CNHSchema] = None
    tipo_contrato: Optional[TipoContrato] = None
    salario: Optional[float] = None
    contato_emergencia: Optional[ContatoEmergenciaSchema] = None
    veiculo_padrao_id: Optional[str] = None
    observacoes: Optional[str] = None
    foto_url: Optional[str] = None


class AtualizarDisponibilidadeRequest(BaseModel):
    disponibilidade: DisponibilidadeMotorista
    motivo: Optional[str] = None
    previsao_retorno: Optional[datetime] = None


# ========================================
# Storage Simulado
# ========================================

motoristas_db: dict = {}


# ========================================
# Endpoints
# ========================================

@router.get("")
async def listar_motoristas(
    status: Optional[StatusMotorista] = None,
    disponibilidade: Optional[DisponibilidadeMotorista] = None,
    tipo_contrato: Optional[TipoContrato] = None,
    categoria_cnh: Optional[CategoriaCNH] = None,
    busca: Optional[str] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100)
):
    """Lista motoristas com filtros"""
    try:
        motoristas = list(motoristas_db.values())
        
        # Filtros
        if status:
            motoristas = [m for m in motoristas if m["status"] == status.value]
        if disponibilidade:
            motoristas = [m for m in motoristas if m.get("disponibilidade") == disponibilidade.value]
        if tipo_contrato:
            motoristas = [m for m in motoristas if m["tipo_contrato"] == tipo_contrato.value]
        if categoria_cnh:
            motoristas = [m for m in motoristas if m["cnh"]["categoria"] == categoria_cnh.value]
        if busca:
            busca_lower = busca.lower()
            motoristas = [
                m for m in motoristas
                if busca_lower in m["nome"].lower() or busca_lower in m["cpf"]
            ]
        
        # Ordenar por nome
        motoristas.sort(key=lambda x: x["nome"])
        
        # Paginação
        total = len(motoristas)
        start = (page - 1) * per_page
        motoristas_paginados = motoristas[start:start + per_page]
        
        return {
            "success": True,
            "data": motoristas_paginados,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "pages": (total + per_page - 1) // per_page
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar motoristas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/disponiveis")
async def listar_motoristas_disponiveis(
    categoria_cnh: Optional[CategoriaCNH] = None
):
    """Lista motoristas disponíveis para viagem"""
    try:
        motoristas = [
            m for m in motoristas_db.values()
            if m["status"] == StatusMotorista.ATIVO.value
            and m.get("disponibilidade") == DisponibilidadeMotorista.DISPONIVEL.value
        ]
        
        if categoria_cnh:
            # Verificar se a categoria do motorista inclui a necessária
            motoristas = [
                m for m in motoristas
                if categoria_cnh.value in m["cnh"]["categoria"]
            ]
        
        return {
            "success": True,
            "data": motoristas,
            "total": len(motoristas)
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar motoristas disponíveis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cnh-vencendo")
async def listar_cnh_vencendo(
    dias: int = Query(30, ge=1, le=180)
):
    """Lista motoristas com CNH vencendo nos próximos dias"""
    try:
        data_limite = date.today() + timedelta(days=dias)
        
        motoristas = [
            {
                "id": m["id"],
                "nome": m["nome"],
                "cnh_numero": m["cnh"]["numero"],
                "cnh_categoria": m["cnh"]["categoria"],
                "cnh_validade": m["cnh"]["data_validade"],
                "dias_para_vencer": (datetime.strptime(m["cnh"]["data_validade"], "%Y-%m-%d").date() - date.today()).days
            }
            for m in motoristas_db.values()
            if m["status"] == StatusMotorista.ATIVO.value
            and datetime.strptime(m["cnh"]["data_validade"], "%Y-%m-%d").date() <= data_limite
        ]
        
        # Ordenar por data de vencimento
        motoristas.sort(key=lambda x: x["cnh_validade"])
        
        return {
            "success": True,
            "data": motoristas,
            "total": len(motoristas),
            "alerta": f"CNHs vencendo nos próximos {dias} dias"
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar CNH vencendo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/estatisticas")
async def estatisticas_motoristas():
    """Estatísticas dos motoristas"""
    try:
        motoristas = list(motoristas_db.values())
        
        total = len(motoristas)
        por_status = {}
        por_disponibilidade = {}
        por_tipo_contrato = {}
        
        for m in motoristas:
            status = m["status"]
            por_status[status] = por_status.get(status, 0) + 1
            
            disp = m.get("disponibilidade", "nao_informado")
            por_disponibilidade[disp] = por_disponibilidade.get(disp, 0) + 1
            
            tipo = m["tipo_contrato"]
            por_tipo_contrato[tipo] = por_tipo_contrato.get(tipo, 0) + 1
        
        # CNH vencendo em 30 dias
        data_limite = date.today() + timedelta(days=30)
        cnh_vencendo = len([
            m for m in motoristas
            if m["status"] == StatusMotorista.ATIVO.value
            and datetime.strptime(m["cnh"]["data_validade"], "%Y-%m-%d").date() <= data_limite
        ])
        
        return {
            "success": True,
            "data": {
                "total": total,
                "por_status": por_status,
                "por_disponibilidade": por_disponibilidade,
                "por_tipo_contrato": por_tipo_contrato,
                "cnh_vencendo_30_dias": cnh_vencendo
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao gerar estatísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{motorista_id}")
async def obter_motorista(motorista_id: str):
    """Obtém detalhes de um motorista"""
    try:
        if motorista_id not in motoristas_db:
            raise HTTPException(status_code=404, detail="Motorista não encontrado")
        
        return {
            "success": True,
            "data": motoristas_db[motorista_id]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter motorista: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("")
async def criar_motorista(request: CriarMotoristaRequest):
    """Cadastra um novo motorista"""
    try:
        # Verificar CPF duplicado
        for m in motoristas_db.values():
            if m["cpf"] == request.cpf:
                raise HTTPException(
                    status_code=400,
                    detail="CPF já cadastrado"
                )
        
        motorista_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        motorista = {
            "id": motorista_id,
            "nome": request.nome,
            "cpf": request.cpf,
            "rg": request.rg,
            "data_nascimento": request.data_nascimento.isoformat(),
            "telefone": request.telefone,
            "telefone_secundario": request.telefone_secundario,
            "email": request.email,
            "endereco": request.endereco.dict(),
            "cnh": {
                **request.cnh.dict(),
                "data_emissao": request.cnh.data_emissao.isoformat(),
                "data_validade": request.cnh.data_validade.isoformat(),
                "primeira_habilitacao": request.cnh.primeira_habilitacao.isoformat() if request.cnh.primeira_habilitacao else None,
                "categoria": request.cnh.categoria.value
            },
            "tipo_contrato": request.tipo_contrato.value,
            "data_admissao": request.data_admissao.isoformat() if request.data_admissao else None,
            "salario": request.salario,
            "contato_emergencia": request.contato_emergencia.dict() if request.contato_emergencia else None,
            "veiculo_padrao_id": request.veiculo_padrao_id,
            "status": StatusMotorista.ATIVO.value,
            "disponibilidade": DisponibilidadeMotorista.DISPONIVEL.value,
            "observacoes": request.observacoes,
            "foto_url": request.foto_url,
            "criado_em": now,
            "atualizado_em": now,
            "viagens_realizadas": 0,
            "km_rodados": 0,
            "avaliacao_media": None
        }
        
        motoristas_db[motorista_id] = motorista
        
        logger.info(f"Motorista cadastrado: {request.nome}")
        
        return {
            "success": True,
            "message": "Motorista cadastrado com sucesso",
            "data": motorista
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar motorista: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{motorista_id}")
async def atualizar_motorista(
    motorista_id: str,
    request: AtualizarMotoristaRequest
):
    """Atualiza dados de um motorista"""
    try:
        if motorista_id not in motoristas_db:
            raise HTTPException(status_code=404, detail="Motorista não encontrado")
        
        motorista = motoristas_db[motorista_id]
        
        update_data = request.dict(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                if key == "cnh" and value:
                    motorista["cnh"] = {
                        **value,
                        "data_emissao": value["data_emissao"].isoformat() if isinstance(value["data_emissao"], date) else value["data_emissao"],
                        "data_validade": value["data_validade"].isoformat() if isinstance(value["data_validade"], date) else value["data_validade"],
                        "categoria": value["categoria"].value if hasattr(value["categoria"], 'value') else value["categoria"]
                    }
                elif key == "endereco" and value:
                    motorista["endereco"] = value if isinstance(value, dict) else value.dict()
                elif key == "contato_emergencia" and value:
                    motorista["contato_emergencia"] = value if isinstance(value, dict) else value.dict()
                elif hasattr(value, 'value'):
                    motorista[key] = value.value
                elif hasattr(value, 'dict'):
                    motorista[key] = value.dict()
                else:
                    motorista[key] = value
        
        motorista["atualizado_em"] = datetime.utcnow()
        
        return {
            "success": True,
            "message": "Motorista atualizado",
            "data": motorista
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar motorista: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{motorista_id}/status")
async def atualizar_status_motorista(
    motorista_id: str,
    status: StatusMotorista,
    motivo: Optional[str] = None
):
    """Atualiza status do motorista"""
    try:
        if motorista_id not in motoristas_db:
            raise HTTPException(status_code=404, detail="Motorista não encontrado")
        
        motorista = motoristas_db[motorista_id]
        motorista["status"] = status.value
        motorista["atualizado_em"] = datetime.utcnow()
        
        if motivo:
            motorista["motivo_status"] = motivo
        
        logger.info(f"Status do motorista {motorista['nome']} alterado para {status.value}")
        
        return {
            "success": True,
            "message": f"Status alterado para {status.value}",
            "data": motorista
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{motorista_id}/disponibilidade")
async def atualizar_disponibilidade(
    motorista_id: str,
    request: AtualizarDisponibilidadeRequest
):
    """Atualiza disponibilidade do motorista"""
    try:
        if motorista_id not in motoristas_db:
            raise HTTPException(status_code=404, detail="Motorista não encontrado")
        
        motorista = motoristas_db[motorista_id]
        motorista["disponibilidade"] = request.disponibilidade.value
        motorista["atualizado_em"] = datetime.utcnow()
        
        if request.motivo:
            motorista["motivo_disponibilidade"] = request.motivo
        if request.previsao_retorno:
            motorista["previsao_retorno"] = request.previsao_retorno.isoformat()
        
        return {
            "success": True,
            "message": f"Disponibilidade alterada para {request.disponibilidade.value}",
            "data": motorista
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar disponibilidade: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{motorista_id}/viagens")
async def listar_viagens_motorista(
    motorista_id: str,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100)
):
    """Lista viagens realizadas pelo motorista"""
    try:
        if motorista_id not in motoristas_db:
            raise HTTPException(status_code=404, detail="Motorista não encontrado")
        
        # TODO: Integrar com pedidos_db
        # Por enquanto retorna lista vazia
        
        return {
            "success": True,
            "data": [],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": 0,
                "pages": 0
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao listar viagens: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{motorista_id}")
async def excluir_motorista(motorista_id: str):
    """Exclui (inativa) um motorista"""
    try:
        if motorista_id not in motoristas_db:
            raise HTTPException(status_code=404, detail="Motorista não encontrado")
        
        motorista = motoristas_db[motorista_id]
        
        # Soft delete - apenas inativa
        motorista["status"] = StatusMotorista.DESLIGADO.value
        motorista["disponibilidade"] = DisponibilidadeMotorista.INDISPONIVEL.value
        motorista["desligado_em"] = datetime.utcnow()
        motorista["atualizado_em"] = datetime.utcnow()
        
        logger.info(f"Motorista desligado: {motorista['nome']}")
        
        return {
            "success": True,
            "message": "Motorista desligado com sucesso"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao excluir motorista: {e}")
        raise HTTPException(status_code=500, detail=str(e))
