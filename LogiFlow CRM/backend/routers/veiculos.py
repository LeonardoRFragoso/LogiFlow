"""
LogiFlow CRM - Router Veículos
Endpoints para gestão de frota de veículos
"""

from fastapi import APIRouter, HTTPException, Query, Path, Request, Depends
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date, timedelta
from enum import Enum
from sqlalchemy.orm import Session
import logging
import uuid
import re

from database import get_db
from models import Veiculo
from middleware.tenant import get_current_tenant_id
from loguru import logger

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
# Schemas - Simplificados para MVP (campos planos)
# ========================================

class VeiculoBase(BaseModel):
    """Schema base com campos planos para compatibilidade com frontend"""
    # Identificação
    placa: str
    renavam: Optional[str] = None
    chassi: Optional[str] = None
    
    # Características
    marca: Optional[str] = None
    modelo: Optional[str] = None
    ano_fabricacao: Optional[int] = None
    ano_modelo: Optional[int] = None
    cor: Optional[str] = None
    
    # Tipo
    tipo: Optional[str] = "truck"
    tipo_carroceria: Optional[str] = "bau"
    tipo_propriedade: Optional[str] = "proprio"
    
    # Capacidade
    capacidade_kg: Optional[float] = None
    capacidade_m3: Optional[float] = None
    eixos: Optional[int] = 2
    km_atual: Optional[int] = 0
    
    # Documentação
    rntrc: Optional[str] = None
    antt: Optional[str] = None
    
    # Propriedade
    proprietario_nome: Optional[str] = None
    proprietario_documento: Optional[str] = None
    
    # Documentos e Seguro
    licenciamento_validade: Optional[str] = None
    seguro_apolice: Optional[str] = None
    seguro_validade: Optional[str] = None
    seguro_valor: Optional[float] = None
    
    # Status
    status: Optional[str] = "ativo"
    disponibilidade: Optional[str] = "disponivel"
    
    # Outros
    observacoes: Optional[str] = None
    foto_url: Optional[str] = None
    motorista_padrao_id: Optional[int] = None


class CriarVeiculoRequest(VeiculoBase):
    """Request para criar veículo"""
    placa: str  # Obrigatório


class AtualizarVeiculoRequest(BaseModel):
    """Request para atualizar veículo - todos campos opcionais"""
    placa: Optional[str] = None
    renavam: Optional[str] = None
    chassi: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    ano_fabricacao: Optional[int] = None
    ano_modelo: Optional[int] = None
    cor: Optional[str] = None
    tipo: Optional[str] = None
    tipo_carroceria: Optional[str] = None
    tipo_propriedade: Optional[str] = None
    capacidade_kg: Optional[float] = None
    capacidade_m3: Optional[float] = None
    eixos: Optional[int] = None
    km_atual: Optional[int] = None
    rntrc: Optional[str] = None
    antt: Optional[str] = None
    proprietario_nome: Optional[str] = None
    licenciamento_validade: Optional[str] = None
    seguro_apolice: Optional[str] = None
    seguro_validade: Optional[str] = None
    seguro_valor: Optional[float] = None
    status: Optional[str] = None
    disponibilidade: Optional[str] = None
    observacoes: Optional[str] = None
    foto_url: Optional[str] = None
    motorista_padrao_id: Optional[int] = None


class VeiculoResponse(BaseModel):
    """Response de veículo"""
    id: int
    placa: str
    renavam: Optional[str] = None
    chassi: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    ano_fabricacao: Optional[int] = None
    ano_modelo: Optional[int] = None
    cor: Optional[str] = None
    tipo: Optional[str] = None
    tipo_carroceria: Optional[str] = None
    tipo_propriedade: Optional[str] = None
    capacidade_kg: Optional[float] = None
    capacidade_m3: Optional[float] = None
    eixos: Optional[int] = None
    km_atual: Optional[int] = None
    status: Optional[str] = None
    disponibilidade: Optional[str] = None
    licenciamento_validade: Optional[str] = None
    seguro_validade: Optional[str] = None
    observacoes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AtualizarKmRequest(BaseModel):
    km_atual: int
    data_registro: Optional[datetime] = None
    observacao: Optional[str] = None


class AgendarManutencaoRequest(BaseModel):
    tipo: str
    data_agendada: date
    km_atual: Optional[int] = None
    descricao: str
    valor_estimado: Optional[float] = None
    oficina: Optional[str] = None


