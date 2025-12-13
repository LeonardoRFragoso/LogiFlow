"""
LogiFlow CRM - Router Pedidos de Frete
Endpoints para gestão de pedidos/ordens de transporte
"""

from fastapi import APIRouter, HTTPException, Query, Path
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

class StatusPedido(str, Enum):
    AGUARDANDO_CONFIRMACAO = "aguardando_confirmacao"
    CONFIRMADO = "confirmado"
    AGUARDANDO_COLETA = "aguardando_coleta"
    EM_COLETA = "em_coleta"
    COLETADO = "coletado"
    EM_TRANSITO = "em_transito"
    EM_ROTA_ENTREGA = "em_rota_entrega"
    ENTREGUE = "entregue"
    ENTREGA_PARCIAL = "entrega_parcial"
    DEVOLVIDO = "devolvido"
    CANCELADO = "cancelado"


class TipoFrete(str, Enum):
    CIF = "cif"
    FOB = "fob"


class PrioridadePedido(str, Enum):
    BAIXA = "baixa"
    NORMAL = "normal"
    ALTA = "alta"
    URGENTE = "urgente"


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
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    contato_nome: Optional[str] = None
    contato_telefone: Optional[str] = None
    instrucoes: Optional[str] = None


class ItemPedido(BaseModel):
    descricao: str
    quantidade: int = Field(..., ge=1)
    peso_kg: float = Field(..., gt=0)
    volume_m3: Optional[float] = None
    valor_mercadoria: Optional[float] = None
    nf_numero: Optional[str] = None
    nf_serie: Optional[str] = None
    nf_chave: Optional[str] = None


class CriarPedidoRequest(BaseModel):
    cotacao_id: Optional[str] = None
    cliente_id: str
    cliente_nome: Optional[str] = None
    
    origem: EnderecoSchema
    destino: EnderecoSchema
    
    tipo_frete: TipoFrete = TipoFrete.CIF
    prioridade: PrioridadePedido = PrioridadePedido.NORMAL
    
    itens: List[ItemPedido] = Field(..., min_items=1)
    
    peso_total_kg: Optional[float] = None
    volume_total_m3: Optional[float] = None
    valor_mercadoria: Optional[float] = None
    
    data_coleta_prevista: Optional[datetime] = None
    data_entrega_prevista: Optional[datetime] = None
    
    motorista_id: Optional[str] = None
    veiculo_id: Optional[str] = None
    
    valor_frete: float
    valor_seguro: float = 0
    valor_pedagio: float = 0
    valor_outros: float = 0
    desconto: float = 0
    valor_total: float
    
    observacoes: Optional[str] = None
    observacoes_coleta: Optional[str] = None
    observacoes_entrega: Optional[str] = None


class AtualizarPedidoRequest(BaseModel):
    prioridade: Optional[PrioridadePedido] = None
    data_coleta_prevista: Optional[datetime] = None
    data_entrega_prevista: Optional[datetime] = None
    motorista_id: Optional[str] = None
    veiculo_id: Optional[str] = None
    observacoes: Optional[str] = None
    observacoes_coleta: Optional[str] = None
    observacoes_entrega: Optional[str] = None


class AtribuirMotoristaRequest(BaseModel):
    motorista_id: str
    veiculo_id: str
    data_coleta_prevista: Optional[datetime] = None


class RegistrarColetaRequest(BaseModel):
    data_coleta: datetime = Field(default_factory=datetime.utcnow)
    conferido_por: Optional[str] = None
    observacoes: Optional[str] = None
    fotos: Optional[List[str]] = None


class RegistrarEntregaRequest(BaseModel):
    data_entrega: datetime = Field(default_factory=datetime.utcnow)
    recebedor_nome: str
    recebedor_documento: Optional[str] = None
    assinatura_url: Optional[str] = None
    foto_comprovante_url: Optional[str] = None
    observacoes: Optional[str] = None


class CancelarPedidoRequest(BaseModel):
    motivo: str = Field(..., min_length=10)


# ========================================
# Storage Simulado
# ========================================

pedidos_db: dict = {}
pedido_counter = 5000

# Importar dados de seed
try:
    from seed_data import pedidos_db as seed_pedidos_db
    if seed_pedidos_db:
        pedidos_db.update(seed_pedidos_db)
        logger.info(f"Pedidos inicializados com {len(pedidos_db)} registros do seed")
except ImportError:
    logger.warning("seed_data não encontrado, iniciando com banco vazio")


def gerar_numero_pedido() -> str:
    global pedido_counter
    pedido_counter += 1
    ano = datetime.now().year
    return f"PED-{ano}-{pedido_counter:06d}"


