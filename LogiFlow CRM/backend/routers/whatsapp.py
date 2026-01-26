# LogiFlow CRM - Router WhatsApp (Evolution API)
# Endpoints para integração com WhatsApp via Evolution API

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Request, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from loguru import logger
from enum import Enum
from sqlalchemy.orm import Session
import uuid

import sys
sys.path.append('..')
from services.whatsapp_service import whatsapp_service
from services.chatbot_service import get_chatbot_service
from database import get_db
from models.whatsapp_message import (
    WhatsAppMessage, WhatsAppConversation, WhatsAppConfig,
    MessageDirection, MessageType, MessageStatus
)

router = APIRouter()


# ===========================================
# Schemas
# ===========================================

class TipoNotificacao(str, Enum):
    PEDIDO_CONFIRMADO = "pedido_confirmado"
    COLETA_REALIZADA = "coleta_realizada"
    EM_TRANSITO = "em_transito"
    SAIU_ENTREGA = "saiu_entrega"
    ENTREGUE = "entregue"
    OCORRENCIA = "ocorrencia"
    TENTATIVA_FALHA = "tentativa_falha"


class MensagemTexto(BaseModel):
    telefone: str = Field(..., description="Telefone com DDD (ex: 11999999999)")
    mensagem: str = Field(..., description="Texto da mensagem")


class MensagemImagem(BaseModel):
    telefone: str
    imagem_url: str
    legenda: Optional[str] = None


class MensagemDocumento(BaseModel):
    telefone: str
    documento_url: str
    nome_arquivo: str
    legenda: Optional[str] = None


class MensagemLocalizacao(BaseModel):
    telefone: str
    latitude: float
    longitude: float
    nome: Optional[str] = None
    endereco: Optional[str] = None


class NotificacaoPedido(BaseModel):
    telefone: str
    cliente_nome: str
    pedido_numero: str
    tipo: TipoNotificacao
    # Campos opcionais dependendo do tipo
    codigo_rastreio: Optional[str] = None
    previsao_entrega: Optional[str] = None
    motorista_nome: Optional[str] = None
    motorista_telefone: Optional[str] = None
    placa_veiculo: Optional[str] = None
    cidade_atual: Optional[str] = None
    recebedor_nome: Optional[str] = None
    data_entrega: Optional[str] = None
    tipo_ocorrencia: Optional[str] = None
    descricao: Optional[str] = None
    acao_tomada: Optional[str] = None
    motivo: Optional[str] = None
    nova_tentativa: Optional[str] = None


class NotificacaoMotorista(BaseModel):
    telefone: str
    motorista_nome: str
    pedido_numero: str
    cliente_nome: str
    endereco_entrega: str
    cidade: str
    observacoes: Optional[str] = None


class EnvioMassa(BaseModel):
    telefones: List[str]
    mensagem: str
    intervalo_segundos: int = Field(default=5, ge=1, le=60)


# ===========================================
# Endpoints - Gerenciamento da Instância
# ===========================================

@router.get("/status")
async def verificar_status():
    """Verifica o status da conexão com WhatsApp"""
    resultado = await whatsapp_service.verificar_conexao()
    return {
        "success": "error" not in resultado,
        "data": resultado,
        "timestamp": datetime.now().isoformat()
    }


@router.post("/instancia/criar")
async def criar_instancia():
    """Cria uma nova instância do WhatsApp"""
    resultado = await whatsapp_service.criar_instancia()
    return {
        "success": "error" not in resultado,
        "data": resultado,
        "message": "Instância criada. Use /qrcode para conectar."
    }


@router.get("/qrcode")
async def obter_qrcode():
    """Obtém o QR Code para conectar o WhatsApp"""
    resultado = await whatsapp_service.obter_qrcode()
    
    if "error" in resultado:
        raise HTTPException(status_code=500, detail=resultado["error"])
    
    return {
        "success": True,
        "data": resultado,
        "instrucoes": "Escaneie o QR Code com seu WhatsApp (Configurações > Dispositivos Conectados)"
    }


@router.post("/desconectar")
async def desconectar():
    """Desconecta a instância do WhatsApp"""
    resultado = await whatsapp_service.desconectar()
    return {
        "success": "error" not in resultado,
        "data": resultado
    }


