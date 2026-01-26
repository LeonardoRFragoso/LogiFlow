"""
LogiFlow CRM - Chatbot Service
Chatbot inteligente para WhatsApp com reconhecimento de intenções
"""

import re
from typing import Dict, Tuple, Optional, List
from datetime import datetime
from loguru import logger
from sqlalchemy.orm import Session


class ChatbotService:
    """Serviço de chatbot com reconhecimento de intenções"""
    
    def __init__(self, db: Session, tenant_id: str):
        self.db = db
        self.tenant_id = tenant_id
        
        # Palavras-chave por intenção
        self.intents = {
            "rastreamento": ["rastreio", "rastrear", "onde está", "localização", "tracking", "código"],
            "status_pedido": ["status", "situação", "andamento", "pedido", "entrega"],
            "prazo": ["prazo", "quanto tempo", "quando chega", "previsão", "data entrega"],
            "cancelamento": ["cancelar", "desistir", "não quero mais"],
            "duvida": ["dúvida", "duvida", "ajuda", "help", "suporte"],
            "horario": ["horário", "horario", "atendimento", "funciona"],
            "preco": ["preço", "preco", "valor", "quanto custa", "cotação", "orçamento"],
            "saudacao": ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite", "hey", "ola"],
            "agradecimento": ["obrigado", "obrigada", "valeu", "agradeco", "thanks"],
            "despedida": ["tchau", "até logo", "ate logo", "adeus", "bye"]
        }
        
        # Padrões de extração
        self.patterns = {
            "codigo_rastreio": r"\b[A-Z]{2}\d{9}[A-Z]{2}\b|\b\d{13}\b",
            "numero_pedido": r"(?:pedido|order|#)\s*(\d+)",
            "telefone": r"\(?\d{2}\)?\s*9?\d{4}[-\s]?\d{4}",
            "cpf": r"\d{3}\.?\d{3}\.?\d{3}-?\d{2}",
            "cnpj": r"\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}"
        }
    
    def processar_mensagem(self, mensagem: str, from_number: str) -> Dict:
        """
        Processa mensagem recebida e gera resposta do bot
        
        Returns:
            Dict com intent, confidence, response, data
        """
        mensagem_lower = mensagem.lower().strip()
        
        # Detectar intenção
        intent, confidence = self._detectar_intencao(mensagem_lower)
        
        # Extrair dados da mensagem
        extracted_data = self._extrair_dados(mensagem)
        
        # Gerar resposta
        response = self._gerar_resposta(intent, extracted_data, from_number)
        
        # Executar ação se necessário
        action_result = self._executar_acao(intent, extracted_data, from_number)
        
        return {
            "intent": intent,
            "confidence": confidence,
            "response": response,
            "extracted_data": extracted_data,
            "action_result": action_result,
            "requires_human": confidence < 60 or intent == "duvida"
        }
    
    def _detectar_intencao(self, mensagem: str) -> Tuple[str, int]:
        """Detecta a intenção da mensagem usando palavras-chave"""
        scores = {}
        
        for intent, keywords in self.intents.items():
            score = 0
            for keyword in keywords:
                if keyword in mensagem:
                    # Palavra exata vale mais
                    if re.search(r'\b' + re.escape(keyword) + r'\b', mensagem):
                        score += 10
                    else:
                        score += 5
            
            if score > 0:
                scores[intent] = score
        
        if not scores:
            return "desconhecido", 0
        
        # Intenção com maior score
        best_intent = max(scores, key=scores.get)
        max_score = scores[best_intent]
        
        # Converter para confiança (0-100)
        confidence = min(max_score * 10, 100)
        
        return best_intent, confidence
    
    def _extrair_dados(self, mensagem: str) -> Dict:
        """Extrai dados estruturados da mensagem"""
        dados = {}
        
        for nome, pattern in self.patterns.items():
            match = re.search(pattern, mensagem, re.IGNORECASE)
            if match:
                dados[nome] = match.group(0) if nome == "codigo_rastreio" else match.group(1)
        
        return dados
    
    def _gerar_resposta(self, intent: str, dados: Dict, from_number: str) -> str:
        """Gera resposta baseada na intenção"""
        
        responses = {
            "saudacao": """Olá! 👋 Seja bem-vindo à *LogiFlow*!

Como posso ajudar você hoje?

1️⃣ Rastrear meu pedido
2️⃣ Ver status da entrega
3️⃣ Consultar prazo
4️⃣ Falar com atendente

Digite o *número da opção* ou descreva sua dúvida.""",

            "rastreamento": self._resposta_rastreamento(dados),
            
            "status_pedido": self._resposta_status_pedido(dados),
            
            "prazo": """📅 *Consulta de Prazo*

Para consultar o prazo de entrega, preciso de algumas informações:

Por favor, me informe o *número do pedido* ou *código de rastreio*.""",

            "cancelamento": """⚠️ *Cancelamento de Pedido*

Entendo que deseja cancelar. Vou transferir você para um atendente que poderá processar essa solicitação.

Por favor, aguarde um momento... 🙏""",

            "duvida": """❓ *Precisa de Ajuda?*

Estou aqui para ajudar! Você pode:

🔍 Rastrear seu pedido
📦 Ver status da entrega
📞 Falar com atendente
💰 Solicitar orçamento

O que você gostaria de fazer?""",

            "horario": """🕐 *Horário de Atendimento*

Segunda a Sexta: 08:00 às 18:00
Sábado: 08:00 às 12:00

Fora do horário comercial, deixe sua mensagem que retornaremos assim que possível! 📱""",

            "preco": """💰 *Cotação de Frete*

Para fazer uma cotação, acesse:
🔗 https://logiflow.com.br/cotacao

Ou me informe:
📍 CEP origem
📍 CEP destino
📦 Peso aproximado

Farei a cotação para você!""",

            "agradecimento": """😊 Por nada! Fico feliz em ajudar!

Precisa de mais alguma coisa?

Se tiver outras dúvidas, é só chamar! 💙""",

            "despedida": """👋 Até logo!

Obrigado por usar a LogiFlow!
Estamos sempre à disposição. 💙

Tenha um ótimo dia! ☀️""",

            "desconhecido": """🤔 Desculpe, não entendi sua mensagem.

Você pode:

🔍 Rastrear pedido (envie o código)
📦 Ver status (envie o número do pedido)
💬 Falar com atendente
❓ Ver menu de opções

Digite *MENU* para ver todas as opções."""
        }
        
        return responses.get(intent, responses["desconhecido"])
    
    def _resposta_rastreamento(self, dados: Dict) -> str:
        """Gera resposta para rastreamento"""
        if "codigo_rastreio" in dados:
            codigo = dados["codigo_rastreio"]
            # Aqui você buscaria no banco de dados
            return f"""🔍 *Rastreamento - {codigo}*

Buscando informações do seu pedido...

📦 Status: Em trânsito
📍 Última atualização: São Paulo - SP
📅 Previsão de entrega: 25/01/2026

🔗 Acompanhe em tempo real:
https://logiflow.com.br/tracking/{codigo}"""
        else:
            return """🔍 *Rastreamento de Pedido*

Para rastrear seu pedido, por favor me envie:

📋 Número do pedido, OU
🔢 Código de rastreio

Exemplo: #12345 ou BR123456789BR"""
    
    def _resposta_status_pedido(self, dados: Dict) -> str:
        """Gera resposta para status do pedido"""
        if "numero_pedido" in dados:
            numero = dados["numero_pedido"]
            return f"""📦 *Status do Pedido #{numero}*

✅ Pedido confirmado
📦 Carga coletada
🚛 Em trânsito para destino
📍 Próxima etapa: Saiu para entrega

Previsão de entrega: *25/01/2026*

Qualquer dúvida, estou aqui! 😊"""
        else:
            return """📦 *Consulta de Status*

Por favor, me informe o *número do pedido*.

Exemplo: #12345 ou pedido 12345"""
    
    def _executar_acao(self, intent: str, dados: Dict, from_number: str) -> Optional[Dict]:
        """Executa ações baseadas na intenção"""
        
        if intent == "cancelamento":
            # Criar caso para atendimento humano
            return {"action": "create_case", "category": "cancelamento"}
        
        elif intent == "duvida":
            # Criar caso de suporte
            return {"action": "create_case", "category": "suporte"}
        
        elif intent == "preco" and len(dados) >= 2:
            # Iniciar processo de cotação
            return {"action": "start_quotation", "data": dados}
        
        return None
    
    def obter_menu_principal(self) -> str:
        """Retorna o menu principal do chatbot"""
        return """📱 *Menu LogiFlow*

Escolha uma opção:

1️⃣ 🔍 Rastrear meu pedido
2️⃣ 📦 Status da entrega
3️⃣ 📅 Consultar prazo
4️⃣ 💰 Solicitar orçamento
5️⃣ ⚠️ Reportar problema
6️⃣ 💬 Falar com atendente
7️⃣ 📞 Informações de contato

Digite o *número* da opção desejada."""
    
    def verificar_horario_comercial(self) -> Tuple[bool, str]:
        """Verifica se está no horário comercial"""
        from models.whatsapp_message import WhatsAppConfig
        
        config = self.db.query(WhatsAppConfig).filter(
            WhatsAppConfig.tenant_id == self.tenant_id
        ).first()
        
        if not config or not config.chatbot_business_hours_only:
            return True, ""
        
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_day = now.strftime("%A").lower()
        
        # Verificar dia da semana
        if current_day not in (config.business_days or []):
            return False, config.out_of_hours_message or "Estamos fora do horário comercial."
        
        # Verificar horário
        if not (config.business_hours_start <= current_time <= config.business_hours_end):
            return False, config.out_of_hours_message or "Estamos fora do horário comercial."
        
        return True, ""
    
    def buscar_pedido_por_telefone(self, telefone: str) -> List[Dict]:
        """Busca pedidos associados ao telefone"""
        # Implementar busca no banco
        # Por enquanto retorna exemplo
        return [
            {
                "numero": "12345",
                "status": "em_transito",
                "previsao": "25/01/2026"
            }
        ]
    
    def criar_caso_atendimento(self, telefone: str, assunto: str, descricao: str) -> str:
        """Cria caso para atendimento humano"""
        # Implementar criação de caso
        case_id = f"CASE-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        logger.info(f"Caso criado: {case_id} para {telefone}")
        return case_id


# Instância global
def get_chatbot_service(db: Session, tenant_id: str) -> ChatbotService:
    """Retorna instância do chatbot"""
    return ChatbotService(db, tenant_id)
