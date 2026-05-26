"""
LogiFlow CRM - Router Rastreamento GPS
Endpoints para rastreamento de entregas e posição de motoristas
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timedelta
from enum import Enum
import logging
import uuid

logger = logging.getLogger(__name__)
router = APIRouter()


# ========================================
# Enums
# ========================================

class StatusEntrega(str, Enum):
    AGUARDANDO_COLETA = "aguardando_coleta"
    EM_COLETA = "em_coleta"
    COLETADO = "coletado"
    EM_TRANSITO = "em_transito"
    EM_ROTA_ENTREGA = "em_rota_entrega"
    ENTREGUE = "entregue"
    TENTATIVA_FALHA = "tentativa_falha"
    DEVOLVIDO = "devolvido"
    CANCELADO = "cancelado"


class TipoEvento(str, Enum):
    POSICAO_GPS = "posicao_gps"
    MUDANCA_STATUS = "mudanca_status"
    OCORRENCIA = "ocorrencia"
    COMPROVANTE = "comprovante"


# ========================================
# Schemas
# ========================================

class PosicaoGPS(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    altitude: Optional[float] = None
    velocidade: Optional[float] = Field(None, ge=0, description="km/h")
    precisao: Optional[float] = Field(None, description="Precisão em metros")
    direcao: Optional[float] = Field(None, ge=0, le=360, description="Graus")


class AtualizarPosicaoRequest(BaseModel):
    entrega_id: str = Field(..., description="ID da entrega")
    motorista_id: str = Field(..., description="ID do motorista")
    posicao: PosicaoGPS
    timestamp: Optional[datetime] = None
    bateria: Optional[int] = Field(None, ge=0, le=100, description="Nível de bateria %")
    observacao: Optional[str] = None


class AtualizarStatusRequest(BaseModel):
    entrega_id: str
    status: StatusEntrega
    motorista_id: str
    posicao: Optional[PosicaoGPS] = None
    observacao: Optional[str] = None
    foto_url: Optional[str] = None
    assinatura_url: Optional[str] = None
    recebedor_nome: Optional[str] = None
    recebedor_documento: Optional[str] = None


class RegistrarOcorrenciaRequest(BaseModel):
    entrega_id: str
    motorista_id: str
    tipo: str = Field(..., description="Tipo da ocorrência")
    descricao: str
    posicao: Optional[PosicaoGPS] = None
    fotos: Optional[List[str]] = None


class EntregaAtiva(BaseModel):
    id: str
    pedido_id: str
    cliente_nome: str
    endereco_entrega: str
    cidade: str
    uf: str
    status: StatusEntrega
    previsao_entrega: Optional[datetime] = None
    ultima_posicao: Optional[PosicaoGPS] = None
    ultima_atualizacao: Optional[datetime] = None


class EventoTracking(BaseModel):
    id: str
    tipo: TipoEvento
    timestamp: datetime
    descricao: str
    posicao: Optional[PosicaoGPS] = None
    dados: Optional[dict] = None


class TrackingPublico(BaseModel):
    codigo_rastreio: str
    status: StatusEntrega
    status_descricao: str
    previsao_entrega: Optional[datetime] = None
    ultima_atualizacao: datetime
    origem: dict
    destino: dict
    eventos: List[EventoTracking]


# ========================================
# Storage Simulado (substituir por DB real)
# ========================================

# Em produção, usar Redis ou banco de dados
posicoes_storage: dict = {}
entregas_storage: dict = {}
eventos_storage: dict = {}


def get_redis(request: Request):
    """Obtém cliente Redis do estado da aplicação"""
    if hasattr(request.app.state, 'redis'):
        return request.app.state.redis
    return None


# ========================================
# Endpoints - Posição GPS
# ========================================

@router.post("/posicao")
async def atualizar_posicao(
    request_data: AtualizarPosicaoRequest,
    request: Request
):
    """
    Atualiza posição GPS de uma entrega/motorista.
    Chamado periodicamente pelo App do Motorista.
    """
    try:
        redis = get_redis(request)
        timestamp = request_data.timestamp or datetime.utcnow()
        
        posicao_data = {
            "entrega_id": request_data.entrega_id,
            "motorista_id": request_data.motorista_id,
            "latitude": request_data.posicao.latitude,
            "longitude": request_data.posicao.longitude,
            "altitude": request_data.posicao.altitude,
            "velocidade": request_data.posicao.velocidade,
            "precisao": request_data.posicao.precisao,
            "direcao": request_data.posicao.direcao,
            "bateria": request_data.bateria,
            "timestamp": timestamp.isoformat(),
            "observacao": request_data.observacao
        }
        
        # Salvar no Redis se disponível
        if redis:
            # Última posição
            redis.hset(
                f"posicao:{request_data.entrega_id}",
                mapping={k: str(v) if v is not None else "" for k, v in posicao_data.items()}
            )
            redis.expire(f"posicao:{request_data.entrega_id}", 86400)  # 24h
            
            # Histórico (lista limitada)
            redis.lpush(
                f"historico:{request_data.entrega_id}",
                str(posicao_data)
            )
            redis.ltrim(f"historico:{request_data.entrega_id}", 0, 999)  # Últimas 1000 posições
            
            # Atualizar índice de entregas ativas do motorista
            redis.sadd(f"motorista:{request_data.motorista_id}:entregas", request_data.entrega_id)
        else:
            # Fallback para storage em memória
            posicoes_storage[request_data.entrega_id] = posicao_data
        
        logger.info(f"Posição atualizada: entrega={request_data.entrega_id}, motorista={request_data.motorista_id}")
        
        return {
            "success": True,
            "message": "Posição atualizada com sucesso",
            "timestamp": timestamp.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erro ao atualizar posição: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/posicao/{entrega_id}")
async def obter_posicao(
    entrega_id: str,
    request: Request
):
    """Obtém última posição de uma entrega"""
    try:
        redis = get_redis(request)
        
        if redis:
            posicao = redis.hgetall(f"posicao:{entrega_id}")
            if not posicao:
                raise HTTPException(status_code=404, detail="Posição não encontrada")
            return {
                "success": True,
                "data": posicao
            }
        else:
            if entrega_id not in posicoes_storage:
                raise HTTPException(status_code=404, detail="Posição não encontrada")
            return {
                "success": True,
                "data": posicoes_storage[entrega_id]
            }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter posição: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/posicao/{entrega_id}/historico")
async def obter_historico_posicoes(
    entrega_id: str,
    request: Request,
    limite: int = Query(100, ge=1, le=1000)
):
    """Obtém histórico de posições de uma entrega"""
    try:
        redis = get_redis(request)
        
        if redis:
            historico = redis.lrange(f"historico:{entrega_id}", 0, limite - 1)
            return {
                "success": True,
                "data": [eval(h) for h in historico] if historico else []
            }
        else:
            return {
                "success": True,
                "data": []
            }
            
    except Exception as e:
        logger.error(f"Erro ao obter histórico: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# Endpoints - Status de Entrega
# ========================================

@router.patch("/entrega/status")
async def atualizar_status_entrega(
    request_data: AtualizarStatusRequest,
    request: Request
):
    """
    Atualiza status de uma entrega.
    Registra evento no histórico de tracking.
    """
    try:
        redis = get_redis(request)
        timestamp = datetime.utcnow()
        
        # Criar evento de tracking
        evento = {
            "id": str(uuid.uuid4()),
            "tipo": TipoEvento.MUDANCA_STATUS.value,
            "timestamp": timestamp.isoformat(),
            "status": request_data.status.value,
            "descricao": _get_status_descricao(request_data.status),
            "motorista_id": request_data.motorista_id,
            "observacao": request_data.observacao,
            "foto_url": request_data.foto_url,
            "assinatura_url": request_data.assinatura_url,
            "recebedor_nome": request_data.recebedor_nome,
            "recebedor_documento": request_data.recebedor_documento
        }
        
        if request_data.posicao:
            evento["posicao"] = {
                "latitude": request_data.posicao.latitude,
                "longitude": request_data.posicao.longitude
            }
        
        # Salvar no Redis
        if redis:
            # Atualizar status atual
            redis.hset(f"entrega:{request_data.entrega_id}", mapping={
                "status": request_data.status.value,
                "ultima_atualizacao": timestamp.isoformat()
            })
            
            # Adicionar evento ao histórico
            redis.lpush(f"eventos:{request_data.entrega_id}", str(evento))
            
            # Se entregue, remover da lista de ativas
            if request_data.status in [StatusEntrega.ENTREGUE, StatusEntrega.DEVOLVIDO, StatusEntrega.CANCELADO]:
                redis.srem(f"motorista:{request_data.motorista_id}:entregas", request_data.entrega_id)
        else:
            eventos_storage.setdefault(request_data.entrega_id, []).insert(0, evento)
        
        logger.info(f"Status atualizado: entrega={request_data.entrega_id}, status={request_data.status}")
        
        return {
            "success": True,
            "message": f"Status atualizado para: {_get_status_descricao(request_data.status)}",
            "evento": evento
        }
        
    except Exception as e:
        logger.error(f"Erro ao atualizar status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/entrega/ocorrencia")
async def registrar_ocorrencia(
    request_data: RegistrarOcorrenciaRequest,
    request: Request
):
    """Registra uma ocorrência durante a entrega"""
    try:
        redis = get_redis(request)
        timestamp = datetime.utcnow()
        
        evento = {
            "id": str(uuid.uuid4()),
            "tipo": TipoEvento.OCORRENCIA.value,
            "timestamp": timestamp.isoformat(),
            "tipo_ocorrencia": request_data.tipo,
            "descricao": request_data.descricao,
            "motorista_id": request_data.motorista_id,
            "fotos": request_data.fotos or []
        }
        
        if request_data.posicao:
            evento["posicao"] = {
                "latitude": request_data.posicao.latitude,
                "longitude": request_data.posicao.longitude
            }
        
        if redis:
            redis.lpush(f"eventos:{request_data.entrega_id}", str(evento))
            redis.lpush(f"ocorrencias:{request_data.entrega_id}", str(evento))
        else:
            eventos_storage.setdefault(request_data.entrega_id, []).insert(0, evento)
        
        logger.info(f"Ocorrência registrada: entrega={request_data.entrega_id}, tipo={request_data.tipo}")
        
        return {
            "success": True,
            "message": "Ocorrência registrada com sucesso",
            "evento": evento
        }
        
    except Exception as e:
        logger.error(f"Erro ao registrar ocorrência: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# Endpoints - Entregas Ativas
# ========================================

@router.get("/entregas/ativas")
async def listar_entregas_ativas(
    request: Request,
    motorista_id: Optional[str] = None
):
    """
    Lista entregas ativas (em andamento).
    Filtra por motorista se informado.
    """
    try:
        redis = get_redis(request)
        entregas = []
        
        if redis:
            # Buscar entregas ativas do motorista
            if motorista_id:
                entrega_ids = redis.smembers(f"motorista:{motorista_id}:entregas")
            else:
                # TODO: Implementar índice global de entregas ativas
                entrega_ids = set()
            
            for entrega_id in entrega_ids:
                entrega_data = redis.hgetall(f"entrega:{entrega_id}")
                posicao_data = redis.hgetall(f"posicao:{entrega_id}")
                
                if entrega_data:
                    entregas.append({
                        "id": entrega_id,
                        "status": entrega_data.get("status"),
                        "ultima_atualizacao": entrega_data.get("ultima_atualizacao"),
                        "posicao": posicao_data if posicao_data else None
                    })
        
        return {
            "success": True,
            "data": entregas,
            "total": len(entregas)
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar entregas ativas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/entregas/{entrega_id}")
async def obter_entrega(
    entrega_id: str,
    request: Request
):
    """Obtém detalhes de uma entrega com posição atual"""
    try:
        redis = get_redis(request)
        
        if redis:
            entrega_data = redis.hgetall(f"entrega:{entrega_id}")
            posicao_data = redis.hgetall(f"posicao:{entrega_id}")
            eventos = redis.lrange(f"eventos:{entrega_id}", 0, 49)  # Últimos 50 eventos
            
            if not entrega_data:
                raise HTTPException(status_code=404, detail="Entrega não encontrada")
            
            return {
                "success": True,
                "data": {
                    "id": entrega_id,
                    **entrega_data,
                    "posicao_atual": posicao_data if posicao_data else None,
                    "eventos": [eval(e) for e in eventos] if eventos else []
                }
            }
        else:
            raise HTTPException(status_code=404, detail="Entrega não encontrada")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter entrega: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# Endpoints - Tracking Público (Portal Cliente)
# ========================================

@router.get("/tracking/{codigo_rastreio}")
async def tracking_publico(
    codigo_rastreio: str,
    request: Request
):
    """
    Endpoint público para rastreamento de entregas.
    Usado pelo Portal do Cliente (não requer autenticação).
    """
    try:
        redis = get_redis(request)
        
        # Buscar entrega pelo código de rastreio
        # Em produção, criar índice codigo_rastreio -> entrega_id
        entrega_id = codigo_rastreio  # Simplificado para demo
        
        if redis:
            entrega_data = redis.hgetall(f"entrega:{entrega_id}")
            eventos = redis.lrange(f"eventos:{entrega_id}", 0, 19)  # Últimos 20 eventos
            
            if not entrega_data:
                raise HTTPException(
                    status_code=404,
                    detail="Código de rastreio não encontrado"
                )
            
            status = entrega_data.get("status", "aguardando_coleta")
            
            return {
                "success": True,
                "data": {
                    "codigo_rastreio": codigo_rastreio,
                    "status": status,
                    "status_descricao": _get_status_descricao(StatusEntrega(status)),
                    "ultima_atualizacao": entrega_data.get("ultima_atualizacao"),
                    "previsao_entrega": entrega_data.get("previsao_entrega"),
                    "eventos": [
                        {
                            "data": eval(e).get("timestamp"),
                            "descricao": eval(e).get("descricao"),
                            "local": eval(e).get("posicao")
                        }
                        for e in eventos
                    ] if eventos else []
                }
            }
        else:
            # Dados de demonstração
            return {
                "success": True,
                "data": {
                    "codigo_rastreio": codigo_rastreio,
                    "status": "em_transito",
                    "status_descricao": "Em trânsito",
                    "ultima_atualizacao": datetime.utcnow().isoformat(),
                    "previsao_entrega": (datetime.utcnow() + timedelta(hours=4)).isoformat(),
                    "eventos": [
                        {
                            "data": datetime.utcnow().isoformat(),
                            "descricao": "Carga em trânsito para o destino",
                            "local": None
                        },
                        {
                            "data": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
                            "descricao": "Carga coletada",
                            "local": None
                        },
                        {
                            "data": (datetime.utcnow() - timedelta(hours=3)).isoformat(),
                            "descricao": "Pedido confirmado",
                            "local": None
                        }
                    ]
                }
            }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no tracking público: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# Endpoints - Motorista
# ========================================

@router.get("/motorista/{motorista_id}/posicao")
async def obter_posicao_motorista(
    motorista_id: str,
    request: Request
):
    """Obtém última posição conhecida de um motorista"""
    try:
        redis = get_redis(request)
        
        if redis:
            # Buscar entregas ativas do motorista
            entrega_ids = redis.smembers(f"motorista:{motorista_id}:entregas")
            
            posicoes = []
            for entrega_id in entrega_ids:
                posicao = redis.hgetall(f"posicao:{entrega_id}")
                if posicao:
                    posicoes.append({
                        "entrega_id": entrega_id,
                        **posicao
                    })
            
            if not posicoes:
                raise HTTPException(
                    status_code=404,
                    detail="Nenhuma posição encontrada para este motorista"
                )
            
            # Retornar a mais recente
            return {
                "success": True,
                "data": max(posicoes, key=lambda x: x.get("timestamp", ""))
            }
        else:
            raise HTTPException(status_code=404, detail="Posição não encontrada")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter posição do motorista: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/motorista/{motorista_id}/entregas")
async def listar_entregas_motorista(
    motorista_id: str,
    request: Request,
    status: Optional[StatusEntrega] = None
):
    """Lista entregas atribuídas a um motorista"""
    try:
        redis = get_redis(request)
        
        if redis:
            entrega_ids = redis.smembers(f"motorista:{motorista_id}:entregas")
            
            entregas = []
            for entrega_id in entrega_ids:
                entrega_data = redis.hgetall(f"entrega:{entrega_id}")
                if entrega_data:
                    if status is None or entrega_data.get("status") == status.value:
                        entregas.append({
                            "id": entrega_id,
                            **entrega_data
                        })
            
            return {
                "success": True,
                "data": entregas,
                "total": len(entregas)
            }
        else:
            return {
                "success": True,
                "data": [],
                "total": 0
            }
            
    except Exception as e:
        logger.error(f"Erro ao listar entregas do motorista: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cliente/{cliente_id}/entregas")
async def listar_entregas_cliente(
    cliente_id: str,
    request: Request,
    status: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Lista todas as entregas de um cliente.
    Endpoint para portal do cliente com histórico completo.
    """
    try:
        # Simular busca de entregas (em produção, usar banco de dados)
        entregas = []
        
        logger.info(f"✅ Entregas do cliente {cliente_id} listadas")
        
        return {
            "success": True,
            "data": entregas,
            "total": len(entregas),
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao listar entregas do cliente: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# Helpers
# ========================================

def _get_status_descricao(status: StatusEntrega) -> str:
    """Retorna descrição amigável do status"""
    descricoes = {
        StatusEntrega.AGUARDANDO_COLETA: "Aguardando coleta",
        StatusEntrega.EM_COLETA: "Motorista a caminho da coleta",
        StatusEntrega.COLETADO: "Carga coletada",
        StatusEntrega.EM_TRANSITO: "Em trânsito",
        StatusEntrega.EM_ROTA_ENTREGA: "Saiu para entrega",
        StatusEntrega.ENTREGUE: "Entregue",
        StatusEntrega.TENTATIVA_FALHA: "Tentativa de entrega sem sucesso",
        StatusEntrega.DEVOLVIDO: "Devolvido ao remetente",
        StatusEntrega.CANCELADO: "Cancelado"
    }
    return descricoes.get(status, str(status))