# ===========================================
# Endpoints - Envio de Mensagens
# ===========================================

@router.post("/enviar/texto")
async def enviar_texto(dados: MensagemTexto):
    """Envia mensagem de texto simples"""
    resultado = await whatsapp_service.enviar_texto(
        telefone=dados.telefone,
        mensagem=dados.mensagem
    )
    
    if not resultado.get("success"):
        raise HTTPException(status_code=500, detail=resultado.get("error", "Erro ao enviar"))
    
    return resultado


@router.post("/enviar/imagem")
async def enviar_imagem(dados: MensagemImagem):
    """Envia imagem com legenda opcional"""
    resultado = await whatsapp_service.enviar_imagem(
        telefone=dados.telefone,
        imagem_url=dados.imagem_url,
        caption=dados.legenda
    )
    
    if not resultado.get("success"):
        raise HTTPException(status_code=500, detail=resultado.get("error", "Erro ao enviar"))
    
    return resultado


@router.post("/enviar/documento")
async def enviar_documento(dados: MensagemDocumento):
    """Envia documento (PDF, etc)"""
    resultado = await whatsapp_service.enviar_documento(
        telefone=dados.telefone,
        documento_url=dados.documento_url,
        nome_arquivo=dados.nome_arquivo,
        caption=dados.legenda
    )
    
    if not resultado.get("success"):
        raise HTTPException(status_code=500, detail=resultado.get("error", "Erro ao enviar"))
    
    return resultado


@router.post("/enviar/localizacao")
async def enviar_localizacao(dados: MensagemLocalizacao):
    """Envia localização no mapa"""
    resultado = await whatsapp_service.enviar_localizacao(
        telefone=dados.telefone,
        latitude=dados.latitude,
        longitude=dados.longitude,
        nome=dados.nome,
        endereco=dados.endereco
    )
    
    if not resultado.get("success"):
        raise HTTPException(status_code=500, detail=resultado.get("error", "Erro ao enviar"))
    
    return resultado


# ===========================================
# Endpoints - Notificações Automáticas
# ===========================================

@router.post("/notificar/pedido")
async def notificar_pedido(dados: NotificacaoPedido, background_tasks: BackgroundTasks):
    """
    Envia notificação automática baseada no status do pedido
    
    Tipos disponíveis:
    - pedido_confirmado
    - coleta_realizada
    - em_transito
    - saiu_entrega
    - entregue
    - ocorrencia
    - tentativa_falha
    """
    
    async def enviar_notificacao():
        resultado = None
        
        if dados.tipo == TipoNotificacao.PEDIDO_CONFIRMADO:
            resultado = await whatsapp_service.notificar_pedido_confirmado(
                telefone=dados.telefone,
                cliente_nome=dados.cliente_nome,
                pedido_numero=dados.pedido_numero,
                codigo_rastreio=dados.codigo_rastreio or "N/A",
                previsao_entrega=dados.previsao_entrega or "Em breve"
            )
        
        elif dados.tipo == TipoNotificacao.COLETA_REALIZADA:
            resultado = await whatsapp_service.notificar_coleta_realizada(
                telefone=dados.telefone,
                cliente_nome=dados.cliente_nome,
                pedido_numero=dados.pedido_numero,
                motorista_nome=dados.motorista_nome or "Motorista"
            )
        
        elif dados.tipo == TipoNotificacao.EM_TRANSITO:
            resultado = await whatsapp_service.notificar_em_transito(
                telefone=dados.telefone,
                cliente_nome=dados.cliente_nome,
                pedido_numero=dados.pedido_numero,
                cidade_atual=dados.cidade_atual or "Em trânsito",
                previsao_entrega=dados.previsao_entrega or "Em breve"
            )
        
        elif dados.tipo == TipoNotificacao.SAIU_ENTREGA:
            resultado = await whatsapp_service.notificar_saiu_entrega(
                telefone=dados.telefone,
                cliente_nome=dados.cliente_nome,
                pedido_numero=dados.pedido_numero,
                motorista_nome=dados.motorista_nome or "Motorista",
                motorista_telefone=dados.motorista_telefone or "",
                placa_veiculo=dados.placa_veiculo or ""
            )
        
        elif dados.tipo == TipoNotificacao.ENTREGUE:
            resultado = await whatsapp_service.notificar_entrega_realizada(
                telefone=dados.telefone,
                cliente_nome=dados.cliente_nome,
                pedido_numero=dados.pedido_numero,
                recebedor_nome=dados.recebedor_nome or "Destinatário",
                data_entrega=dados.data_entrega or datetime.now().strftime("%d/%m/%Y %H:%M")
            )
        
        elif dados.tipo == TipoNotificacao.OCORRENCIA:
            resultado = await whatsapp_service.notificar_ocorrencia(
                telefone=dados.telefone,
                cliente_nome=dados.cliente_nome,
                pedido_numero=dados.pedido_numero,
                tipo_ocorrencia=dados.tipo_ocorrencia or "Ocorrência",
                descricao=dados.descricao or "Sem descrição",
                acao_tomada=dados.acao_tomada or "Em análise"
            )
        
        elif dados.tipo == TipoNotificacao.TENTATIVA_FALHA:
            resultado = await whatsapp_service.notificar_tentativa_entrega(
                telefone=dados.telefone,
                cliente_nome=dados.cliente_nome,
                pedido_numero=dados.pedido_numero,
                motivo=dados.motivo or "Destinatário ausente",
                nova_tentativa=dados.nova_tentativa or "Em breve"
            )
        
        if resultado:
            logger.info(f"Notificação {dados.tipo} enviada para {dados.telefone}")
        
        return resultado
    
    # Executa em background para não bloquear a requisição
    background_tasks.add_task(enviar_notificacao)
    
    return {
        "success": True,
        "message": f"Notificação '{dados.tipo}' agendada para envio",
        "telefone": dados.telefone,
        "pedido": dados.pedido_numero
    }


