"""
LogiFlow CRM - Router Veículos
Endpoints para gestão de frota de veículos
"""

from fastapi import APIRouter, HTTPException, Query, Path
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

class StatusVeiculo(str, Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    MANUTENCAO = "manutencao"
    VENDIDO = "vendido"
    SINISTRADO = "sinistrado"


class TipoVeiculo(str, Enum):
    UTILITARIO = "utilitario"
    VUC = "vuc"
    TOCO = "toco"
    TRUCK = "truck"
    CARRETA = "carreta"
    BITREM = "bitrem"
    RODOTREM = "rodotrem"
    VAN = "van"
    FURGAO = "furgao"


class TipoCarroceria(str, Enum):
    ABERTA = "aberta"
    FECHADA = "fechada"
    BAU = "bau"
    SIDER = "sider"
    GRANELEIRA = "graneleira"
    TANQUE = "tanque"
    CEGONHA = "cegonha"
    REFRIGERADA = "refrigerada"
    PORTA_CONTAINER = "porta_container"


class TipoPropriedade(str, Enum):
    PROPRIO = "proprio"
    AGREGADO = "agregado"
    TERCEIRIZADO = "terceirizado"
    ALUGADO = "alugado"


class DisponibilidadeVeiculo(str, Enum):
    DISPONIVEL = "disponivel"
    EM_VIAGEM = "em_viagem"
    EM_MANUTENCAO = "em_manutencao"
    RESERVADO = "reservado"
    INDISPONIVEL = "indisponivel"


class TipoManutencao(str, Enum):
    PREVENTIVA = "preventiva"
    CORRETIVA = "corretiva"
    REVISAO = "revisao"
    TROCA_OLEO = "troca_oleo"
    TROCA_PNEUS = "troca_pneus"
    FUNILARIA = "funilaria"
    OUTROS = "outros"


# ========================================
# Schemas
# ========================================

class DocumentoVeiculo(BaseModel):
    tipo: str  # CRLV, Seguro, ANTT, etc
    numero: str
    data_emissao: date
    data_validade: date
    arquivo_url: Optional[str] = None


class ManutencaoSchema(BaseModel):
    tipo: TipoManutencao
    data: date
    km_atual: int
    descricao: str
    valor: float
    oficina: Optional[str] = None
    proxima_km: Optional[int] = None
    proxima_data: Optional[date] = None
    observacoes: Optional[str] = None


class CriarVeiculoRequest(BaseModel):
    placa: str = Field(..., min_length=7, max_length=8)
    placa_reboque: Optional[str] = None
    renavam: str
    chassi: Optional[str] = None
    
    marca: str
    modelo: str
    ano_fabricacao: int = Field(..., ge=1990, le=2030)
    ano_modelo: int = Field(..., ge=1990, le=2030)
    cor: Optional[str] = None
    
    tipo: TipoVeiculo
    tipo_carroceria: TipoCarroceria
    tipo_propriedade: TipoPropriedade = TipoPropriedade.PROPRIO
    
    capacidade_kg: float = Field(..., gt=0)
    capacidade_m3: Optional[float] = None
    eixos: int = Field(..., ge=2, le=9)
    
    km_atual: int = Field(0, ge=0)
    
    rntrc: Optional[str] = None  # Registro Nacional de Transportadores
    antt: Optional[str] = None
    
    motorista_padrao_id: Optional[str] = None
    
    proprietario_nome: Optional[str] = None
    proprietario_documento: Optional[str] = None
    
    valor_compra: Optional[float] = None
    data_compra: Optional[date] = None
    
    seguro_apolice: Optional[str] = None
    seguro_validade: Optional[date] = None
    seguro_valor: Optional[float] = None
    
    observacoes: Optional[str] = None
    foto_url: Optional[str] = None
    
    @validator('placa')
    def validar_placa(cls, v):
        placa = v.upper().replace('-', '')
        # Placa antiga: ABC1234 ou Mercosul: ABC1D23
        if not re.match(r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$', placa):
            raise ValueError('Placa inválida')
        return placa


class AtualizarVeiculoRequest(BaseModel):
    placa_reboque: Optional[str] = None
    cor: Optional[str] = None
    tipo_carroceria: Optional[TipoCarroceria] = None
    tipo_propriedade: Optional[TipoPropriedade] = None
    capacidade_kg: Optional[float] = None
    capacidade_m3: Optional[float] = None
    km_atual: Optional[int] = None
    rntrc: Optional[str] = None
    antt: Optional[str] = None
    motorista_padrao_id: Optional[str] = None
    seguro_apolice: Optional[str] = None
    seguro_validade: Optional[date] = None
    seguro_valor: Optional[float] = None
    observacoes: Optional[str] = None
    foto_url: Optional[str] = None


class AtualizarKmRequest(BaseModel):
    km_atual: int = Field(..., ge=0)
    data_registro: Optional[datetime] = None
    observacao: Optional[str] = None


class AgendarManutencaoRequest(BaseModel):
    tipo: TipoManutencao
    data_agendada: date
    km_atual: Optional[int] = None
    descricao: str
    valor_estimado: Optional[float] = None
    oficina: Optional[str] = None


class RegistrarManutencaoRequest(BaseModel):
    tipo: TipoManutencao
    data: date
    km_atual: int
    descricao: str
    valor: float
    oficina: Optional[str] = None
    pecas_trocadas: Optional[List[str]] = None
    proxima_km: Optional[int] = None
    proxima_data: Optional[date] = None
    observacoes: Optional[str] = None


# ========================================
# Storage Simulado
# ========================================

veiculos_db: dict = {}
manutencoes_db: dict = {}


# ========================================
# Endpoints
# ========================================

@router.get("")
async def listar_veiculos(
    status: Optional[StatusVeiculo] = None,
    disponibilidade: Optional[DisponibilidadeVeiculo] = None,
    tipo: Optional[TipoVeiculo] = None,
    tipo_carroceria: Optional[TipoCarroceria] = None,
    tipo_propriedade: Optional[TipoPropriedade] = None,
    busca: Optional[str] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100)
):
    """Lista veículos com filtros"""
    try:
        veiculos = list(veiculos_db.values())
        
        # Filtros
        if status:
            veiculos = [v for v in veiculos if v["status"] == status.value]
        if disponibilidade:
            veiculos = [v for v in veiculos if v.get("disponibilidade") == disponibilidade.value]
        if tipo:
            veiculos = [v for v in veiculos if v["tipo"] == tipo.value]
        if tipo_carroceria:
            veiculos = [v for v in veiculos if v["tipo_carroceria"] == tipo_carroceria.value]
        if tipo_propriedade:
            veiculos = [v for v in veiculos if v["tipo_propriedade"] == tipo_propriedade.value]
        if busca:
            busca_upper = busca.upper()
            veiculos = [
                v for v in veiculos
                if busca_upper in v["placa"] or 
                   busca_upper in v["modelo"].upper() or
                   busca_upper in v["marca"].upper()
            ]
        
        # Ordenar por placa
        veiculos.sort(key=lambda x: x["placa"])
        
        # Paginação
        total = len(veiculos)
        start = (page - 1) * per_page
        veiculos_paginados = veiculos[start:start + per_page]
        
        return {
            "success": True,
            "data": veiculos_paginados,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "pages": (total + per_page - 1) // per_page
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar veículos: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/disponiveis")
async def listar_veiculos_disponiveis(
    tipo: Optional[TipoVeiculo] = None,
    capacidade_minima_kg: Optional[float] = None
):
    """Lista veículos disponíveis para viagem"""
    try:
        veiculos = [
            v for v in veiculos_db.values()
            if v["status"] == StatusVeiculo.ATIVO.value
            and v.get("disponibilidade") == DisponibilidadeVeiculo.DISPONIVEL.value
        ]
        
        if tipo:
            veiculos = [v for v in veiculos if v["tipo"] == tipo.value]
        if capacidade_minima_kg:
            veiculos = [v for v in veiculos if v["capacidade_kg"] >= capacidade_minima_kg]
        
        return {
            "success": True,
            "data": veiculos,
            "total": len(veiculos)
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar veículos disponíveis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/manutencao-pendente")
async def listar_manutencao_pendente(
    dias: int = Query(30, ge=1, le=180)
):
    """Lista veículos com manutenção pendente ou próxima"""
    try:
        data_limite = date.today() + timedelta(days=dias)
        alertas = []
        
        for v in veiculos_db.values():
            if v["status"] != StatusVeiculo.ATIVO.value:
                continue
            
            # Verificar última manutenção
            manutencoes = manutencoes_db.get(v["id"], [])
            for m in manutencoes:
                if m.get("proxima_data"):
                    proxima = datetime.strptime(m["proxima_data"], "%Y-%m-%d").date()
                    if proxima <= data_limite:
                        alertas.append({
                            "veiculo_id": v["id"],
                            "placa": v["placa"],
                            "modelo": v["modelo"],
                            "tipo_manutencao": m["tipo"],
                            "proxima_data": m["proxima_data"],
                            "proxima_km": m.get("proxima_km"),
                            "km_atual": v["km_atual"],
                            "dias_restantes": (proxima - date.today()).days
                        })
                
                if m.get("proxima_km") and v["km_atual"] >= m["proxima_km"] - 1000:
                    alertas.append({
                        "veiculo_id": v["id"],
                        "placa": v["placa"],
                        "modelo": v["modelo"],
                        "tipo_manutencao": m["tipo"],
                        "proxima_km": m["proxima_km"],
                        "km_atual": v["km_atual"],
                        "km_restantes": m["proxima_km"] - v["km_atual"]
                    })
        
        # Ordenar por urgência
        alertas.sort(key=lambda x: x.get("dias_restantes", 999))
        
        return {
            "success": True,
            "data": alertas,
            "total": len(alertas)
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar manutenção pendente: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documentos-vencendo")
async def listar_documentos_vencendo(
    dias: int = Query(30, ge=1, le=180)
):
    """Lista veículos com documentos vencendo"""
    try:
        data_limite = date.today() + timedelta(days=dias)
        alertas = []
        
        for v in veiculos_db.values():
            if v["status"] != StatusVeiculo.ATIVO.value:
                continue
            
            # Verificar seguro
            if v.get("seguro_validade"):
                validade = datetime.strptime(v["seguro_validade"], "%Y-%m-%d").date()
                if validade <= data_limite:
                    alertas.append({
                        "veiculo_id": v["id"],
                        "placa": v["placa"],
                        "documento": "Seguro",
                        "validade": v["seguro_validade"],
                        "dias_restantes": (validade - date.today()).days
                    })
            
            # Verificar outros documentos
            for doc in v.get("documentos", []):
                if doc.get("data_validade"):
                    validade = datetime.strptime(doc["data_validade"], "%Y-%m-%d").date()
                    if validade <= data_limite:
                        alertas.append({
                            "veiculo_id": v["id"],
                            "placa": v["placa"],
                            "documento": doc["tipo"],
                            "validade": doc["data_validade"],
                            "dias_restantes": (validade - date.today()).days
                        })
        
        alertas.sort(key=lambda x: x["dias_restantes"])
        
        return {
            "success": True,
            "data": alertas,
            "total": len(alertas)
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar documentos vencendo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/estatisticas")
async def estatisticas_veiculos():
    """Estatísticas da frota"""
    try:
        veiculos = list(veiculos_db.values())
        
        total = len(veiculos)
        por_status = {}
        por_tipo = {}
        por_propriedade = {}
        capacidade_total = 0
        
        for v in veiculos:
            por_status[v["status"]] = por_status.get(v["status"], 0) + 1
            por_tipo[v["tipo"]] = por_tipo.get(v["tipo"], 0) + 1
            por_propriedade[v["tipo_propriedade"]] = por_propriedade.get(v["tipo_propriedade"], 0) + 1
            
            if v["status"] == StatusVeiculo.ATIVO.value:
                capacidade_total += v["capacidade_kg"]
        
        # Idade média da frota
        ano_atual = date.today().year
        idades = [ano_atual - v["ano_fabricacao"] for v in veiculos if v["status"] == StatusVeiculo.ATIVO.value]
        idade_media = sum(idades) / len(idades) if idades else 0
        
        return {
            "success": True,
            "data": {
                "total": total,
                "por_status": por_status,
                "por_tipo": por_tipo,
                "por_propriedade": por_propriedade,
                "capacidade_total_kg": capacidade_total,
                "idade_media_frota": round(idade_media, 1)
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao gerar estatísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{veiculo_id}")
async def obter_veiculo(veiculo_id: str):
    """Obtém detalhes de um veículo"""
    try:
        if veiculo_id not in veiculos_db:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        
        veiculo = veiculos_db[veiculo_id]
        veiculo["manutencoes"] = manutencoes_db.get(veiculo_id, [])
        
        return {
            "success": True,
            "data": veiculo
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter veículo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("")
async def criar_veiculo(request: CriarVeiculoRequest):
    """Cadastra um novo veículo"""
    try:
        # Verificar placa duplicada
        for v in veiculos_db.values():
            if v["placa"] == request.placa:
                raise HTTPException(
                    status_code=400,
                    detail="Placa já cadastrada"
                )
        
        veiculo_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        veiculo = {
            "id": veiculo_id,
            "placa": request.placa,
            "placa_reboque": request.placa_reboque,
            "renavam": request.renavam,
            "chassi": request.chassi,
            "marca": request.marca,
            "modelo": request.modelo,
            "ano_fabricacao": request.ano_fabricacao,
            "ano_modelo": request.ano_modelo,
            "cor": request.cor,
            "tipo": request.tipo.value,
            "tipo_carroceria": request.tipo_carroceria.value,
            "tipo_propriedade": request.tipo_propriedade.value,
            "capacidade_kg": request.capacidade_kg,
            "capacidade_m3": request.capacidade_m3,
            "eixos": request.eixos,
            "km_atual": request.km_atual,
            "rntrc": request.rntrc,
            "antt": request.antt,
            "motorista_padrao_id": request.motorista_padrao_id,
            "proprietario_nome": request.proprietario_nome,
            "proprietario_documento": request.proprietario_documento,
            "valor_compra": request.valor_compra,
            "data_compra": request.data_compra.isoformat() if request.data_compra else None,
            "seguro_apolice": request.seguro_apolice,
            "seguro_validade": request.seguro_validade.isoformat() if request.seguro_validade else None,
            "seguro_valor": request.seguro_valor,
            "status": StatusVeiculo.ATIVO.value,
            "disponibilidade": DisponibilidadeVeiculo.DISPONIVEL.value,
            "observacoes": request.observacoes,
            "foto_url": request.foto_url,
            "documentos": [],
            "criado_em": now,
            "atualizado_em": now,
            "viagens_realizadas": 0,
            "km_rodados_total": 0
        }
        
        veiculos_db[veiculo_id] = veiculo
        manutencoes_db[veiculo_id] = []
        
        logger.info(f"Veículo cadastrado: {request.placa}")
        
        return {
            "success": True,
            "message": "Veículo cadastrado com sucesso",
            "data": veiculo
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar veículo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{veiculo_id}")
async def atualizar_veiculo(
    veiculo_id: str,
    request: AtualizarVeiculoRequest
):
    """Atualiza dados de um veículo"""
    try:
        if veiculo_id not in veiculos_db:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        
        veiculo = veiculos_db[veiculo_id]
        
        update_data = request.dict(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                if hasattr(value, 'value'):
                    veiculo[key] = value.value
                elif isinstance(value, date):
                    veiculo[key] = value.isoformat()
                else:
                    veiculo[key] = value
        
        veiculo["atualizado_em"] = datetime.utcnow()
        
        return {
            "success": True,
            "message": "Veículo atualizado",
            "data": veiculo
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar veículo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{veiculo_id}/km")
async def atualizar_km(
    veiculo_id: str,
    request: AtualizarKmRequest
):
    """Atualiza quilometragem do veículo"""
    try:
        if veiculo_id not in veiculos_db:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        
        veiculo = veiculos_db[veiculo_id]
        
        if request.km_atual < veiculo["km_atual"]:
            raise HTTPException(
                status_code=400,
                detail="Quilometragem não pode ser menor que a atual"
            )
        
        km_rodado = request.km_atual - veiculo["km_atual"]
        veiculo["km_atual"] = request.km_atual
        veiculo["km_rodados_total"] = veiculo.get("km_rodados_total", 0) + km_rodado
        veiculo["atualizado_em"] = datetime.utcnow()
        
        return {
            "success": True,
            "message": f"Quilometragem atualizada: {request.km_atual} km",
            "data": {
                "km_atual": veiculo["km_atual"],
                "km_rodado_neste_registro": km_rodado
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar km: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{veiculo_id}/disponibilidade")
async def atualizar_disponibilidade_veiculo(
    veiculo_id: str,
    disponibilidade: DisponibilidadeVeiculo,
    motivo: Optional[str] = None
):
    """Atualiza disponibilidade do veículo"""
    try:
        if veiculo_id not in veiculos_db:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        
        veiculo = veiculos_db[veiculo_id]
        veiculo["disponibilidade"] = disponibilidade.value
        veiculo["atualizado_em"] = datetime.utcnow()
        
        if motivo:
            veiculo["motivo_disponibilidade"] = motivo
        
        return {
            "success": True,
            "message": f"Disponibilidade alterada para {disponibilidade.value}",
            "data": veiculo
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar disponibilidade: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{veiculo_id}/manutencao")
async def registrar_manutencao(
    veiculo_id: str,
    request: RegistrarManutencaoRequest
):
    """Registra manutenção realizada"""
    try:
        if veiculo_id not in veiculos_db:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        
        veiculo = veiculos_db[veiculo_id]
        
        manutencao = {
            "id": str(uuid.uuid4()),
            "tipo": request.tipo.value,
            "data": request.data.isoformat(),
            "km_atual": request.km_atual,
            "descricao": request.descricao,
            "valor": request.valor,
            "oficina": request.oficina,
            "pecas_trocadas": request.pecas_trocadas or [],
            "proxima_km": request.proxima_km,
            "proxima_data": request.proxima_data.isoformat() if request.proxima_data else None,
            "observacoes": request.observacoes,
            "registrado_em": datetime.utcnow().isoformat()
        }
        
        if veiculo_id not in manutencoes_db:
            manutencoes_db[veiculo_id] = []
        
        manutencoes_db[veiculo_id].insert(0, manutencao)
        
        # Atualizar km do veículo se maior
        if request.km_atual > veiculo["km_atual"]:
            veiculo["km_atual"] = request.km_atual
        
        veiculo["atualizado_em"] = datetime.utcnow()
        
        logger.info(f"Manutenção registrada: {veiculo['placa']} - {request.tipo.value}")
        
        return {
            "success": True,
            "message": "Manutenção registrada com sucesso",
            "data": manutencao
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao registrar manutenção: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{veiculo_id}/manutencoes")
async def listar_manutencoes(
    veiculo_id: str,
    tipo: Optional[TipoManutencao] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100)
):
    """Lista histórico de manutenções do veículo"""
    try:
        if veiculo_id not in veiculos_db:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        
        manutencoes = manutencoes_db.get(veiculo_id, [])
        
        if tipo:
            manutencoes = [m for m in manutencoes if m["tipo"] == tipo.value]
        
        total = len(manutencoes)
        start = (page - 1) * per_page
        manutencoes_paginadas = manutencoes[start:start + per_page]
        
        return {
            "success": True,
            "data": manutencoes_paginadas,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "pages": (total + per_page - 1) // per_page
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao listar manutenções: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{veiculo_id}")
async def excluir_veiculo(veiculo_id: str):
    """Exclui (inativa) um veículo"""
    try:
        if veiculo_id not in veiculos_db:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        
        veiculo = veiculos_db[veiculo_id]
        
        # Soft delete
        veiculo["status"] = StatusVeiculo.INATIVO.value
        veiculo["disponibilidade"] = DisponibilidadeVeiculo.INDISPONIVEL.value
        veiculo["inativado_em"] = datetime.utcnow()
        veiculo["atualizado_em"] = datetime.utcnow()
        
        logger.info(f"Veículo inativado: {veiculo['placa']}")
        
        return {
            "success": True,
            "message": "Veículo inativado com sucesso"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao excluir veículo: {e}")
        raise HTTPException(status_code=500, detail=str(e))
