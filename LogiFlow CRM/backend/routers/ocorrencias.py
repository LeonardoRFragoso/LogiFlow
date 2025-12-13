"""
LogiFlow CRM - Router Ocorrências
Endpoints para gestão de ocorrências e incidentes nas entregas
"""

from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date, timedelta
from enum import Enum
import logging
import uuid

logger = logging.getLogger(__name__)
router = APIRouter()


# ========================================
# Enums
# ========================================

class TipoOcorrencia(str, Enum):
    ATRASO = "atraso"
    AVARIA = "avaria"
    EXTRAVIO = "extravio"
    RECUSA = "recusa"
    ACIDENTE = "acidente"
    ROUBO = "roubo"
    OUTROS = "outros"


class StatusOcorrencia(str, Enum):
    ABERTA = "aberta"
    EM_ANALISE = "em_analise"
    RESOLVIDA = "resolvida"
    CANCELADA = "cancelada"


class PrioridadeOcorrencia(str, Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


# ========================================
# Schemas
# ========================================

class CriarOcorrenciaRequest(BaseModel):
    pedido_id: str
    pedido_numero: Optional[str] = None
    tipo: TipoOcorrencia
    titulo: str = Field(..., min_length=5, max_length=200)
    descricao: str = Field(..., min_length=10)
    prioridade: PrioridadeOcorrencia = PrioridadeOcorrencia.MEDIA
    data_ocorrencia: Optional[datetime] = None
    local_ocorrencia: Optional[str] = None
    motorista_id: Optional[str] = None
    veiculo_id: Optional[str] = None
    fotos: Optional[List[str]] = None
    documentos: Optional[List[str]] = None


class AtualizarOcorrenciaRequest(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    prioridade: Optional[PrioridadeOcorrencia] = None
    status: Optional[StatusOcorrencia] = None
    resolucao: Optional[str] = None


class AdicionarComentarioRequest(BaseModel):
    comentario: str = Field(..., min_length=5)
    usuario_nome: Optional[str] = None


# ========================================
# Storage Simulado
# ========================================

ocorrencias_db: dict = {}
ocorrencia_counter = 1000

# Importar dados de seed
try:
    from seed_data import ocorrencias_db as seed_ocorrencias_db
    if seed_ocorrencias_db:
        ocorrencias_db.update(seed_ocorrencias_db)
        logger.info(f"Ocorrências inicializadas com {len(ocorrencias_db)} registros do seed")
except ImportError:
    logger.warning("seed_data não encontrado, iniciando com banco vazio")


def gerar_numero_ocorrencia() -> str:
    global ocorrencia_counter
    ocorrencia_counter += 1
    ano = datetime.now().year
    return f"OCO-{ano}-{ocorrencia_counter:06d}"


# ========================================
# Endpoints
# ========================================

@router.get("")
async def listar_ocorrencias(
    status: Optional[StatusOcorrencia] = None,
    tipo: Optional[TipoOcorrencia] = None,
    prioridade: Optional[PrioridadeOcorrencia] = None,
    pedido_id: Optional[str] = None,
    motorista_id: Optional[str] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100)
):
    """Lista ocorrências com filtros"""
    try:
        ocorrencias = list(ocorrencias_db.values())
        
        # Filtros
        if status:
            ocorrencias = [o for o in ocorrencias if o["status"] == status.value]
        if tipo:
            ocorrencias = [o for o in ocorrencias if o["tipo"] == tipo.value]
        if prioridade:
            ocorrencias = [o for o in ocorrencias if o["prioridade"] == prioridade.value]
        if pedido_id:
            ocorrencias = [o for o in ocorrencias if o["pedido_id"] == pedido_id]
        if motorista_id:
            ocorrencias = [o for o in ocorrencias if o.get("motorista_id") == motorista_id]
        if data_inicio:
            ocorrencias = [o for o in ocorrencias if o["data_ocorrencia"].date() >= data_inicio]
        if data_fim:
            ocorrencias = [o for o in ocorrencias if o["data_ocorrencia"].date() <= data_fim]
        
        # Ordenar por prioridade e data
        prioridade_ordem = {"critica": 0, "alta": 1, "media": 2, "baixa": 3}
        ocorrencias.sort(key=lambda x: (
            prioridade_ordem.get(x["prioridade"], 2),
            x["criado_em"]
        ), reverse=True)
        
        # Paginação
        total = len(ocorrencias)
        start = (page - 1) * per_page
        ocorrencias_paginadas = ocorrencias[start:start + per_page]
        
        return {
            "success": True,
            "data": ocorrencias_paginadas,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "pages": (total + per_page - 1) // per_page
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar ocorrências: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/abertas")
async def listar_ocorrencias_abertas():
    """Lista ocorrências abertas (não resolvidas)"""
    try:
        ocorrencias = [
            o for o in ocorrencias_db.values()
            if o["status"] in [StatusOcorrencia.ABERTA.value, StatusOcorrencia.EM_ANALISE.value]
        ]
        
        return {
            "success": True,
            "data": ocorrencias,
            "total": len(ocorrencias)
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar ocorrências abertas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/estatisticas")
async def estatisticas_ocorrencias(
    periodo_dias: int = Query(30, ge=1, le=365)
):
    """Estatísticas de ocorrências"""
    try:
        data_limite = datetime.utcnow() - timedelta(days=periodo_dias)
        ocorrencias = [
            o for o in ocorrencias_db.values()
            if o["criado_em"] >= data_limite
        ]
        
        total = len(ocorrencias)
        abertas = len([o for o in ocorrencias if o["status"] == StatusOcorrencia.ABERTA.value])
        em_analise = len([o for o in ocorrencias if o["status"] == StatusOcorrencia.EM_ANALISE.value])
        resolvidas = len([o for o in ocorrencias if o["status"] == StatusOcorrencia.RESOLVIDA.value])
        
        # Por tipo
        por_tipo = {}
        for tipo in TipoOcorrencia:
            por_tipo[tipo.value] = len([o for o in ocorrencias if o["tipo"] == tipo.value])
        
        # Por prioridade
        por_prioridade = {}
        for prioridade in PrioridadeOcorrencia:
            por_prioridade[prioridade.value] = len([o for o in ocorrencias if o["prioridade"] == prioridade.value])
        
        # Tempo médio de resolução
        tempos_resolucao = []
        for o in ocorrencias:
            if o["status"] == StatusOcorrencia.RESOLVIDA.value and o.get("resolvida_em"):
                tempo = (o["resolvida_em"] - o["criado_em"]).total_seconds() / 3600
                tempos_resolucao.append(tempo)
        
        tempo_medio = sum(tempos_resolucao) / len(tempos_resolucao) if tempos_resolucao else 0
        
        return {
            "success": True,
            "data": {
                "periodo_dias": periodo_dias,
                "total": total,
                "abertas": abertas,
                "em_analise": em_analise,
                "resolvidas": resolvidas,
                "por_tipo": por_tipo,
                "por_prioridade": por_prioridade,
                "tempo_medio_resolucao_horas": round(tempo_medio, 1),
                "taxa_resolucao": round((resolvidas / total * 100) if total > 0 else 0, 2)
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao gerar estatísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{ocorrencia_id}")
async def obter_ocorrencia(ocorrencia_id: str):
    """Obtém detalhes de uma ocorrência"""
    try:
        if ocorrencia_id not in ocorrencias_db:
            raise HTTPException(status_code=404, detail="Ocorrência não encontrada")
        
        return {
            "success": True,
            "data": ocorrencias_db[ocorrencia_id]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter ocorrência: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("")
async def criar_ocorrencia(request: CriarOcorrenciaRequest):
    """Cria uma nova ocorrência"""
    try:
        ocorrencia_id = str(uuid.uuid4())
        numero = gerar_numero_ocorrencia()
        now = datetime.utcnow()
        
        ocorrencia = {
            "id": ocorrencia_id,
            "numero": numero,
            "pedido_id": request.pedido_id,
            "pedido_numero": request.pedido_numero,
            "tipo": request.tipo.value,
            "titulo": request.titulo,
            "descricao": request.descricao,
            "prioridade": request.prioridade.value,
            "status": StatusOcorrencia.ABERTA.value,
            "data_ocorrencia": request.data_ocorrencia or now,
            "local_ocorrencia": request.local_ocorrencia,
            "motorista_id": request.motorista_id,
            "veiculo_id": request.veiculo_id,
            "fotos": request.fotos or [],
            "documentos": request.documentos or [],
            "comentarios": [],
            "criado_em": now,
            "atualizado_em": now,
            "historico": [
                {
                    "data": now.isoformat(),
                    "status": StatusOcorrencia.ABERTA.value,
                    "descricao": "Ocorrência criada"
                }
            ]
        }
        
        ocorrencias_db[ocorrencia_id] = ocorrencia
        
        logger.info(f"Ocorrência criada: {numero}")
        
        return {
            "success": True,
            "message": "Ocorrência criada com sucesso",
            "data": ocorrencia
        }
        
    except Exception as e:
        logger.error(f"Erro ao criar ocorrência: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{ocorrencia_id}")
async def atualizar_ocorrencia(
    ocorrencia_id: str,
    request: AtualizarOcorrenciaRequest
):
    """Atualiza uma ocorrência"""
    try:
        if ocorrencia_id not in ocorrencias_db:
            raise HTTPException(status_code=404, detail="Ocorrência não encontrada")
        
        ocorrencia = ocorrencias_db[ocorrencia_id]
        now = datetime.utcnow()
        
        update_data = request.dict(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                if hasattr(value, 'value'):
                    ocorrencia[key] = value.value
                else:
                    ocorrencia[key] = value
        
        ocorrencia["atualizado_em"] = now
        
        if request.status and request.status.value != ocorrencia["status"]:
            ocorrencia["historico"].append({
                "data": now.isoformat(),
                "status": request.status.value,
                "descricao": f"Status alterado para {request.status.value}"
            })
        
        return {
            "success": True,
            "message": "Ocorrência atualizada",
            "data": ocorrencia
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar ocorrência: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{ocorrencia_id}/comentarios")
async def adicionar_comentario(
    ocorrencia_id: str,
    request: AdicionarComentarioRequest
):
    """Adiciona um comentário à ocorrência"""
    try:
        if ocorrencia_id not in ocorrencias_db:
            raise HTTPException(status_code=404, detail="Ocorrência não encontrada")
        
        ocorrencia = ocorrencias_db[ocorrencia_id]
        now = datetime.utcnow()
        
        comentario = {
            "id": str(uuid.uuid4()),
            "comentario": request.comentario,
            "usuario_nome": request.usuario_nome or "Sistema",
            "criado_em": now.isoformat()
        }
        
        ocorrencia["comentarios"].append(comentario)
        ocorrencia["atualizado_em"] = now
        
        return {
            "success": True,
            "message": "Comentário adicionado",
            "data": comentario
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao adicionar comentário: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{ocorrencia_id}/resolver")
async def resolver_ocorrencia(
    ocorrencia_id: str,
    resolucao: str = Body(..., min_length=10, embed=True)
):
    """Marca ocorrência como resolvida"""
    try:
        if ocorrencia_id not in ocorrencias_db:
            raise HTTPException(status_code=404, detail="Ocorrência não encontrada")
        
        ocorrencia = ocorrencias_db[ocorrencia_id]
        now = datetime.utcnow()
        
        ocorrencia["status"] = StatusOcorrencia.RESOLVIDA.value
        ocorrencia["resolucao"] = resolucao
        ocorrencia["resolvida_em"] = now
        ocorrencia["atualizado_em"] = now
        ocorrencia["historico"].append({
            "data": now.isoformat(),
            "status": StatusOcorrencia.RESOLVIDA.value,
            "descricao": f"Ocorrência resolvida: {resolucao}"
        })
        
        logger.info(f"Ocorrência resolvida: {ocorrencia['numero']}")
        
        return {
            "success": True,
            "message": "Ocorrência resolvida",
            "data": ocorrencia
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao resolver ocorrência: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{ocorrencia_id}/status")
async def atualizar_status_ocorrencia(
    ocorrencia_id: str,
    status: StatusOcorrencia,
    observacao: Optional[str] = None
):
    """Atualiza status da ocorrência"""
    try:
        if ocorrencia_id not in ocorrencias_db:
            raise HTTPException(status_code=404, detail="Ocorrência não encontrada")
        
        ocorrencia = ocorrencias_db[ocorrencia_id]
        now = datetime.utcnow()
        
        ocorrencia["status"] = status.value
        ocorrencia["atualizado_em"] = now
        ocorrencia["historico"].append({
            "data": now.isoformat(),
            "status": status.value,
            "descricao": observacao or f"Status alterado para {status.value}"
        })
        
        if status == StatusOcorrencia.RESOLVIDA:
            ocorrencia["resolvida_em"] = now
        
        return {
            "success": True,
            "message": f"Status atualizado para {status.value}",
            "data": ocorrencia
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar status: {e}")
        raise HTTPException(status_code=500, detail=str(e))