@router.post("/notificar/motorista")
async def notificar_motorista(dados: NotificacaoMotorista, background_tasks: BackgroundTasks):
    """Notifica motorista sobre nova entrega atribuída"""
    
    async def enviar():
        return await whatsapp_service.notificar_motorista_nova_entrega(
            telefone=dados.telefone,
            motorista_nome=dados.motorista_nome,
            pedido_numero=dados.pedido_numero,
            cliente_nome=dados.cliente_nome,
            endereco_entrega=dados.endereco_entrega,
            cidade=dados.cidade,
            observacoes=dados.observacoes
        )
    
    background_tasks.add_task(enviar)
    
    return {
        "success": True,
        "message": "Notificação para motorista agendada",
        "motorista": dados.motorista_nome,
        "pedido": dados.pedido_numero
    }


@router.post("/enviar/codigo-rastreio")
async def enviar_codigo_rastreio(
    telefone: str,
    cliente_nome: str,
    pedido_numero: str,
    codigo_rastreio: str
):
    """Envia código de rastreio para o cliente"""
    resultado = await whatsapp_service.enviar_codigo_rastreio(
        telefone=telefone,
        cliente_nome=cliente_nome,
        pedido_numero=pedido_numero,
        codigo_rastreio=codigo_rastreio
    )
    
    return resultado


# ===========================================
# Endpoints - Envio em Massa
# ===========================================

@router.post("/enviar/massa")
async def enviar_em_massa(dados: EnvioMassa, background_tasks: BackgroundTasks):
    """
    Envia mensagem para múltiplos números
    
    ATENÇÃO: Use com moderação para evitar bloqueio do WhatsApp
    Recomendado intervalo mínimo de 5 segundos entre mensagens
    """
    import asyncio
    
    async def enviar_todas():
        resultados = []
        for i, telefone in enumerate(dados.telefones):
            resultado = await whatsapp_service.enviar_texto(telefone, dados.mensagem)
            resultados.append({"telefone": telefone, "resultado": resultado})
            
            # Aguarda intervalo entre mensagens (exceto última)
            if i < len(dados.telefones) - 1:
                await asyncio.sleep(dados.intervalo_segundos)
        
        logger.info(f"Envio em massa concluído: {len(resultados)} mensagens")
        return resultados
    
    background_tasks.add_task(enviar_todas)
    
    return {
        "success": True,
        "message": f"Envio em massa iniciado para {len(dados.telefones)} números",
        "intervalo_segundos": dados.intervalo_segundos,
        "tempo_estimado_minutos": round((len(dados.telefones) * dados.intervalo_segundos) / 60, 1)
    }


