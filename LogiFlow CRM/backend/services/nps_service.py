"""
LogiFlow CRM - Serviço de NPS e Satisfação
Sistema REAL de pesquisas NPS, CSAT e ações automáticas com persistência em BD
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
import logging
import json

from models import (
    NPSSurvey, CSATSurvey, ChurnAlert, CustomerSuccessAction,
    NPSCategory, SurveyStatus, ChurnRiskLevel
)

logger = logging.getLogger(__name__)


class NPSService:
    """
    Serviço REAL de NPS (Net Promoter Score)
    
    NPS = % Promotores - % Detratores
    Escala: -100 a +100
    """
    
    def __init__(self, db: Session):
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
    
    def criar_pesquisa_nps(self, tenant_id: str, cliente_id: str, tipo: str = "30_dias") -> Dict:
        """
        Cria pesquisa NPS para um cliente (PERSISTENTE)
        
        Args:
            tenant_id: ID do tenant
            cliente_id: ID do cliente
            tipo: "30_dias" ou "90_dias"
            
        Returns:
            Dados da pesquisa criada
        """
        try:
            dias_expiracao = 7
            
            pesquisa = NPSSurvey(
                tenant_id=tenant_id,
                cliente_id=cliente_id,
                tipo=tipo,
                pergunta="Em uma escala de 0 a 10, quanto você recomendaria o LogiFlow CRM para um amigo ou colega?",
                status=SurveyStatus.ENVIADA.value,
                data_criacao=datetime.utcnow(),
                data_expiracao=datetime.utcnow() + timedelta(days=dias_expiracao),
                link_pesquisa=f"https://logiflow.com.br/nps/{cliente_id}/{datetime.utcnow().timestamp()}"
            )
            
            self.db.add(pesquisa)
            self.db.commit()
            self.db.refresh(pesquisa)
            
            logger.info(f"✅ Pesquisa NPS criada para cliente {cliente_id}: ID {pesquisa.id}")
            
            return self._pesquisa_to_dict(pesquisa)
        
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao criar pesquisa NPS: {e}")
            raise
    
    def registrar_resposta_nps(self, pesquisa_id: int, score: int, feedback: Optional[str] = None, ip: Optional[str] = None) -> Dict:
        """
        Registra resposta de uma pesquisa NPS (PERSISTENTE)
        
        Args:
            pesquisa_id: ID da pesquisa
            score: Score de 0 a 10
            feedback: Feedback textual opcional
            ip: IP da resposta
            
        Returns:
            Pesquisa atualizada
        """
        if not 0 <= score <= 10:
            raise ValueError("Score deve estar entre 0 e 10")
        
        try:
            pesquisa = self.db.query(NPSSurvey).filter(NPSSurvey.id == pesquisa_id).first()
            
            if not pesquisa:
                raise ValueError(f"Pesquisa {pesquisa_id} não encontrada")
            
            if pesquisa.status == SurveyStatus.RESPONDIDA.value:
                raise ValueError("Pesquisa já foi respondida")
            
            categoria = self.categorizar_resposta(score)
            
            # Atualizar pesquisa
            pesquisa.score = score
            pesquisa.categoria = categoria.value
            pesquisa.feedback_texto = feedback
            pesquisa.status = SurveyStatus.RESPONDIDA.value
            pesquisa.data_resposta = datetime.utcnow()
            pesquisa.ip_resposta = ip
            
            self.db.commit()
            self.db.refresh(pesquisa)
            
            # Acionar ações automáticas se necessário
            if categoria == NPSCategory.DETRATOR:
                self._acionar_acao_detrator(pesquisa)
            elif categoria == NPSCategory.PROMOTOR:
                self._acionar_acao_promotor(pesquisa)
            
            logger.info(f"✅ Resposta NPS registrada: {pesquisa_id} - Score: {score} - Categoria: {categoria.value}")
            
            return self._pesquisa_to_dict(pesquisa)
        
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao registrar resposta NPS: {e}")
            raise
    
    def _acionar_acao_detrator(self, pesquisa: NPSSurvey):
        """Aciona ações automáticas para detratores (PERSISTENTE)"""
        try:
            acao = CustomerSuccessAction(
                tenant_id=pesquisa.tenant_id,
                cliente_id=pesquisa.cliente_id,
                origem_tipo="nps_detrator",
                origem_id=str(pesquisa.id),
                tipo="contato_urgente",
                titulo=f"🚨 Detrator NPS - Score {pesquisa.score}",
                descricao=f"Cliente deu NPS {pesquisa.score}. Feedback: {pesquisa.feedback_texto or 'Sem feedback'}",
                responsavel="CS Team",
                status="pendente",
                prioridade="urgente",
                data_criacao=datetime.utcnow(),
                prazo=datetime.utcnow() + timedelta(days=1)
            )
            
            self.db.add(acao)
            self.db.commit()
            
            logger.warning(f"🚨 Detrator identificado! Cliente: {pesquisa.cliente_id} - Score: {pesquisa.score} - Ação criada: {acao.id}")
        
        except Exception as e:
            logger.error(f"Erro ao criar ação para detrator: {e}")
    
    def _acionar_acao_promotor(self, pesquisa: NPSSurvey):
        """Aciona ações automáticas para promotores (PERSISTENTE)"""
        try:
            acao = CustomerSuccessAction(
                tenant_id=pesquisa.tenant_id,
                cliente_id=pesquisa.cliente_id,
                origem_tipo="nps_promotor",
                origem_id=str(pesquisa.id),
                tipo="solicitar_depoimento",
                titulo=f"⭐ Promotor NPS - Score {pesquisa.score}",
                descricao=f"Cliente deu NPS {pesquisa.score}! Oportunidade para case de sucesso.",
                responsavel="Marketing",
                status="pendente",
                prioridade="media",
                data_criacao=datetime.utcnow(),
                prazo=datetime.utcnow() + timedelta(days=7)
            )
            
            self.db.add(acao)
            self.db.commit()
            
            logger.info(f"⭐ Promotor identificado! Cliente: {pesquisa.cliente_id} - Score: {pesquisa.score}")
        
        except Exception as e:
            logger.error(f"Erro ao criar ação para promotor: {e}")
    
    def obter_nps_periodo(self, tenant_id: str, data_inicio: datetime, data_fim: datetime) -> Dict:
        """
        Calcula NPS de um período (REAL do banco)
        
        Args:
            tenant_id: ID do tenant
            data_inicio: Data inicial
            data_fim: Data final
            
        Returns:
            NPS e estatísticas do período
        """
        try:
            # Buscar respostas do período
            respostas = self.db.query(NPSSurvey).filter(
                and_(
                    NPSSurvey.tenant_id == tenant_id,
                    NPSSurvey.status == SurveyStatus.RESPONDIDA.value,
                    NPSSurvey.data_resposta >= data_inicio,
                    NPSSurvey.data_resposta <= data_fim
                )
            ).all()
            
            scores = [r.score for r in respostas if r.score is not None]
            
            nps_data = self.calcular_nps(scores)
            nps_data["periodo"] = {
                "inicio": data_inicio.isoformat(),
                "fim": data_fim.isoformat()
            }
            
            # Feedback dos detratores
            detratores_com_feedback = [
                {"cliente_id": r.cliente_id, "score": r.score, "feedback": r.feedback_texto}
                for r in respostas if r.categoria == NPSCategory.DETRATOR.value and r.feedback_texto
            ]
            nps_data["detratores_feedback"] = detratores_com_feedback[:5]  # Top 5
            
            return nps_data
        
        except Exception as e:
            logger.error(f"Erro ao obter NPS do período: {e}")
            raise
    
    def agendar_pesquisas_automaticas(self, tenant_id: str) -> List[Dict]:
        """
        Agenda pesquisas NPS automáticas para clientes elegíveis (REAL)
        
        Args:
            tenant_id: ID do tenant
        
        Returns:
            Lista de pesquisas agendadas
        """
        try:
            pesquisas_agendadas = []
            
            # Buscar clientes elegíveis (que não têm pesquisa recente)
            clientes_elegiveis = self._obter_clientes_elegiveis(tenant_id)
            
            for cliente in clientes_elegiveis:
                # Verificar se já tem pesquisa recente
                if not self._tem_pesquisa_recente(tenant_id, cliente["id"]):
                    # Determinar tipo baseado no tempo de cliente
                    tipo = "90_dias" if cliente.get("dias_cliente", 0) > 90 else "30_dias"
                    
                    pesquisa = self.criar_pesquisa_nps(tenant_id, cliente["id"], tipo)
                    pesquisas_agendadas.append(pesquisa)
            
            logger.info(f"✅ {len(pesquisas_agendadas)} pesquisas NPS agendadas para tenant {tenant_id}")
            
            return pesquisas_agendadas
        
        except Exception as e:
            logger.error(f"Erro ao agendar pesquisas automáticas: {e}")
            raise
    
    def _obter_clientes_elegiveis(self, tenant_id: str) -> List[Dict]:
        """Obtém clientes elegíveis para pesquisa NPS (do banco)"""
        from models import Cliente
        
        try:
            # Buscar clientes ativos do tenant
            clientes = self.db.query(Cliente).filter(
                and_(
                    Cliente.tenant_id == tenant_id,
                    Cliente.ativo == True
                )
            ).limit(100).all()
            
            return [
                {
                    "id": c.id,
                    "nome": c.razao_social or c.nome_fantasia,
                    "dias_cliente": (datetime.utcnow() - c.created_at).days if c.created_at else 0
                }
                for c in clientes
            ]
        
        except Exception as e:
            logger.error(f"Erro ao obter clientes elegíveis: {e}")
            return []
    
    def _tem_pesquisa_recente(self, tenant_id: str, cliente_id: str, dias: int = 30) -> bool:
        """Verifica se cliente tem pesquisa recente (REAL)"""
        try:
            data_limite = datetime.utcnow() - timedelta(days=dias)
            
            pesquisa = self.db.query(NPSSurvey).filter(
                and_(
                    NPSSurvey.tenant_id == tenant_id,
                    NPSSurvey.cliente_id == cliente_id,
                    NPSSurvey.data_criacao >= data_limite
                )
            ).first()
            
            return pesquisa is not None
        
        except Exception as e:
            logger.error(f"Erro ao verificar pesquisa recente: {e}")
            return False
    
    def _pesquisa_to_dict(self, pesquisa: NPSSurvey) -> Dict:
        """Converte model NPSSurvey para dict"""
        return {
            "id": pesquisa.id,
            "cliente_id": pesquisa.cliente_id,
            "tipo": pesquisa.tipo,
            "pergunta": pesquisa.pergunta,
            "score": pesquisa.score,
            "categoria": pesquisa.categoria,
            "feedback_texto": pesquisa.feedback_texto,
            "status": pesquisa.status,
            "data_criacao": pesquisa.data_criacao.isoformat() if pesquisa.data_criacao else None,
            "data_expiracao": pesquisa.data_expiracao.isoformat() if pesquisa.data_expiracao else None,
            "data_resposta": pesquisa.data_resposta.isoformat() if pesquisa.data_resposta else None,
            "link_pesquisa": pesquisa.link_pesquisa
        }


class CSATService:
    """
    Serviço REAL de CSAT (Customer Satisfaction Score)
    Pesquisa de satisfação pós-suporte
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def criar_pesquisa_csat(self, tenant_id: str, ticket_id: str, cliente_id: str, atendente: Optional[str] = None) -> Dict:
        """
        Cria pesquisa CSAT após fechamento de ticket (PERSISTENTE)
        
        Args:
            tenant_id: ID do tenant
            ticket_id: ID do ticket de suporte
            cliente_id: ID do cliente
            atendente: Nome do atendente responsável
            
        Returns:
            Dados da pesquisa criada
        """
        try:
            pesquisa = CSATSurvey(
                tenant_id=tenant_id,
                cliente_id=cliente_id,
                ticket_id=ticket_id,
                pergunta="Como você avalia o atendimento recebido?",
                status=SurveyStatus.ENVIADA.value,
                data_criacao=datetime.utcnow(),
                data_expiracao=datetime.utcnow() + timedelta(days=3),
                atendente_responsavel=atendente,
                link_pesquisa=f"https://logiflow.com.br/csat/{ticket_id}/{datetime.utcnow().timestamp()}"
            )
            
            self.db.add(pesquisa)
            self.db.commit()
            self.db.refresh(pesquisa)
            
            logger.info(f"✅ Pesquisa CSAT criada para ticket {ticket_id}")
            
            return self._pesquisa_to_dict(pesquisa)
        
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao criar pesquisa CSAT: {e}")
            raise
    
    def registrar_resposta_csat(self, pesquisa_id: int, score: int, comentario: Optional[str] = None, ip: Optional[str] = None) -> Dict:
        """
        Registra resposta de pesquisa CSAT (PERSISTENTE)
        
        Args:
            pesquisa_id: ID da pesquisa
            score: Score de 1 a 5
            comentario: Comentário opcional
            ip: IP da resposta
            
        Returns:
            Pesquisa atualizada
        """
        if not 1 <= score <= 5:
            raise ValueError("Score deve estar entre 1 e 5")
        
        try:
            pesquisa = self.db.query(CSATSurvey).filter(CSATSurvey.id == pesquisa_id).first()
            
            if not pesquisa:
                raise ValueError(f"Pesquisa {pesquisa_id} não encontrada")
            
            pesquisa.score = score
            pesquisa.comentario = comentario
            pesquisa.status = SurveyStatus.RESPONDIDA.value
            pesquisa.data_resposta = datetime.utcnow()
            pesquisa.ip_resposta = ip
            
            self.db.commit()
            self.db.refresh(pesquisa)
            
            # Se insatisfeito, criar alerta
            if score <= 2:
                self._criar_alerta_insatisfacao(pesquisa)
            
            logger.info(f"✅ Resposta CSAT registrada: {pesquisa_id} - Score: {score}")
            
            return self._pesquisa_to_dict(pesquisa)
        
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao registrar resposta CSAT: {e}")
            raise
    
    def calcular_csat_periodo(self, tenant_id: str, data_inicio: datetime, data_fim: datetime) -> Dict:
        """
        Calcula CSAT médio de um período (REAL do banco)
        
        Args:
            tenant_id: ID do tenant
            data_inicio: Data inicial
            data_fim: Data final
            
        Returns:
            CSAT e estatísticas
        """
        try:
            # Buscar respostas do período
            respostas = self.db.query(CSATSurvey).filter(
                and_(
                    CSATSurvey.tenant_id == tenant_id,
                    CSATSurvey.status == SurveyStatus.RESPONDIDA.value,
                    CSATSurvey.data_resposta >= data_inicio,
                    CSATSurvey.data_resposta <= data_fim
                )
            ).all()
            
            scores = [r.score for r in respostas if r.score is not None]
            
            if not scores:
                return {
                    "csat": 0,
                    "score_medio": 0,
                    "total_respostas": 0,
                    "distribuicao": {},
                    "periodo": {
                        "inicio": data_inicio.isoformat(),
                        "fim": data_fim.isoformat()
                    }
                }
            
            total = len(scores)
            soma = sum(scores)
            csat = (soma / (total * 5)) * 100  # Percentual de satisfação
            
            # Distribuição
            distribuicao = {
                "muito_satisfeito": len([r for r in scores if r == 5]),
                "satisfeito": len([r for r in scores if r == 4]),
                "neutro": len([r for r in scores if r == 3]),
                "insatisfeito": len([r for r in scores if r == 2]),
                "muito_insatisfeito": len([r for r in scores if r == 1])
            }
            
            # Comentários negativos
            negativos_com_comentario = [
                {"ticket_id": r.ticket_id, "score": r.score, "comentario": r.comentario, "atendente": r.atendente_responsavel}
                for r in respostas if r.score <= 2 and r.comentario
            ]
            
            return {
                "csat": round(csat, 2),
                "score_medio": round(soma / total, 2),
                "total_respostas": total,
                "distribuicao": distribuicao,
                "periodo": {
                    "inicio": data_inicio.isoformat(),
                    "fim": data_fim.isoformat()
                },
                "negativos_comentarios": negativos_com_comentario[:5]  # Top 5
            }
        
        except Exception as e:
            logger.error(f"Erro ao calcular CSAT: {e}")
            raise
    
    def _criar_alerta_insatisfacao(self, pesquisa: CSATSurvey):
        """Cria alerta e ação para resposta insatisfeita (PERSISTENTE)"""
        try:
            acao = CustomerSuccessAction(
                tenant_id=pesquisa.tenant_id,
                cliente_id=pesquisa.cliente_id,
                origem_tipo="csat_insatisfeito",
                origem_id=str(pesquisa.id),
                tipo="follow_up_suporte",
                titulo=f"😞 Cliente insatisfeito com suporte - Ticket {pesquisa.ticket_id}",
                descricao=f"CSAT {pesquisa.score}/5. Comentário: {pesquisa.comentario or 'Sem comentário'}. Atendente: {pesquisa.atendente_responsavel or 'N/A'}",
                responsavel="Supervisor Suporte",
                status="pendente",
                prioridade="alta",
                data_criacao=datetime.utcnow(),
                prazo=datetime.utcnow() + timedelta(days=2)
            )
            
            self.db.add(acao)
            self.db.commit()
            
            logger.warning(f"😞 Cliente insatisfeito com suporte! Ticket: {pesquisa.ticket_id} - Score: {pesquisa.score}")
        
        except Exception as e:
            logger.error(f"Erro ao criar alerta de insatisfação: {e}")
    
    def _pesquisa_to_dict(self, pesquisa: CSATSurvey) -> Dict:
        """Converte model CSATSurvey para dict"""
        return {
            "id": pesquisa.id,
            "ticket_id": pesquisa.ticket_id,
            "cliente_id": pesquisa.cliente_id,
            "pergunta": pesquisa.pergunta,
            "score": pesquisa.score,
            "comentario": pesquisa.comentario,
            "status": pesquisa.status,
            "data_criacao": pesquisa.data_criacao.isoformat() if pesquisa.data_criacao else None,
            "data_expiracao": pesquisa.data_expiracao.isoformat() if pesquisa.data_expiracao else None,
            "data_resposta": pesquisa.data_resposta.isoformat() if pesquisa.data_resposta else None,
            "atendente_responsavel": pesquisa.atendente_responsavel,
            "link_pesquisa": pesquisa.link_pesquisa
        }