class RegistrarManutencaoRequest(BaseModel):
    tipo: str
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
    request: Request,
    status: Optional[StatusVeiculo] = None,
    disponibilidade: Optional[DisponibilidadeVeiculo] = None,
    tipo: Optional[TipoVeiculo] = None,
    tipo_carroceria: Optional[TipoCarroceria] = None,
    tipo_propriedade: Optional[TipoPropriedade] = None,
    busca: Optional[str] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Lista veículos do tenant atual com filtros"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        # Construir query base filtrando por tenant
        query = db.query(Veiculo).filter(Veiculo.tenant_id == tenant_id)
        
        # Aplicar filtros adicionais
        if status:
            query = query.filter(Veiculo.status == status.value)
        if disponibilidade:
            query = query.filter(Veiculo.disponibilidade == disponibilidade.value)
        if tipo:
            query = query.filter(Veiculo.tipo == tipo.value)
        if tipo_carroceria:
            query = query.filter(Veiculo.tipo_carroceria == tipo_carroceria.value)
        if tipo_propriedade:
            query = query.filter(Veiculo.tipo_propriedade == tipo_propriedade.value)
        if busca:
            query = query.filter(
                (Veiculo.placa.ilike(f"%{busca}%")) |
                (Veiculo.modelo.ilike(f"%{busca}%")) |
                (Veiculo.marca.ilike(f"%{busca}%"))
            )
        
        # Ordenar por placa
        query = query.order_by(Veiculo.placa)
        
        # Paginação
        total = query.count()
        veiculos = query.offset((page - 1) * per_page).limit(per_page).all()
        
        logger.info(f"✅ Listados {len(veiculos)} veículos do tenant {tenant_id}")
        
        return {
            "success": True,
            "data": veiculos,
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
        logger.error(f"❌ Erro ao listar veículos: {e}")
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


@router.get("/{veiculo_id}", response_model=VeiculoResponse)
async def obter_veiculo(
    veiculo_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Obtém detalhes de um veículo"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        veiculo = db.query(Veiculo).filter(
            Veiculo.id == veiculo_id,
            Veiculo.tenant_id == tenant_id
        ).first()
        
        if not veiculo:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        
        return veiculo
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao obter veículo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=VeiculoResponse)
async def criar_veiculo(
    veiculo_data: CriarVeiculoRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Cadastra um novo veículo"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        # Verificar placa duplicada
        existing = db.query(Veiculo).filter(
            Veiculo.placa == veiculo_data.placa.upper(),
            Veiculo.tenant_id == tenant_id
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="Placa já cadastrada")
        
        veiculo = Veiculo(
            placa=veiculo_data.placa.upper(),
            renavam=veiculo_data.renavam,
            chassi=veiculo_data.chassi,
            marca=veiculo_data.marca,
            modelo=veiculo_data.modelo,
            ano_fabricacao=veiculo_data.ano_fabricacao,
            ano_modelo=veiculo_data.ano_modelo,
            cor=veiculo_data.cor,
            tipo=veiculo_data.tipo,
            tipo_carroceria=veiculo_data.tipo_carroceria,
            tipo_propriedade=veiculo_data.tipo_propriedade,
            capacidade_kg=veiculo_data.capacidade_kg,
            capacidade_m3=veiculo_data.capacidade_m3,
            eixos=veiculo_data.eixos or 2,
            km_atual=veiculo_data.km_atual or 0,
            rntrc=veiculo_data.rntrc,
            antt=veiculo_data.antt,
            proprietario_nome=veiculo_data.proprietario_nome,
            licenciamento_validade=veiculo_data.licenciamento_validade,
            seguro_apolice=veiculo_data.seguro_apolice,
            seguro_validade=veiculo_data.seguro_validade,
            seguro_valor=veiculo_data.seguro_valor,
            status=veiculo_data.status or "ativo",
            disponibilidade=veiculo_data.disponibilidade or "disponivel",
            observacoes=veiculo_data.observacoes,
            foto_url=veiculo_data.foto_url,
            motorista_padrao_id=veiculo_data.motorista_padrao_id,
            tenant_id=tenant_id
        )
        
        db.add(veiculo)
        db.commit()
        db.refresh(veiculo)
        
        logger.info(f"✅ Veículo cadastrado: {veiculo.placa} (ID: {veiculo.id})")
        
        return veiculo
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao criar veículo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{veiculo_id}", response_model=VeiculoResponse)
async def atualizar_veiculo(
    veiculo_id: int,
    veiculo_data: AtualizarVeiculoRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Atualiza dados de um veículo"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        veiculo = db.query(Veiculo).filter(
            Veiculo.id == veiculo_id,
            Veiculo.tenant_id == tenant_id
        ).first()
        
        if not veiculo:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        
        update_data = veiculo_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None and hasattr(veiculo, key):
                setattr(veiculo, key, value)
        
        db.commit()
        db.refresh(veiculo)
        
        logger.info(f"✅ Veículo atualizado: {veiculo.placa}")
        
        return veiculo
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao atualizar veículo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{veiculo_id}/km")
async def atualizar_km(
    veiculo_id: int,
    km_data: AtualizarKmRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Atualiza quilometragem do veículo"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        veiculo = db.query(Veiculo).filter(
            Veiculo.id == veiculo_id,
            Veiculo.tenant_id == tenant_id
        ).first()
        
        if not veiculo:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        
        if km_data.km_atual < (veiculo.km_atual or 0):
            raise HTTPException(
                status_code=400,
                detail="Quilometragem não pode ser menor que a atual"
            )
        
        km_anterior = veiculo.km_atual or 0
        veiculo.km_atual = km_data.km_atual
        db.commit()
        
        return {
            "success": True,
            "message": f"Quilometragem atualizada: {km_data.km_atual} km",
            "data": {
                "km_atual": veiculo.km_atual,
                "km_rodado_neste_registro": km_data.km_atual - km_anterior
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao atualizar km: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{veiculo_id}/disponibilidade")
async def atualizar_disponibilidade_veiculo(
    veiculo_id: int,
    disponibilidade: str,
    request: Request,
    db: Session = Depends(get_db),
    motivo: Optional[str] = None
):
    """Atualiza disponibilidade do veículo"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        veiculo = db.query(Veiculo).filter(
            Veiculo.id == veiculo_id,
            Veiculo.tenant_id == tenant_id
        ).first()
        
        if not veiculo:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        
        veiculo.disponibilidade = disponibilidade
        db.commit()
        
        return {
            "success": True,
            "message": f"Disponibilidade alterada para {disponibilidade}",
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
            "tipo": request.tipo,
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
        
        logger.info(f"Manutenção registrada: {veiculo['placa']} - {request.tipo}")
        
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