# ===========================================
# Webhook para receber mensagens
# ===========================================

@router.post("/webhook")
async def webhook_evolution(payload: dict):
    """
    Webhook para receber eventos da Evolution API
    Configure na Evolution: POST para /whatsapp/webhook
    """
    event = payload.get("event")
    
    logger.info(f"Webhook recebido: {event}")
    
    # Processar diferentes tipos de eventos
    if event == "messages.upsert":
        # Nova mensagem recebida
        messages = payload.get("data", {}).get("messages", [])
        for msg in messages:
            if not msg.get("key", {}).get("fromMe"):
                # Mensagem recebida de cliente
                from_number = msg.get("key", {}).get("remoteJid", "").replace("@s.whatsapp.net", "")
                text = msg.get("message", {}).get("conversation", "")
                logger.info(f"Mensagem recebida de {from_number}: {text}")
                
                # Aqui você pode implementar auto-resposta ou encaminhar para atendimento
    
    elif event == "connection.update":
        # Status de conexão atualizado
        state = payload.get("data", {}).get("state")
        logger.info(f"Status de conexão: {state}")
    
    return {"received": True, "event": event}


# ===========================================
# Endpoints - Histórico e Conversas
# ===========================================

@router.get("/conversas")
async def listar_conversas(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    archived: Optional[bool] = None,
    unread_only: bool = False
):
    """Lista todas as conversas WhatsApp"""
    try:
        tenant_id = getattr(request.state, "tenant_id", "default")
        
        query = db.query(WhatsAppConversation).filter(
            WhatsAppConversation.tenant_id == tenant_id
        )
        
        if archived is not None:
            query = query.filter(WhatsAppConversation.is_archived == archived)
        
        if unread_only:
            query = query.filter(WhatsAppConversation.unread_count > 0)
        
        total = query.count()
        
        conversas = query.order_by(
            WhatsAppConversation.last_message_at.desc()
        ).offset((page - 1) * limit).limit(limit).all()
        
        return {
            "success": True,
            "data": [conv.to_dict() for conv in conversas],
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }
    except Exception as e:
        logger.error(f"Erro ao listar conversas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversas/{conversa_id}/mensagens")
async def obter_mensagens_conversa(
    conversa_id: str,
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(100, ge=1, le=200)
):
    """Obtém mensagens de uma conversa específica"""
    try:
        tenant_id = getattr(request.state, "tenant_id", "default")
        
        query = db.query(WhatsAppMessage).filter(
            WhatsAppMessage.tenant_id == tenant_id,
            WhatsAppMessage.conversation_id == conversa_id
        )
        
        total = query.count()
        
        mensagens = query.order_by(
            WhatsAppMessage.timestamp.asc()
        ).offset((page - 1) * limit).limit(limit).all()
        
        return {
            "success": True,
            "data": [msg.to_dict() for msg in mensagens],
            "total": total,
            "page": page,
            "limit": limit
        }
    except Exception as e:
        logger.error(f"Erro ao obter mensagens: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mensagens")
async def listar_mensagens(
    request: Request,
    db: Session = Depends(get_db),
    phone_number: Optional[str] = None,
    direction: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100)
):
    """Lista mensagens com filtros"""
    try:
        tenant_id = getattr(request.state, "tenant_id", "default")
        
        query = db.query(WhatsAppMessage).filter(
            WhatsAppMessage.tenant_id == tenant_id
        )
        
        if phone_number:
            query = query.filter(
                (WhatsAppMessage.from_number == phone_number) |
                (WhatsAppMessage.to_number == phone_number)
            )
        
        if direction:
            query = query.filter(WhatsAppMessage.direction == direction)
        
        if date_from:
            date_from_dt = datetime.strptime(date_from, "%Y-%m-%d")
            query = query.filter(WhatsAppMessage.timestamp >= date_from_dt)
        
        if date_to:
            date_to_dt = datetime.strptime(date_to, "%Y-%m-%d")
            query = query.filter(WhatsAppMessage.timestamp <= date_to_dt)
        
        total = query.count()
        
        mensagens = query.order_by(
            WhatsAppMessage.timestamp.desc()
        ).offset((page - 1) * limit).limit(limit).all()
        
        return {
            "success": True,
            "data": [msg.to_dict() for msg in mensagens],
            "total": total,
            "page": page,
            "limit": limit
        }
    except Exception as e:
        logger.error(f"Erro ao listar mensagens: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conversas/{conversa_id}/marcar-lida")