def gerar_codigo_rastreio() -> str:
    """Gera código de rastreio único para o cliente"""
    import random
    import string
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=12))


# ========================================
# Endpoints
# ========================================

@router.get("")
async def listar_pedidos(
    status: Optional[StatusPedido] = None,
    cliente_id: Optional[str] = None,
    motorista_id: Optional[str] = None,
    prioridade: Optional[PrioridadePedido] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100)
):
    """Lista pedidos com filtros"""
    try:
        pedidos = list(pedidos_db.values())
        
        # Filtros
        if status:
            pedidos = [p for p in pedidos if p["status"] == status.value]
        if cliente_id:
            pedidos = [p for p in pedidos if p["cliente_id"] == cliente_id]
        if motorista_id:
            pedidos = [p for p in pedidos if p.get("motorista_id") == motorista_id]
        if prioridade:
            pedidos = [p for p in pedidos if p["prioridade"] == prioridade.value]
        if data_inicio:
            pedidos = [p for p in pedidos if p["criado_em"].date() >= data_inicio]
        if data_fim:
            pedidos = [p for p in pedidos if p["criado_em"].date() <= data_fim]
        
        # Ordenar por prioridade e data
        prioridade_ordem = {"urgente": 0, "alta": 1, "normal": 2, "baixa": 3}
        pedidos.sort(key=lambda x: (
            prioridade_ordem.get(x["prioridade"], 2),
            x["criado_em"]
        ), reverse=True)
        
        # Paginação
        total = len(pedidos)
        start = (page - 1) * per_page
        pedidos_paginados = pedidos[start:start + per_page]
        
        return {
            "success": True,
            "data": pedidos_paginados,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "pages": (total + per_page - 1) // per_page
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar pedidos: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/em-andamento")
async def listar_pedidos_em_andamento(
    motorista_id: Optional[str] = None
):
    """Lista pedidos ativos (não finalizados)"""
    try:
        status_ativos = [
            StatusPedido.CONFIRMADO.value,
            StatusPedido.AGUARDANDO_COLETA.value,
            StatusPedido.EM_COLETA.value,
            StatusPedido.COLETADO.value,
            StatusPedido.EM_TRANSITO.value,
            StatusPedido.EM_ROTA_ENTREGA.value
        ]
        
        pedidos = [
            p for p in pedidos_db.values()
            if p["status"] in status_ativos
        ]
        
        if motorista_id:
            pedidos = [p for p in pedidos if p.get("motorista_id") == motorista_id]
        
        return {
            "success": True,
            "data": pedidos,
            "total": len(pedidos)
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar pedidos em andamento: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/estatisticas")
async def estatisticas_pedidos(
    periodo_dias: int = Query(30, ge=1, le=365)
):
    """Estatísticas de pedidos"""
    try:
        data_limite = datetime.utcnow() - timedelta(days=periodo_dias)
        pedidos = [
            p for p in pedidos_db.values()
            if p["criado_em"] >= data_limite
        ]
        
        total = len(pedidos)
        entregues = len([p for p in pedidos if p["status"] == StatusPedido.ENTREGUE.value])
        cancelados = len([p for p in pedidos if p["status"] == StatusPedido.CANCELADO.value])
        em_andamento = len([p for p in pedidos if p["status"] not in [
            StatusPedido.ENTREGUE.value, StatusPedido.CANCELADO.value, StatusPedido.DEVOLVIDO.value
        ]])
        
        valor_total = sum(p.get("valor_total", 0) for p in pedidos if p["status"] == StatusPedido.ENTREGUE.value)
        
        # Tempo médio de entrega
        tempos_entrega = []
        for p in pedidos:
            if p["status"] == StatusPedido.ENTREGUE.value and p.get("entregue_em"):
                tempo = (p["entregue_em"] - p["criado_em"]).total_seconds() / 3600
                tempos_entrega.append(tempo)
        
        tempo_medio = sum(tempos_entrega) / len(tempos_entrega) if tempos_entrega else 0
        
        return {
            "success": True,
            "data": {
                "periodo_dias": periodo_dias,
                "total": total,
                "entregues": entregues,
                "cancelados": cancelados,
                "em_andamento": em_andamento,
                "valor_total_entregue": round(valor_total, 2),
                "tempo_medio_entrega_horas": round(tempo_medio, 1),
                "taxa_entrega": round((entregues / total * 100) if total > 0 else 0, 2)
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao gerar estatísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{pedido_id}")
async def obter_pedido(pedido_id: str):
    """Obtém detalhes de um pedido"""
    try:
        if pedido_id not in pedidos_db:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
        return {
            "success": True,
            "data": pedidos_db[pedido_id]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter pedido: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("")
async def criar_pedido(request: CriarPedidoRequest):
    """Cria um novo pedido de frete"""
    try:
        pedido_id = str(uuid.uuid4())
        numero = gerar_numero_pedido()
        codigo_rastreio = gerar_codigo_rastreio()
        now = datetime.utcnow()
        
        peso_total = request.peso_total_kg or sum(
            item.peso_kg * item.quantidade for item in request.itens
        )
        
        pedido = {
            "id": pedido_id,
            "numero": numero,
            "codigo_rastreio": codigo_rastreio,
            "cotacao_id": request.cotacao_id,
            "cliente_id": request.cliente_id,
            "cliente_nome": request.cliente_nome,
            "status": StatusPedido.AGUARDANDO_CONFIRMACAO.value,
            "tipo_frete": request.tipo_frete.value,
            "prioridade": request.prioridade.value,
            "origem": request.origem.dict(),
            "destino": request.destino.dict(),
            "itens": [item.dict() for item in request.itens],
            "peso_total_kg": peso_total,
            "volume_total_m3": request.volume_total_m3,
            "valor_mercadoria": request.valor_mercadoria,
            "data_coleta_prevista": request.data_coleta_prevista.isoformat() if request.data_coleta_prevista else None,
            "data_entrega_prevista": request.data_entrega_prevista.isoformat() if request.data_entrega_prevista else None,
            "motorista_id": request.motorista_id,
            "veiculo_id": request.veiculo_id,
            "valor_frete": request.valor_frete,
            "valor_seguro": request.valor_seguro,
            "valor_pedagio": request.valor_pedagio,
            "valor_outros": request.valor_outros,
            "desconto": request.desconto,
            "valor_total": request.valor_total,
            "observacoes": request.observacoes,
            "observacoes_coleta": request.observacoes_coleta,
            "observacoes_entrega": request.observacoes_entrega,
            "criado_em": now,
            "atualizado_em": now,
            "historico": [
                {
                    "data": now.isoformat(),
                    "status": StatusPedido.AGUARDANDO_CONFIRMACAO.value,
                    "descricao": "Pedido criado"
                }
            ]
        }
        
        pedidos_db[pedido_id] = pedido
        
        logger.info(f"Pedido criado: {numero}")
        
        return {
            "success": True,
            "message": "Pedido criado com sucesso",
            "data": pedido
        }
        
    except Exception as e:
        logger.error(f"Erro ao criar pedido: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{pedido_id}")
async def atualizar_pedido(
    pedido_id: str,
    request: AtualizarPedidoRequest
):
    """Atualiza um pedido"""
    try:
        if pedido_id not in pedidos_db:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
        pedido = pedidos_db[pedido_id]
        
        update_data = request.dict(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                if hasattr(value, 'value'):
                    pedido[key] = value.value
                elif isinstance(value, datetime):
                    pedido[key] = value.isoformat()
                else:
                    pedido[key] = value
        
        pedido["atualizado_em"] = datetime.utcnow()
        
        return {
            "success": True,
            "message": "Pedido atualizado",
            "data": pedido
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar pedido: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{pedido_id}/confirmar")
async def confirmar_pedido(pedido_id: str):
    """Confirma um pedido"""
    try:
        if pedido_id not in pedidos_db:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
        pedido = pedidos_db[pedido_id]
        now = datetime.utcnow()
        
        pedido["status"] = StatusPedido.CONFIRMADO.value
        pedido["confirmado_em"] = now
        pedido["atualizado_em"] = now
        pedido["historico"].append({
            "data": now.isoformat(),
            "status": StatusPedido.CONFIRMADO.value,
            "descricao": "Pedido confirmado"
        })
        
        logger.info(f"Pedido confirmado: {pedido['numero']}")
        
        return {
            "success": True,
            "message": "Pedido confirmado",
            "data": pedido
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao confirmar pedido: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{pedido_id}/atribuir-motorista")
async def atribuir_motorista(
    pedido_id: str,
    request: AtribuirMotoristaRequest
):
    """Atribui motorista e veículo ao pedido"""
    try:
        if pedido_id not in pedidos_db:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
        pedido = pedidos_db[pedido_id]
        now = datetime.utcnow()
        
        pedido["motorista_id"] = request.motorista_id
        pedido["veiculo_id"] = request.veiculo_id
        if request.data_coleta_prevista:
            pedido["data_coleta_prevista"] = request.data_coleta_prevista.isoformat()
        
        pedido["status"] = StatusPedido.AGUARDANDO_COLETA.value
        pedido["atualizado_em"] = now
        pedido["historico"].append({
            "data": now.isoformat(),
            "status": StatusPedido.AGUARDANDO_COLETA.value,
            "descricao": f"Motorista atribuído: {request.motorista_id}"
        })
        
        logger.info(f"Motorista atribuído ao pedido {pedido['numero']}")
        
        return {
            "success": True,
            "message": "Motorista atribuído com sucesso",
            "data": pedido
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atribuir motorista: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{pedido_id}/coleta")
async def registrar_coleta(
    pedido_id: str,
    request: RegistrarColetaRequest
):
    """Registra que a carga foi coletada"""
    try:
        if pedido_id not in pedidos_db:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
        pedido = pedidos_db[pedido_id]
        now = datetime.utcnow()
        
        pedido["status"] = StatusPedido.COLETADO.value
        pedido["coletado_em"] = request.data_coleta.isoformat()
        pedido["coleta_conferido_por"] = request.conferido_por
        pedido["coleta_observacoes"] = request.observacoes
        pedido["coleta_fotos"] = request.fotos
        pedido["atualizado_em"] = now
        pedido["historico"].append({
            "data": now.isoformat(),
            "status": StatusPedido.COLETADO.value,
            "descricao": "Carga coletada"
        })
        
        logger.info(f"Coleta registrada: {pedido['numero']}")
        
        return {
            "success": True,
            "message": "Coleta registrada",
            "data": pedido
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao registrar coleta: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{pedido_id}/entrega")
async def registrar_entrega(
    pedido_id: str,
    request: RegistrarEntregaRequest
):
    """Registra a entrega do pedido"""
    try:
        if pedido_id not in pedidos_db:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
        pedido = pedidos_db[pedido_id]
        now = datetime.utcnow()
        
        pedido["status"] = StatusPedido.ENTREGUE.value
        pedido["entregue_em"] = request.data_entrega
        pedido["recebedor_nome"] = request.recebedor_nome
        pedido["recebedor_documento"] = request.recebedor_documento
        pedido["assinatura_url"] = request.assinatura_url
        pedido["foto_comprovante_url"] = request.foto_comprovante_url
        pedido["entrega_observacoes"] = request.observacoes
        pedido["atualizado_em"] = now
        pedido["historico"].append({
            "data": now.isoformat(),
            "status": StatusPedido.ENTREGUE.value,
            "descricao": f"Entregue - Recebedor: {request.recebedor_nome}"
        })
        
        logger.info(f"Entrega registrada: {pedido['numero']}")
        
        return {
            "success": True,
            "message": "Entrega registrada com sucesso",
            "data": pedido
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao registrar entrega: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{pedido_id}/cancelar")
async def cancelar_pedido(
    pedido_id: str,
    request: CancelarPedidoRequest
):
    """Cancela um pedido"""
    try:
        if pedido_id not in pedidos_db:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
        pedido = pedidos_db[pedido_id]
        
        if pedido["status"] == StatusPedido.ENTREGUE.value:
            raise HTTPException(
                status_code=400,
                detail="Não é possível cancelar pedido já entregue"
            )
        
        now = datetime.utcnow()
        
        pedido["status"] = StatusPedido.CANCELADO.value
        pedido["cancelado_em"] = now
        pedido["motivo_cancelamento"] = request.motivo
        pedido["atualizado_em"] = now
        pedido["historico"].append({
            "data": now.isoformat(),
            "status": StatusPedido.CANCELADO.value,
            "descricao": f"Cancelado: {request.motivo}"
        })
        
        logger.info(f"Pedido cancelado: {pedido['numero']}")
        
        return {
            "success": True,
            "message": "Pedido cancelado",
            "data": pedido
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao cancelar pedido: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{pedido_id}/status")
async def atualizar_status_pedido(
    pedido_id: str,
    status: StatusPedido,
    observacao: Optional[str] = None
):
    """Atualiza status do pedido"""
    try:
        if pedido_id not in pedidos_db:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
        pedido = pedidos_db[pedido_id]
        now = datetime.utcnow()
        
        pedido["status"] = status.value
        pedido["atualizado_em"] = now
        pedido["historico"].append({
            "data": now.isoformat(),
            "status": status.value,
            "descricao": observacao or f"Status alterado para {status.value}"
        })
        
        return {
            "success": True,
            "message": f"Status atualizado para {status.value}",
            "data": pedido
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar status: {e}")
        raise HTTPException(status_code=500, detail=str(e))
