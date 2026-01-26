# LogiFlow CRM - WhatsApp Service (Evolution API)
# Serviço para envio de mensagens via WhatsApp usando Evolution API

import httpx
from typing import Optional, Dict, Any, List
from datetime import datetime
from loguru import logger
from config import settings

class WhatsAppService:
    """
    Serviço de integração com Evolution API para WhatsApp
    Documentação: https://doc.evolution-api.com/
    """
    
    def __init__(self, api_url: str = None, api_key: str = None, instance_name: str = None):
        """
        Args:
            api_url: URL da Evolution API (ex: https://api.evolution-api.com)
            api_key: Chave de API da Evolution
            instance_name: Nome da instância
        """
        # Se não passar parâmetros, usa settings (fallback para compat.)
        self.base_url = api_url or getattr(settings, 'EVOLUTION_API_URL', "http://localhost:8080")
        self.api_key = api_key or getattr(settings, 'EVOLUTION_API_KEY', "")
        self.instance_name = instance_name or getattr(settings, 'EVOLUTION_INSTANCE_NAME', "logiflow")
        self.timeout = 30.0
        
    @property
    def headers(self) -> Dict[str, str]:
        return {
            "apikey": self.api_key,
            "Content-Type": "application/json"
        }
    
    # ==========================================
    # Gerenciamento de Instância
    # ==========================================
    
    async def criar_instancia(self) -> Dict[str, Any]:
        """Cria uma nova instância do WhatsApp"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/instance/create",
                    headers=self.headers,
                    json={
                        "instanceName": self.instance_name,
                        "qrcode": True,
                        "integration": "WHATSAPP-BAILEYS"
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Erro ao criar instância: {e}")
            return {"error": str(e)}
    
    async def obter_qrcode(self) -> Dict[str, Any]:
        """Obtém o QR Code para conectar o WhatsApp"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/instance/connect/{self.instance_name}",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Erro ao obter QR Code: {e}")
            return {"error": str(e)}
    
    async def verificar_conexao(self) -> Dict[str, Any]:
        """Verifica o status da conexão do WhatsApp"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/instance/connectionState/{self.instance_name}",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Erro ao verificar conexão: {e}")
            return {"error": str(e), "state": "disconnected"}
    
    async def desconectar(self) -> Dict[str, Any]:
        """Desconecta a instância do WhatsApp"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.delete(
                    f"{self.base_url}/instance/logout/{self.instance_name}",
                    headers=self.headers
                )
                response.raise_for_status()
                return {"success": True}
        except Exception as e:
            logger.error(f"Erro ao desconectar: {e}")
            return {"error": str(e)}
    
    # ==========================================
    # Envio de Mensagens
    # ==========================================
    
    async def enviar_texto(
        self, 
        telefone: str, 
        mensagem: str,
        delay: int = 1200
    ) -> Dict[str, Any]:
        """
        Envia mensagem de texto simples
        
        Args:
            telefone: Número com DDD (ex: 11999999999)
            mensagem: Texto da mensagem
            delay: Delay em ms antes de enviar (simula digitação)
        """
        numero = self._formatar_numero(telefone)
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/message/sendText/{self.instance_name}",
                    headers=self.headers,
                    json={
                        "number": numero,
                        "text": mensagem,
                        "delay": delay
                    }
                )
                response.raise_for_status()
                logger.info(f"Mensagem enviada para {numero}")
                return {"success": True, "data": response.json()}
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem para {numero}: {e}")
            return {"success": False, "error": str(e)}
    
    async def enviar_imagem(
        self,
        telefone: str,
        imagem_url: str,
        caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """Envia imagem com legenda opcional"""
        numero = self._formatar_numero(telefone)
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/message/sendMedia/{self.instance_name}",
                    headers=self.headers,
                    json={
                        "number": numero,
                        "mediatype": "image",
                        "media": imagem_url,
                        "caption": caption or ""
                    }
                )
                response.raise_for_status()
                return {"success": True, "data": response.json()}
        except Exception as e:
            logger.error(f"Erro ao enviar imagem: {e}")
            return {"success": False, "error": str(e)}
    
    async def enviar_documento(
        self,
        telefone: str,
        documento_url: str,
        nome_arquivo: str,
        caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """Envia documento (PDF, etc)"""
        numero = self._formatar_numero(telefone)
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/message/sendMedia/{self.instance_name}",
                    headers=self.headers,
                    json={
                        "number": numero,
                        "mediatype": "document",
                        "media": documento_url,
                        "fileName": nome_arquivo,
                        "caption": caption or ""
                    }
                )
                response.raise_for_status()
                return {"success": True, "data": response.json()}
        except Exception as e:
            logger.error(f"Erro ao enviar documento: {e}")
            return {"success": False, "error": str(e)}
    
    async def enviar_localizacao(
        self,
        telefone: str,
        latitude: float,
        longitude: float,
        nome: Optional[str] = None,
        endereco: Optional[str] = None
    ) -> Dict[str, Any]:
        """Envia localização no mapa"""
        numero = self._formatar_numero(telefone)
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/message/sendLocation/{self.instance_name}",
                    headers=self.headers,
                    json={
                        "number": numero,
                        "latitude": latitude,
                        "longitude": longitude,
                        "name": nome or "Localização",
                        "address": endereco or ""
                    }
                )
                response.raise_for_status()
                return {"success": True, "data": response.json()}
        except Exception as e:
            logger.error(f"Erro ao enviar localização: {e}")
            return {"success": False, "error": str(e)}
    
    # ==========================================
    # Templates de Notificação LogiFlow
    # ==========================================
    
    async def notificar_pedido_confirmado(
        self,
        telefone: str,
        cliente_nome: str,
        pedido_numero: str,
        codigo_rastreio: str,
        previsao_entrega: str
    ) -> Dict[str, Any]:
        """Template: Pedido confirmado"""
        mensagem = f"""🚛 *LogiFlow - Pedido Confirmado!*

Olá, {cliente_nome}!

Seu pedido foi confirmado e está sendo preparado para envio.

📦 *Pedido:* {pedido_numero}
🔍 *Rastreio:* {codigo_rastreio}
📅 *Previsão:* {previsao_entrega}

Acompanhe sua entrega em tempo real:
🔗 https://logiflow.com.br/tracking/{codigo_rastreio}

Obrigado por escolher a LogiFlow! 💙"""
        
        return await self.enviar_texto(telefone, mensagem)
    
    async def notificar_coleta_realizada(
        self,
        telefone: str,
        cliente_nome: str,
        pedido_numero: str,
        motorista_nome: str
    ) -> Dict[str, Any]:
        """Template: Carga coletada"""
        mensagem = f"""📦 *LogiFlow - Carga Coletada!*

Olá, {cliente_nome}!

Sua carga foi coletada e está a caminho do destino.

📦 *Pedido:* {pedido_numero}
🚚 *Motorista:* {motorista_nome}

Em breve você receberá atualizações sobre a entrega! 🚛"""
        
        return await self.enviar_texto(telefone, mensagem)
    
    async def notificar_em_transito(
        self,
        telefone: str,
        cliente_nome: str,
        pedido_numero: str,
        cidade_atual: str,
        previsao_entrega: str
    ) -> Dict[str, Any]:
        """Template: Em trânsito"""
        mensagem = f"""🚛 *LogiFlow - Carga em Trânsito*

Olá, {cliente_nome}!

Sua carga está em trânsito.

📦 *Pedido:* {pedido_numero}
📍 *Localização:* {cidade_atual}
📅 *Previsão:* {previsao_entrega}

Fique tranquilo, estamos cuidando da sua entrega! 💙"""
        
        return await self.enviar_texto(telefone, mensagem)
    
    async def notificar_saiu_entrega(
        self,
        telefone: str,
        cliente_nome: str,
        pedido_numero: str,
        motorista_nome: str,
        motorista_telefone: str,
        placa_veiculo: str
    ) -> Dict[str, Any]:
        """Template: Saiu para entrega"""
        mensagem = f"""🎉 *LogiFlow - Saiu para Entrega!*

Olá, {cliente_nome}!

Boa notícia! Sua encomenda saiu para entrega e chegará em breve.

📦 *Pedido:* {pedido_numero}
🚚 *Motorista:* {motorista_nome}
📞 *Contato:* {motorista_telefone}
🚗 *Veículo:* {placa_veiculo}

Por favor, esteja disponível para receber! 📍"""
        
        return await self.enviar_texto(telefone, mensagem)
    
    async def notificar_entrega_realizada(
        self,
        telefone: str,
        cliente_nome: str,
        pedido_numero: str,
        recebedor_nome: str,
        data_entrega: str
    ) -> Dict[str, Any]:
        """Template: Entrega realizada"""
        mensagem = f"""✅ *LogiFlow - Entrega Realizada!*

Olá, {cliente_nome}!

Sua encomenda foi entregue com sucesso! 🎉

📦 *Pedido:* {pedido_numero}
👤 *Recebido por:* {recebedor_nome}
📅 *Data/Hora:* {data_entrega}

Obrigado por confiar na LogiFlow!
Esperamos vê-lo novamente em breve. 💙

⭐ Avalie nossa entrega:
https://logiflow.com.br/avaliar/{pedido_numero}"""
        
        return await self.enviar_texto(telefone, mensagem)
    
    async def notificar_ocorrencia(
        self,
        telefone: str,
        cliente_nome: str,
        pedido_numero: str,
        tipo_ocorrencia: str,
        descricao: str,
        acao_tomada: str
    ) -> Dict[str, Any]:
        """Template: Ocorrência registrada"""
        mensagem = f"""⚠️ *LogiFlow - Ocorrência Registrada*

Olá, {cliente_nome}!

Informamos que houve uma ocorrência com sua entrega:

📦 *Pedido:* {pedido_numero}
⚠️ *Tipo:* {tipo_ocorrencia}
📝 *Descrição:* {descricao}
✅ *Ação:* {acao_tomada}

Nossa equipe está trabalhando para resolver o mais rápido possível.

Em caso de dúvidas, entre em contato:
📞 (11) 99999-9999"""
        
        return await self.enviar_texto(telefone, mensagem)
    
    async def notificar_tentativa_entrega(
        self,
        telefone: str,
        cliente_nome: str,
        pedido_numero: str,
        motivo: str,
        nova_tentativa: str
    ) -> Dict[str, Any]:
        """Template: Tentativa de entrega sem sucesso"""
        mensagem = f"""❌ *LogiFlow - Tentativa sem Sucesso*

Olá, {cliente_nome}!

Tentamos entregar sua encomenda, mas não foi possível.

📦 *Pedido:* {pedido_numero}
📝 *Motivo:* {motivo}
🔄 *Nova tentativa:* {nova_tentativa}

Por favor, certifique-se de que haverá alguém no local para receber.

Precisa reagendar? Responda esta mensagem ou ligue:
📞 (11) 99999-9999"""
        
        return await self.enviar_texto(telefone, mensagem)
    
    async def enviar_codigo_rastreio(
        self,
        telefone: str,
        cliente_nome: str,
        pedido_numero: str,
        codigo_rastreio: str
    ) -> Dict[str, Any]:
        """Template: Envio de código de rastreio"""
        mensagem = f"""🔍 *LogiFlow - Código de Rastreio*

Olá, {cliente_nome}!

Aqui está o código para rastrear seu pedido:

📦 *Pedido:* {pedido_numero}
🔍 *Código:* `{codigo_rastreio}`

Acompanhe em tempo real:
🔗 https://logiflow.com.br/tracking/{codigo_rastreio}

Basta clicar no link ou digitar o código no nosso site! 📱"""
        
        return await self.enviar_texto(telefone, mensagem)
    
    # ==========================================
    # Mensagens para Motoristas
    # ==========================================
    
    async def notificar_motorista_nova_entrega(
        self,
        telefone: str,
        motorista_nome: str,
        pedido_numero: str,
        cliente_nome: str,
        endereco_entrega: str,
        cidade: str,
        observacoes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Template: Nova entrega atribuída ao motorista"""
        obs_text = f"\n📝 *Obs:* {observacoes}" if observacoes else ""
        
        mensagem = f"""🚛 *LogiFlow - Nova Entrega!*

Olá, {motorista_nome}!

Uma nova entrega foi atribuída a você:

📦 *Pedido:* {pedido_numero}
👤 *Cliente:* {cliente_nome}
📍 *Endereço:* {endereco_entrega}
🏙️ *Cidade:* {cidade}{obs_text}

Acesse o app para mais detalhes e iniciar a rota! 📱"""
        
        return await self.enviar_texto(telefone, mensagem)
    
    # ==========================================
    # Utilitários
    # ==========================================
    
    def _formatar_numero(self, telefone: str) -> str:
        """
        Formata número para padrão WhatsApp
        Input: 11999999999 ou (11) 99999-9999
        Output: 5511999999999
        """
        # Remove caracteres não numéricos
        numero = ''.join(filter(str.isdigit, telefone))
        
        # Adiciona código do país se não tiver
        if len(numero) == 11:  # DDD + 9 dígitos
            numero = f"55{numero}"
        elif len(numero) == 10:  # DDD + 8 dígitos (fixo)
            numero = f"55{numero}"
        
        return numero


# Instância global do serviço (deprecated - use get_whatsapp_service_for_tenant)
whatsapp_service = WhatsAppService()


def get_whatsapp_service_for_tenant(tenant_id: int, db) -> Optional[WhatsAppService]:
    """
    Obtém WhatsAppService configurado para o tenant
    
    Args:
        tenant_id: ID do tenant
        db: Sessão do banco
        
    Returns:
        WhatsAppService configurado ou None se não configurado
    """
    from services.integration_manager import get_evolution_api_client
    
    config = get_evolution_api_client(tenant_id, db)
    
    if not config:
        logger.warning(f"Evolution API não configurado para tenant {tenant_id}")
        return None
    
    return WhatsAppService(
        api_url=config["api_url"],
        api_key=config["api_key"],
        instance_name=config["instance_name"]
    )