class SatisfactionDashboard:
    """Dashboard consolidado de NPS e CSAT (REAL)"""
    
    def __init__(self, db: Session):
        self.db = db
        self.nps_service = NPSService(db)
        self.csat_service = CSATService(db)
    
    def obter_dashboard(self, tenant_id: str, periodo_dias: int = 30) -> Dict:
        """
        Obtém dashboard consolidado de satisfação (REAL)
        
        Args:
            tenant_id: ID do tenant
            periodo_dias: Período em dias
            
        Returns:
            Dashboard com NPS, CSAT e tendências
        """
        try:
            data_fim = datetime.utcnow()
            data_inicio = data_fim - timedelta(days=periodo_dias)
            
            # Obter dados REAIS
            nps_data = self.nps_service.obter_nps_periodo(tenant_id, data_inicio, data_fim)
            csat_data = self.csat_service.calcular_csat_periodo(tenant_id, data_inicio, data_fim)
            
            # Tendências (últimas 4 semanas)
            tendencias = self._calcular_tendencias(tenant_id, periodo_dias)
            
            return {
                "periodo_dias": periodo_dias,
                "nps": nps_data,
                "csat": csat_data,
                "tendencias": tendencias,
                "alertas_ativos": self._obter_alertas_ativos(tenant_id),
                "data_atualizacao": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Erro ao obter dashboard de satisfação: {e}")
            raise
    
    def _calcular_tendencias(self, tenant_id: str, periodo_dias: int) -> Dict:
        """Calcula tendências semanais (REAL)"""
        try:
            semanas = []
            data_fim = datetime.utcnow()
            
            for i in range(4):  # Últimas 4 semanas
                semana_fim = data_fim - timedelta(days=i*7)
                semana_inicio = semana_fim - timedelta(days=7)
                
                # NPS da semana
                respostas_nps = self.db.query(NPSSurvey).filter(
                    and_(
                        NPSSurvey.tenant_id == tenant_id,
                        NPSSurvey.status == SurveyStatus.RESPONDIDA.value,
                        NPSSurvey.data_resposta >= semana_inicio,
                        NPSSurvey.data_resposta < semana_fim
                    )
                ).all()
                
                scores_nps = [r.score for r in respostas_nps if r.score is not None]
                nps = self.nps_service.calcular_nps(scores_nps)["nps"] if scores_nps else 0
                
                # CSAT da semana
                respostas_csat = self.db.query(CSATSurvey).filter(
                    and_(
                        CSATSurvey.tenant_id == tenant_id,
                        CSATSurvey.status == SurveyStatus.RESPONDIDA.value,
                        CSATSurvey.data_resposta >= semana_inicio,
                        CSATSurvey.data_resposta < semana_fim
                    )
                ).all()
                
                scores_csat = [r.score for r in respostas_csat if r.score is not None]
                csat = (sum(scores_csat) / (len(scores_csat) * 5) * 100) if scores_csat else 0
                
                semanas.insert(0, {
                    "data": semana_inicio.strftime("%Y-%m-%d"),
                    "nps": round(nps, 2),
                    "csat": round(csat, 2)
                })
            
            return {
                "nps": [{"data": s["data"], "valor": s["nps"]} for s in semanas],
                "csat": [{"data": s["data"], "valor": s["csat"]} for s in semanas]
            }
        
        except Exception as e:
            logger.error(f"Erro ao calcular tendências: {e}")
            return {"nps": [], "csat": []}
    
    def _obter_alertas_ativos(self, tenant_id: str) -> List[Dict]:
        """Obtém alertas ativos de satisfação (REAL)"""
        try:
            # Buscar ações pendentes dos últimos 7 dias
            data_limite = datetime.utcnow() - timedelta(days=7)
            
            acoes = self.db.query(CustomerSuccessAction).filter(
                and_(
                    CustomerSuccessAction.tenant_id == tenant_id,
                    CustomerSuccessAction.status == "pendente",
                    or_(
                        CustomerSuccessAction.origem_tipo == "nps_detrator",
                        CustomerSuccessAction.origem_tipo == "csat_insatisfeito"
                    ),
                    CustomerSuccessAction.data_criacao >= data_limite
                )
            ).order_by(CustomerSuccessAction.prioridade.desc(), CustomerSuccessAction.data_criacao.desc()).limit(10).all()
            
            return [
                {
                    "id": acao.id,
                    "tipo": acao.origem_tipo,
                    "cliente_id": acao.cliente_id,
                    "titulo": acao.titulo,
                    "descricao": acao.descricao,
                    "prioridade": acao.prioridade,
                    "prazo": acao.prazo.isoformat() if acao.prazo else None,
                    "data_criacao": acao.data_criacao.isoformat() if acao.data_criacao else None
                }
                for acao in acoes
            ]
        
        except Exception as e:
            logger.error(f"Erro ao obter alertas ativos: {e}")
            return []