async def marcar_conversa_lida(
    conversa_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Marca todas as mensagens de uma conversa como lidas"""
    try:
        tenant_id = getattr(request.state, "tenant_id", "default")
        
        conversa = db.query(WhatsAppConversation).filter(
            WhatsAppConversation.id == conversa_id,
            WhatsAppConversation.tenant_id == tenant_id
        ).first()
        
        if not conversa:
            raise HTTPException(status_code=404, detail="Conversa não encontrada")
        
        conversa.unread_count = 0
        db.commit()
        
        return {"success": True, "message": "Conversa marcada como lida"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao marcar conversa como lida: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/conversas/{conversa_id}/arquivar")
async def arquivar_conversa(
    conversa_id: str,
    request: Request,
    db: Session = Depends(get_db),
    arquivar: bool = True
):
    """Arquiva ou desarquiva uma conversa"""
    try:
        tenant_id = getattr(request.state, "tenant_id", "default")
        
        conversa = db.query(WhatsAppConversation).filter(
            WhatsAppConversation.id == conversa_id,
            WhatsAppConversation.tenant_id == tenant_id
        ).first()
        
        if not conversa:
            raise HTTPException(status_code=404, detail="Conversa não encontrada")
        
        conversa.is_archived = arquivar
        db.commit()
        
        return {
            "success": True,
            "message": f"Conversa {'arquivada' if arquivar else 'desarquivada'}"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao arquivar conversa: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================
# Endpoints - Configurações
# ===========================================

@router.get("/config")
async def obter_configuracao(
    request: Request,
    db: Session = Depends(get_db)
):
    """Obtém configuração WhatsApp do tenant"""
    try:
        tenant_id = getattr(request.state, "tenant_id", "default")
        
        config = db.query(WhatsAppConfig).filter(
            WhatsAppConfig.tenant_id == tenant_id
        ).first()
        
        if not config:
            # Criar configuração padrão
            config = WhatsAppConfig(
                id=str(uuid.uuid4()),
                tenant_id=tenant_id,
                chatbot_welcome_message="Olá! Bem-vindo à LogiFlow! Como posso ajudar?"
            )
            db.add(config)
            db.commit()
            db.refresh(config)
        
        return {
            "success": True,
            "data": config.to_dict()
        }
    except Exception as e:
        logger.error(f"Erro ao obter configuração: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class ConfigWhatsAppRequest(BaseModel):
    chatbot_enabled: Optional[bool] = None
    chatbot_welcome_message: Optional[str] = None
    chatbot_auto_reply: Optional[bool] = None
    chatbot_business_hours_only: Optional[bool] = None
    business_hours_start: Optional[str] = None
    business_hours_end: Optional[str] = None
    business_days: Optional[List[str]] = None
    out_of_hours_message: Optional[str] = None
    auto_notify_pedido_confirmado: Optional[bool] = None
    auto_notify_coleta_realizada: Optional[bool] = None
    auto_notify_em_transito: Optional[bool] = None
    auto_notify_saiu_entrega: Optional[bool] = None
    auto_notify_entregue: Optional[bool] = None
    auto_notify_ocorrencia: Optional[bool] = None


@router.put("/config")
async def atualizar_configuracao(
    request: Request,
    config_data: ConfigWhatsAppRequest,
    db: Session = Depends(get_db)
):
    """Atualiza configuração WhatsApp"""
    try:
        tenant_id = getattr(request.state, "tenant_id", "default")
        
        config = db.query(WhatsAppConfig).filter(
            WhatsAppConfig.tenant_id == tenant_id
        ).first()
        
        if not config:
            config = WhatsAppConfig(
                id=str(uuid.uuid4()),
                tenant_id=tenant_id
            )
            db.add(config)
        
        for key, value in config_data.dict(exclude_unset=True).items():
            setattr(config, key, value)
        
        config.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(config)
        
        return {
            "success": True,
            "message": "Configuração atualizada",
            "data": config.to_dict()
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao atualizar configuração: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status-conexao")
async def verificar_status_conexao(request: Request, db: Session = Depends(get_db)):
    """Verifica status da conexão WhatsApp"""
    try:
        tenant_id = getattr(request.state, "tenant_id", "default")
        
        status = await whatsapp_service.verificar_conexao()
        
        # Atualizar no banco
        config = db.query(WhatsAppConfig).filter(
            WhatsAppConfig.tenant_id == tenant_id
        ).first()
        
        if config:
            config.is_connected = status.get("state") == "open"
            config.connection_status = status.get("state")
            config.last_connection_check = datetime.utcnow()
            db.commit()
        
        return {
            "success": True,
            "connected": status.get("state") == "open",
            "status": status
        }
    except Exception as e:
        logger.error(f"Erro ao verificar conexão: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================
# Endpoints - Dashboard e Métricas
# ===========================================

@router.get("/dashboard")
async def dashboard_whatsapp(
    request: Request,
    db: Session = Depends(get_db),
    date_from: Optional[str] = None,
    date_to: Optional[str] = None
):
    """Dashboard com métricas WhatsApp"""
    try:
        tenant_id = getattr(request.state, "tenant_id", "default")
        
        now = datetime.utcnow()
        date_from_dt = datetime.strptime(date_from, "%Y-%m-%d") if date_from else datetime(now.year, now.month, 1)
        date_to_dt = datetime.strptime(date_to, "%Y-%m-%d") if date_to else now
        
        query = db.query(WhatsAppMessage).filter(
            WhatsAppMessage.tenant_id == tenant_id,
            WhatsAppMessage.timestamp >= date_from_dt,
            WhatsAppMessage.timestamp <= date_to_dt
        )
        
        total_mensagens = query.count()
        mensagens_enviadas = query.filter(WhatsAppMessage.direction == MessageDirection.OUTBOUND).count()
        mensagens_recebidas = query.filter(WhatsAppMessage.direction == MessageDirection.INBOUND).count()
        mensagens_bot = query.filter(WhatsAppMessage.is_bot_message == True).count()
        
        total_conversas = db.query(WhatsAppConversation).filter(
            WhatsAppConversation.tenant_id == tenant_id,
            WhatsAppConversation.last_message_at >= date_from_dt,
            WhatsAppConversation.last_message_at <= date_to_dt
        ).count()
        
        conversas_ativas = db.query(WhatsAppConversation).filter(
            WhatsAppConversation.tenant_id == tenant_id,
            WhatsAppConversation.is_active == True,
            WhatsAppConversation.is_archived == False
        ).count()
        
        conversas_nao_lidas = db.query(WhatsAppConversation).filter(
            WhatsAppConversation.tenant_id == tenant_id,
            WhatsAppConversation.unread_count > 0
        ).count()
        
        return {
            "success": True,
            "data": {
                "periodo": {
                    "inicio": date_from_dt.isoformat(),
                    "fim": date_to_dt.isoformat()
                },
                "mensagens": {
                    "total": total_mensagens,
                    "enviadas": mensagens_enviadas,
                    "recebidas": mensagens_recebidas,
                    "bot": mensagens_bot,
                    "taxa_bot": round((mensagens_bot / total_mensagens * 100) if total_mensagens > 0 else 0, 2)
                },
                "conversas": {
                    "total_periodo": total_conversas,
                    "ativas": conversas_ativas,
                    "nao_lidas": conversas_nao_lidas
                }
            }
        }
    except Exception as e:
        logger.error(f"Erro ao gerar dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================
# Webhook Melhorado com Chatbot
# ===========================================

@router.post("/webhook/enhanced")
async def webhook_evolution_enhanced(
    payload: dict,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Webhook avançado com processamento de chatbot e histórico
    """
    event = payload.get("event")
    tenant_id = getattr(request.state, "tenant_id", "default")
    
    logger.info(f"Webhook enhanced recebido: {event}")
    
    async def processar_webhook():
        try:
            if event == "messages.upsert":
                messages = payload.get("data", {}).get("messages", [])
                
                for msg in messages:
                    if not msg.get("key", {}).get("fromMe"):
                        # Mensagem recebida de cliente
                        from_number = msg.get("key", {}).get("remoteJid", "").replace("@s.whatsapp.net", "")
                        message_text = msg.get("message", {}).get("conversation", "")
                        message_id = msg.get("key", {}).get("id", "")
                        
                        if not message_text:
                            continue
                        
                        # Salvar mensagem recebida
                        conversa_id = _obter_ou_criar_conversa(db, tenant_id, from_number)
                        
                        mensagem_db = WhatsAppMessage(
                            id=str(uuid.uuid4()),
                            tenant_id=tenant_id,
                            message_id=message_id,
                            conversation_id=conversa_id,
                            direction=MessageDirection.INBOUND,
                            message_type=MessageType.TEXT,
                            status=MessageStatus.DELIVERED,
                            from_number=from_number,
                            to_number=whatsapp_service.instance_name,
                            content=message_text,
                            timestamp=datetime.utcnow()
                        )
                        db.add(mensagem_db)
                        
                        # Processar com chatbot
                        chatbot = get_chatbot_service(db, tenant_id)
                        bot_response = chatbot.processar_mensagem(message_text, from_number)
                        
                        # Atualizar mensagem com dados do bot
                        mensagem_db.bot_intent = bot_response["intent"]
                        mensagem_db.bot_confidence = bot_response["confidence"]
                        mensagem_db.bot_response = bot_response["response"]
                        
                        db.commit()
                        
                        # Enviar resposta automática se habilitado
                        config = db.query(WhatsAppConfig).filter(
                            WhatsAppConfig.tenant_id == tenant_id
                        ).first()
                        
                        if config and config.chatbot_enabled and bot_response["response"]:
                            # Verificar horário comercial
                            is_business_hours, out_message = chatbot.verificar_horario_comercial()
                            
                            response_text = bot_response["response"]
                            if not is_business_hours and out_message:
                                response_text = out_message
                            
                            # Enviar resposta
                            await whatsapp_service.enviar_texto(from_number, response_text)
                            
                            # Salvar resposta enviada
                            resposta_db = WhatsAppMessage(
                                id=str(uuid.uuid4()),
                                tenant_id=tenant_id,
                                message_id=f"bot_{uuid.uuid4()}",
                                conversation_id=conversa_id,
                                direction=MessageDirection.OUTBOUND,
                                message_type=MessageType.TEXT,
                                status=MessageStatus.SENT,
                                from_number=whatsapp_service.instance_name,
                                to_number=from_number,
                                content=response_text,
                                is_bot_message=True,
                                timestamp=datetime.utcnow()
                            )
                            db.add(resposta_db)
                        
                        # Atualizar conversa
                        _atualizar_conversa(db, conversa_id, message_text, MessageDirection.INBOUND)
                        
                        db.commit()
                        
                        logger.info(f"Mensagem processada de {from_number} com intent: {bot_response['intent']}")
        
        except Exception as e:
            logger.error(f"Erro ao processar webhook: {e}")
            db.rollback()
    
    background_tasks.add_task(processar_webhook)
    
    return {"received": True, "event": event, "processing": "background"}


def _obter_ou_criar_conversa(db: Session, tenant_id: str, phone_number: str) -> str:
    """Obtém ou cria uma conversa"""
    conversa = db.query(WhatsAppConversation).filter(
        WhatsAppConversation.tenant_id == tenant_id,
        WhatsAppConversation.phone_number == phone_number
    ).first()
    
    if not conversa:
        conversa = WhatsAppConversation(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            phone_number=phone_number,
            is_active=True
        )
        db.add(conversa)
        db.commit()
    
    return conversa.id


def _atualizar_conversa(db: Session, conversa_id: str, mensagem: str, direction: MessageDirection):
    """Atualiza estatísticas da conversa"""
    conversa = db.query(WhatsAppConversation).filter(
        WhatsAppConversation.id == conversa_id
    ).first()
    
    if conversa:
        conversa.total_messages += 1
        conversa.last_message_content = mensagem[:200]
        conversa.last_message_at = datetime.utcnow()
        conversa.last_message_direction = direction
        
        if direction == MessageDirection.INBOUND:
            conversa.unread_count += 1
        
        db.commit()
