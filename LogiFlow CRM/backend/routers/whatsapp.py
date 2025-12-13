# LogiFlow CRM - Router WhatsApp (Evolution API)
# Endpoints para integração com WhatsApp via Evolution API

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from loguru import logger
from enum import Enum

import sys
sys.path.append('..')
from services.whatsapp_service import whatsapp_service

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
