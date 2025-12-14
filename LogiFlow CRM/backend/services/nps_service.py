"""
LogiFlow CRM - Serviço de NPS e Satisfação
Sistema de pesquisas NPS, CSAT e ações automáticas
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class NPSCategory(Enum):
    """Categorias de NPS"""
    PROMOTOR = "promotor"  # 9-10
    NEUTRO = "neutro"      # 7-8
    DETRATOR = "detrator"  # 0-6


class NPSService:
    """
    Serviço de NPS (Net Promoter Score)
    
    NPS = % Promotores - % Detratores
    Escala: -100 a +100
    """
    
    def __init__(self, db=None):
        self.db = db
    
    def calcular_nps(self, respostas: List[int]) -> Dict:
        """
        Calcula NPS baseado em lista de respostas (0-10)
        
        Args:
            respostas: Lista de scores de 0 a 10
            
        Returns:
            Dict com NPS, categorias e análise
        """
        if not respostas:
            return {
                "nps": 0,
                "total_respostas": 0,
                "promotores": 0,
                "neutros": 0,
                "detratores": 0
            }
        
        total = len(respostas)
        promotores = len([r for r in respostas if r >= 9])
        neutros = len([r for r in respostas if 7 <= r <= 8])
        detratores = len([r for r in respostas if r <= 6])
        
        # Calcular NPS
        pct_promotores = (promotores / total) * 100
        pct_detratores = (detratores / total) * 100
        nps = pct_promotores - pct_detratores
        
        # Determinar classificação
        if nps >= 75:
            classificacao = "excelente"
        elif nps >= 50:
            classificacao = "muito_bom"
        elif nps >= 0:
            classificacao = "razoavel"
        else:
            classificacao = "critico"
        
        return {
            "nps": round(nps, 2),
            "total_respostas": total,
            "promotores": promotores,
            "promotores_pct": round(pct_promotores, 2),
            "neutros": neutros,
            "neutros_pct": round((neutros / total) * 100, 2),
            "detratores": detratores,
            "detratores_pct": round(pct_detratores, 2),
            "classificacao": classificacao
        }
    
    def categorizar_resposta(self, score: int) -> NPSCategory:
        """Categoriza uma resposta NPS"""
        if score >= 9:
            return NPSCategory.PROMOTOR
        elif score >= 7:
            return NPSCategory.NEUTRO
        else:
            return NPSCategory.DETRATOR
    
    def criar_pesquisa_nps(self, cliente_id: str, tipo: str = "30_dias") -> Dict:
        """
        Cria pesquisa NPS para um cliente
        
        Args:
            cliente_id: ID do cliente
            tipo: "30_dias" ou "90_dias"
            
        Returns:
            Dados da pesquisa criada
        """
        dias = 30 if tipo == "30_dias" else 90
        
        pesquisa = {
            "id": f"nps_{cliente_id}_{datetime.now().timestamp()}",
            "cliente_id": cliente_id,
            "tipo": tipo,
            "pergunta": "Em uma escala de 0 a 10, quanto você recomendaria o LogiFlow CRM para um amigo ou colega?",
            "data_criacao": datetime.now().isoformat(),
            "data_expiracao": (datetime.now() + timedelta(days=7)).isoformat(),
            "status": "enviada",
            "resposta": None,
            "score": None,
            "categoria": None,
            "feedback_texto": None
        }
        
        # Em produção, salvar no DB
        logger.info(f"Pesquisa NPS criada para cliente {cliente_id}: {pesquisa['id']}")
        
        return pesquisa
    
    def registrar_resposta_nps(self, pesquisa_id: str, score: int, feedback: Optional[str] = None) -> Dict:
        """
        Registra resposta de uma pesquisa NPS
        
        Args:
            pesquisa_id: ID da pesquisa
            score: Score de 0 a 10
            feedback: Feedback textual opcional
            
        Returns:
            Pesquisa atualizada
        """
        if not 0 <= score <= 10:
            raise ValueError("Score deve estar entre 0 e 10")
        
        categoria = self.categorizar_resposta(score)
        
        # Atualizar pesquisa (em produção, no DB)
        pesquisa = {
            "id": pesquisa_id,
            "status": "respondida",
            "resposta": score,
            "score": score,
            "categoria": categoria.value,
            "feedback_texto": feedback,
            "data_resposta": datetime.now().isoformat()
        }
        
        # Acionar ações automáticas se necessário
        if categoria == NPSCategory.DETRATOR:
            self._acionar_acao_detrator(pesquisa)
        elif categoria == NPSCategory.PROMOTOR:
            self._acionar_acao_promotor(pesquisa)
        
        logger.info(f"Resposta NPS registrada: {pesquisa_id} - Score: {score} - Categoria: {categoria.value}")
        
        return pesquisa
    
    def _acionar_acao_detrator(self, pesquisa: Dict):
        """Aciona ações automáticas para detratores"""
        # Criar alerta para CS
        alerta = {
            "tipo": "nps_detrator",
            "cliente_id": pesquisa.get("cliente_id"),
            "pesquisa_id": pesquisa["id"],
            "score": pesquisa["score"],
            "feedback": pesquisa.get("feedback_texto"),
            "urgencia": "alta",
            "acao_sugerida": "Contato imediato com cliente para entender insatisfação",
            "data_criacao": datetime.now().isoformat()
        }
        
        logger.warning(f"Detrator identificado! Cliente: {pesquisa.get('cliente_id')} - Score: {pesquisa['score']}")
        
        # Em produção: enviar notificação, criar ticket, etc
        
    def _acionar_acao_promotor(self, pesquisa: Dict):
        """Aciona ações automáticas para promotores"""
        # Solicitar depoimento, caso de sucesso, etc
        acao = {
            "tipo": "nps_promotor",
            "cliente_id": pesquisa.get("cliente_id"),
            "pesquisa_id": pesquisa["id"],
            "score": pesquisa["score"],
            "acao_sugerida": "Solicitar depoimento ou caso de sucesso",
            "data_criacao": datetime.now().isoformat()
        }
        
        logger.info(f"Promotor identificado! Cliente: {pesquisa.get('cliente_id')} - Score: {pesquisa['score']}")
    
    def obter_nps_periodo(self, data_inicio: datetime, data_fim: datetime) -> Dict:
        """
        Calcula NPS de um período
        
        Args:
            data_inicio: Data inicial
            data_fim: Data final
            
        Returns:
            NPS e estatísticas do período
        """
        # Simular respostas (em produção, buscar do DB)
        respostas = [9, 10, 8, 7, 9, 10, 6, 5, 9, 8, 10, 7, 9, 8, 10]
        
        nps_data = self.calcular_nps(respostas)
        nps_data["periodo"] = {
            "inicio": data_inicio.isoformat(),
            "fim": data_fim.isoformat()
        }
        
        return nps_data
    
    def agendar_pesquisas_automaticas(self) -> List[Dict]:
        """
        Agenda pesquisas NPS automáticas para clientes elegíveis
        
        Returns:
            Lista de pesquisas agendadas
        """
        pesquisas_agendadas = []
        
        # Simular clientes (em produção, buscar do DB)
        clientes_elegiveis = self._obter_clientes_elegiveis()
        
        for cliente in clientes_elegiveis:
            # Verificar se já tem pesquisa recente
            if not self._tem_pesquisa_recente(cliente["id"]):
                # Determinar tipo baseado no tempo de cliente
                tipo = "90_dias" if cliente.get("dias_cliente", 0) > 90 else "30_dias"
                
                pesquisa = self.criar_pesquisa_nps(cliente["id"], tipo)
                pesquisas_agendadas.append(pesquisa)
        
        logger.info(f"{len(pesquisas_agendadas)} pesquisas NPS agendadas")
        
        return pesquisas_agendadas
    
    def _obter_clientes_elegiveis(self) -> List[Dict]:
        """Obtém clientes elegíveis para pesquisa NPS"""
        # Simular (em produção, buscar do DB)
        return [
            {"id": "cli_001", "nome": "Empresa ABC", "dias_cliente": 35},
            {"id": "cli_002", "nome": "Transportadora XYZ", "dias_cliente": 95},
            {"id": "cli_003", "nome": "Logística 123", "dias_cliente": 45}
        ]
    
    def _tem_pesquisa_recente(self, cliente_id: str) -> bool:
        """Verifica se cliente tem pesquisa recente"""
        # Simular (em produção, buscar do DB)
        return False


class CSATService:
    """
    Serviço de CSAT (Customer Satisfaction Score)
    Pesquisa de satisfação pós-suporte
    """
    
    def __init__(self, db=None):
        self.db = db
    
    def criar_pesquisa_csat(self, ticket_id: str, cliente_id: str) -> Dict:
        """
        Cria pesquisa CSAT após fechamento de ticket
        
        Args:
            ticket_id: ID do ticket de suporte
            cliente_id: ID do cliente
            
        Returns:
            Dados da pesquisa criada
        """
        pesquisa = {
            "id": f"csat_{ticket_id}_{datetime.now().timestamp()}",
            "ticket_id": ticket_id,
            "cliente_id": cliente_id,
            "pergunta": "Como você avalia o atendimento recebido?",
            "opcoes": [
                {"valor": 5, "label": "Muito Satisfeito 😄"},
                {"valor": 4, "label": "Satisfeito 🙂"},
                {"valor": 3, "label": "Neutro 😐"},
                {"valor": 2, "label": "Insatisfeito 😞"},
                {"valor": 1, "label": "Muito Insatisfeito 😡"}
            ],
            "data_criacao": datetime.now().isoformat(),
            "data_expiracao": (datetime.now() + timedelta(days=3)).isoformat(),
            "status": "enviada",
            "resposta": None
        }
        
        logger.info(f"Pesquisa CSAT criada para ticket {ticket_id}")
        
        return pesquisa
    
    def registrar_resposta_csat(self, pesquisa_id: str, score: int, comentario: Optional[str] = None) -> Dict:
        """
        Registra resposta de pesquisa CSAT
        
        Args:
            pesquisa_id: ID da pesquisa
            score: Score de 1 a 5
            comentario: Comentário opcional
            
        Returns:
            Pesquisa atualizada
        """
        if not 1 <= score <= 5:
            raise ValueError("Score deve estar entre 1 e 5")
        
        pesquisa = {
            "id": pesquisa_id,
            "status": "respondida",
            "resposta": score,
            "comentario": comentario,
            "data_resposta": datetime.now().isoformat()
        }
        
        # Se insatisfeito, criar alerta
        if score <= 2:
            self._criar_alerta_insatisfacao(pesquisa)
        
        logger.info(f"Resposta CSAT registrada: {pesquisa_id} - Score: {score}")
        
        return pesquisa
    
    def calcular_csat_periodo(self, data_inicio: datetime, data_fim: datetime) -> Dict:
        """
        Calcula CSAT médio de um período
        
        Args:
            data_inicio: Data inicial
            data_fim: Data final
            
        Returns:
            CSAT e estatísticas
        """
        # Simular respostas (em produção, buscar do DB)
        respostas = [5, 4, 5, 3, 4, 5, 2, 4, 5, 4, 5, 3, 4, 5, 4]
        
        if not respostas:
            return {"csat": 0, "total_respostas": 0}
        
        total = len(respostas)
        soma = sum(respostas)
        csat = (soma / (total * 5)) * 100  # Percentual de satisfação
        
        # Distribuição
        distribuicao = {
            "muito_satisfeito": len([r for r in respostas if r == 5]),
            "satisfeito": len([r for r in respostas if r == 4]),
            "neutro": len([r for r in respostas if r == 3]),
            "insatisfeito": len([r for r in respostas if r == 2]),
            "muito_insatisfeito": len([r for r in respostas if r == 1])
        }
        
        return {
            "csat": round(csat, 2),
            "score_medio": round(soma / total, 2),
            "total_respostas": total,
            "distribuicao": distribuicao,
            "periodo": {
                "inicio": data_inicio.isoformat(),
                "fim": data_fim.isoformat()
            }
        }
    
    def _criar_alerta_insatisfacao(self, pesquisa: Dict):
        """Cria alerta para resposta insatisfeita"""
        alerta = {
            "tipo": "csat_insatisfeito",
            "ticket_id": pesquisa.get("ticket_id"),
            "cliente_id": pesquisa.get("cliente_id"),
            "score": pesquisa["resposta"],
            "comentario": pesquisa.get("comentario"),
            "urgencia": "alta",
            "acao_sugerida": "Revisar atendimento e contatar cliente",
            "data_criacao": datetime.now().isoformat()
        }
        
        logger.warning(f"Cliente insatisfeito com suporte! Ticket: {pesquisa.get('ticket_id')} - Score: {pesquisa['resposta']}")


class SatisfactionDashboard:
    """Dashboard consolidado de NPS e CSAT"""
    
    def __init__(self, db=None):
        self.db = db
        self.nps_service = NPSService(db)
        self.csat_service = CSATService(db)
    
    def obter_dashboard(self, periodo_dias: int = 30) -> Dict:
        """
        Obtém dashboard consolidado de satisfação
        
        Args:
            periodo_dias: Período em dias
            
        Returns:
            Dashboard com NPS, CSAT e tendências
        """
        data_fim = datetime.now()
        data_inicio = data_fim - timedelta(days=periodo_dias)
        
        # Obter dados
        nps_data = self.nps_service.obter_nps_periodo(data_inicio, data_fim)
        csat_data = self.csat_service.calcular_csat_periodo(data_inicio, data_fim)
        
        # Tendências (simular)
        tendencias = {
            "nps": [
                {"data": "2024-11-14", "valor": 65},
                {"data": "2024-11-21", "valor": 68},
                {"data": "2024-11-28", "valor": 70},
                {"data": "2024-12-05", "valor": 72},
                {"data": "2024-12-12", "valor": 75}
            ],
            "csat": [
                {"data": "2024-11-14", "valor": 82},
                {"data": "2024-11-21", "valor": 84},
                {"data": "2024-11-28", "valor": 85},
                {"data": "2024-12-05", "valor": 86},
                {"data": "2024-12-12", "valor": 88}
            ]
        }
        
        return {
            "periodo_dias": periodo_dias,
            "nps": nps_data,
            "csat": csat_data,
            "tendencias": tendencias,
            "alertas_ativos": self._obter_alertas_ativos(),
            "data_atualizacao": datetime.now().isoformat()
        }
    
    def _obter_alertas_ativos(self) -> List[Dict]:
        """Obtém alertas ativos de satisfação"""
        # Simular (em produção, buscar do DB)
        return [
            {
                "tipo": "nps_detrator",
                "cliente": "Empresa ABC",
                "score": 4,
                "feedback": "Dificuldade em usar o sistema",
                "data": "2024-12-13T10:00:00"
            },
            {
                "tipo": "csat_insatisfeito",
                "cliente": "Transportadora XYZ",
                "score": 2,
                "comentario": "Demora no atendimento",
                "data": "2024-12-14T14:30:00"
            }
        ]
