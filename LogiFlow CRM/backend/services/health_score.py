"""
LogiFlow CRM - Health Score e Customer Success
Sistema de cálculo de saúde do cliente e prevenção de churn
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class HealthScoreCalculator:
    """
    Calculadora de Health Score do Cliente
    
    Fórmula:
    Health Score = (Uso × 30%) + (Adoção × 20%) + (Engajamento × 15%) + 
                   (Suporte × 15%) + (Financeiro × 20%)
    
    Escala: 0-100
    - 80-100: Verde (Saudável)
    - 50-79: Amarelo (Atenção)
    - 0-49: Vermelho (Risco de Churn)
    """
    
    # Pesos das métricas
    PESO_USO = 0.30
    PESO_ADOCAO = 0.20
    PESO_ENGAJAMENTO = 0.15
    PESO_SUPORTE = 0.15
    PESO_FINANCEIRO = 0.20
    
    # Thresholds
    THRESHOLD_VERDE = 80
    THRESHOLD_AMARELO = 50
    
    def __init__(self, cliente_id: str, db=None):
        """
        Inicializa calculadora para um cliente
        
        Args:
            cliente_id: ID do cliente
            db: Conexão com banco de dados (opcional)
        """
        self.cliente_id = cliente_id
        self.db = db
        self.metricas = {}
    
    def calcular_health_score(self) -> Dict:
        """
        Calcula Health Score completo do cliente
        
        Returns:
            Dict com score, status, métricas e recomendações
        """
        try:
            # Calcular cada métrica
            uso = self.calcular_metrica_uso()
            adocao = self.calcular_metrica_adocao()
            engajamento = self.calcular_metrica_engajamento()
            suporte = self.calcular_metrica_suporte()
            financeiro = self.calcular_metrica_financeiro()
            
            # Armazenar métricas
            self.metricas = {
                'uso': uso,
                'adocao': adocao,
                'engajamento': engajamento,
                'suporte': suporte,
                'financeiro': financeiro
            }
            
            # Calcular score total
            score = (
                uso['score'] * self.PESO_USO +
                adocao['score'] * self.PESO_ADOCAO +
                engajamento['score'] * self.PESO_ENGAJAMENTO +
                suporte['score'] * self.PESO_SUPORTE +
                financeiro['score'] * self.PESO_FINANCEIRO
            )
            
            # Determinar status
            status = self._determinar_status(score)
            
            # Gerar recomendações
            recomendacoes = self._gerar_recomendacoes()
            
            # Calcular risco de churn
            risco_churn = self._calcular_risco_churn(score)
            
            return {
                'cliente_id': self.cliente_id,
                'health_score': round(score, 2),
                'status': status,
                'metricas': self.metricas,
                'recomendacoes': recomendacoes,
                'risco_churn': risco_churn,
                'data_calculo': datetime.now().isoformat(),
                'proxima_revisao': (datetime.now() + timedelta(days=7)).isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro ao calcular Health Score para cliente {self.cliente_id}: {e}")
            return {
                'cliente_id': self.cliente_id,
                'health_score': 0,
                'status': 'erro',
                'error': str(e)
            }
    
    def calcular_metrica_uso(self) -> Dict:
        """
        Métrica 1: Uso do Sistema (30%)
        
        Indicadores:
        - Logins nos últimos 30 dias
        - Frequência de uso
        - Tempo médio de sessão
        - Última atividade
        
        Returns:
            Dict com score (0-100) e detalhes
        """
        # Simular dados (em produção, buscar do banco)
        logins_30d = self._get_logins_ultimos_30_dias()
        ultima_atividade = self._get_ultima_atividade()
        tempo_medio_sessao = self._get_tempo_medio_sessao()
        
        # Calcular score
        score = 0
        
        # Logins (40 pontos)
        if logins_30d >= 20:
            score += 40
        elif logins_30d >= 10:
            score += 30
        elif logins_30d >= 5:
            score += 20
        elif logins_30d >= 1:
            score += 10
        
        # Última atividade (30 pontos)
        dias_sem_uso = (datetime.now() - ultima_atividade).days
        if dias_sem_uso <= 1:
            score += 30
        elif dias_sem_uso <= 7:
            score += 20
        elif dias_sem_uso <= 15:
            score += 10
        elif dias_sem_uso <= 30:
            score += 5
        
        # Tempo de sessão (30 pontos)
        if tempo_medio_sessao >= 30:  # 30+ minutos
            score += 30
        elif tempo_medio_sessao >= 15:
            score += 20
        elif tempo_medio_sessao >= 5:
            score += 10
        
        return {
            'score': score,
            'logins_30d': logins_30d,
            'ultima_atividade': ultima_atividade.isoformat(),
            'dias_sem_uso': dias_sem_uso,
            'tempo_medio_sessao_min': tempo_medio_sessao,
            'status': 'ativo' if dias_sem_uso <= 7 else 'inativo'
        }
    
    def calcular_metrica_adocao(self) -> Dict:
        """
        Métrica 2: Adoção de Features (20%)
        
        Indicadores:
        - Módulos utilizados
        - Features ativadas
        - Configurações personalizadas
        - Integrações ativas
        
        Returns:
            Dict com score (0-100) e detalhes
        """
        # Features disponíveis
        features_disponiveis = [
            'cotacoes', 'pedidos', 'entregas', 'rastreamento',
            'whatsapp', 'cte', 'relatorios', 'dashboard'
        ]
        
        # Simular features utilizadas
        features_utilizadas = self._get_features_utilizadas()
        
        # Calcular score
        taxa_adocao = (len(features_utilizadas) / len(features_disponiveis)) * 100
        
        # Bônus por features críticas
        features_criticas = ['cotacoes', 'pedidos', 'entregas']
        criticas_ativas = len([f for f in features_criticas if f in features_utilizadas])
        bonus = (criticas_ativas / len(features_criticas)) * 20
        
        score = min(100, taxa_adocao + bonus)
        
        return {
            'score': round(score, 2),
            'features_utilizadas': features_utilizadas,
            'features_disponiveis': features_disponiveis,
            'taxa_adocao': round(taxa_adocao, 2),
            'features_criticas_ativas': criticas_ativas,
            'total_features_criticas': len(features_criticas)
        }
    
    def calcular_metrica_engajamento(self) -> Dict:
        """
        Métrica 3: Engajamento (15%)
        
        Indicadores:
        - Ações realizadas (cotações, pedidos, etc)
        - Interações com suporte
        - Feedback fornecido
        - Participação em treinamentos
        
        Returns:
            Dict com score (0-100) e detalhes
        """
        # Simular dados
        acoes_30d = self._get_acoes_ultimos_30_dias()
        interacoes_suporte = self._get_interacoes_suporte()
        feedback_fornecido = self._get_feedback_fornecido()
        
        score = 0
        
        # Ações (50 pontos)
        if acoes_30d >= 100:
            score += 50
        elif acoes_30d >= 50:
            score += 40
        elif acoes_30d >= 20:
            score += 30
        elif acoes_30d >= 10:
            score += 20
        elif acoes_30d >= 1:
            score += 10
        
        # Interações com suporte (25 pontos)
        if interacoes_suporte >= 5:
            score += 25
        elif interacoes_suporte >= 3:
            score += 20
        elif interacoes_suporte >= 1:
            score += 15
        
        # Feedback (25 pontos)
        if feedback_fornecido >= 3:
            score += 25
        elif feedback_fornecido >= 1:
            score += 15
        
        return {
            'score': score,
            'acoes_30d': acoes_30d,
            'interacoes_suporte': interacoes_suporte,
            'feedback_fornecido': feedback_fornecido,
            'nivel_engajamento': 'alto' if score >= 70 else 'medio' if score >= 40 else 'baixo'
        }
    
    def calcular_metrica_suporte(self) -> Dict:
        """
        Métrica 4: Suporte (15%)
        
        Indicadores:
        - Tickets abertos vs resolvidos
        - Tempo médio de resolução
        - Satisfação com suporte (NPS)
        - Tickets críticos
        
        Returns:
            Dict com score (0-100) e detalhes
        """
        # Simular dados
        tickets_abertos = self._get_tickets_abertos()
        tickets_resolvidos = self._get_tickets_resolvidos()
        tempo_medio_resolucao = self._get_tempo_medio_resolucao()
        nps_suporte = self._get_nps_suporte()
        
        score = 100  # Começar com 100 e deduzir
        
        # Deduzir por tickets abertos (máximo -40)
        if tickets_abertos > 5:
            score -= 40
        elif tickets_abertos > 3:
            score -= 30
        elif tickets_abertos > 1:
            score -= 20
        elif tickets_abertos == 1:
            score -= 10
        
        # Deduzir por tempo de resolução (máximo -30)
        if tempo_medio_resolucao > 48:  # >48h
            score -= 30
        elif tempo_medio_resolucao > 24:
            score -= 20
        elif tempo_medio_resolucao > 12:
            score -= 10
        
        # Ajustar por NPS (máximo -30 ou +30)
        if nps_suporte >= 9:
            score += 30
        elif nps_suporte >= 7:
            score += 10
        elif nps_suporte <= 6:
            score -= 30
        
        score = max(0, min(100, score))
        
        return {
            'score': score,
            'tickets_abertos': tickets_abertos,
            'tickets_resolvidos': tickets_resolvidos,
            'tempo_medio_resolucao_h': tempo_medio_resolucao,
            'nps_suporte': nps_suporte,
            'qualidade_suporte': 'excelente' if score >= 80 else 'boa' if score >= 60 else 'precisa_melhorar'
        }
    
    def calcular_metrica_financeiro(self) -> Dict:
        """
        Métrica 5: Financeiro (20%)
        
        Indicadores:
        - Pagamentos em dia
        - Inadimplência
        - Crescimento de receita
        - Valor do contrato
        
        Returns:
            Dict com score (0-100) e detalhes
        """
        # Simular dados
        pagamentos_em_dia = self._get_pagamentos_em_dia()
        dias_atraso = self._get_dias_atraso()
        crescimento_receita = self._get_crescimento_receita()
        
        score = 100  # Começar com 100
        
        # Deduzir por atraso (máximo -50)
        if dias_atraso > 30:
            score -= 50
        elif dias_atraso > 15:
            score -= 40
        elif dias_atraso > 7:
            score -= 30
        elif dias_atraso > 0:
            score -= 20
        
        # Deduzir por inadimplência (máximo -30)
        if pagamentos_em_dia < 0.5:  # <50%
            score -= 30
        elif pagamentos_em_dia < 0.8:
            score -= 20
        elif pagamentos_em_dia < 0.95:
            score -= 10
        
        # Bônus por crescimento (máximo +20)
        if crescimento_receita > 0.20:  # >20%
            score += 20
        elif crescimento_receita > 0.10:
            score += 10
        elif crescimento_receita > 0:
            score += 5
        
        score = max(0, min(100, score))
        
        return {
            'score': score,
            'pagamentos_em_dia_pct': round(pagamentos_em_dia * 100, 2),
            'dias_atraso': dias_atraso,
            'crescimento_receita_pct': round(crescimento_receita * 100, 2),
            'status_financeiro': 'saudavel' if score >= 80 else 'atencao' if score >= 50 else 'critico'
        }
    
    def _determinar_status(self, score: float) -> str:
        """Determina status baseado no score"""
        if score >= self.THRESHOLD_VERDE:
            return 'verde'
        elif score >= self.THRESHOLD_AMARELO:
            return 'amarelo'
        else:
            return 'vermelho'
    
    def _calcular_risco_churn(self, score: float) -> Dict:
        """Calcula risco de churn"""
        if score >= 80:
            nivel = 'baixo'
            probabilidade = 5
        elif score >= 50:
            nivel = 'medio'
            probabilidade = 30
        else:
            nivel = 'alto'
            probabilidade = 70
        
        return {
            'nivel': nivel,
            'probabilidade_pct': probabilidade,
            'acao_requerida': nivel in ['medio', 'alto']
        }
    
    def _gerar_recomendacoes(self) -> List[str]:
        """Gera recomendações baseadas nas métricas"""
        recomendacoes = []
        
        # Uso
        if self.metricas['uso']['score'] < 50:
            recomendacoes.append("🔴 Baixo uso do sistema. Agendar treinamento de reciclagem.")
        
        # Adoção
        if self.metricas['adocao']['score'] < 50:
            recomendacoes.append("🔴 Baixa adoção de features. Apresentar funcionalidades não utilizadas.")
        
        # Engajamento
        if self.metricas['engajamento']['score'] < 40:
            recomendacoes.append("🔴 Baixo engajamento. Agendar reunião de alinhamento.")
        
        # Suporte
        if self.metricas['suporte']['tickets_abertos'] > 3:
            recomendacoes.append("🟡 Múltiplos tickets abertos. Priorizar resolução.")
        
        # Financeiro
        if self.metricas['financeiro']['dias_atraso'] > 0:
            recomendacoes.append("🔴 Pagamento em atraso. Contatar financeiro do cliente.")
        
        if not recomendacoes:
            recomendacoes.append("✅ Cliente saudável. Manter acompanhamento regular.")
        
        return recomendacoes
    
    # Métodos auxiliares (simular dados - em produção, buscar do DB)
    
    def _get_logins_ultimos_30_dias(self) -> int:
        """Simula logins dos últimos 30 dias"""
        return 15  # Exemplo
    
    def _get_ultima_atividade(self) -> datetime:
        """Simula última atividade"""
        return datetime.now() - timedelta(days=2)
    
    def _get_tempo_medio_sessao(self) -> int:
        """Simula tempo médio de sessão em minutos"""
        return 25
    
    def _get_features_utilizadas(self) -> List[str]:
        """Simula features utilizadas"""
        return ['cotacoes', 'pedidos', 'entregas', 'dashboard']
    
    def _get_acoes_ultimos_30_dias(self) -> int:
        """Simula ações realizadas"""
        return 45
    
    def _get_interacoes_suporte(self) -> int:
        """Simula interações com suporte"""
        return 2
    
    def _get_feedback_fornecido(self) -> int:
        """Simula feedback fornecido"""
        return 1
    
    def _get_tickets_abertos(self) -> int:
        """Simula tickets abertos"""
        return 1
    
    def _get_tickets_resolvidos(self) -> int:
        """Simula tickets resolvidos"""
        return 8
    
    def _get_tempo_medio_resolucao(self) -> float:
        """Simula tempo médio de resolução em horas"""
        return 18.5
    
    def _get_nps_suporte(self) -> int:
        """Simula NPS do suporte (0-10)"""
        return 9
    
    def _get_pagamentos_em_dia(self) -> float:
        """Simula taxa de pagamentos em dia (0-1)"""
        return 0.95
    
    def _get_dias_atraso(self) -> int:
        """Simula dias de atraso no pagamento"""
        return 0
    
    def _get_crescimento_receita(self) -> float:
        """Simula crescimento de receita (0-1)"""
        return 0.15


class ChurnAlertSystem:
    """Sistema de Alertas de Risco de Churn"""
    
    def __init__(self, db=None):
        self.db = db
    
    def verificar_alertas(self) -> List[Dict]:
        """
        Verifica todos os clientes e gera alertas de risco
        
        Returns:
            Lista de alertas de clientes em risco
        """
        alertas = []
        
        # Simular lista de clientes (em produção, buscar do DB)
        clientes = self._get_clientes()
        
        for cliente in clientes:
            calculator = HealthScoreCalculator(cliente['id'])
            resultado = calculator.calcular_health_score()
            
            # Gerar alerta se em risco
            if resultado['risco_churn']['nivel'] in ['medio', 'alto']:
                alerta = {
                    'cliente_id': cliente['id'],
                    'cliente_nome': cliente['nome'],
                    'health_score': resultado['health_score'],
                    'status': resultado['status'],
                    'risco_churn': resultado['risco_churn'],
                    'recomendacoes': resultado['recomendacoes'],
                    'urgencia': 'alta' if resultado['risco_churn']['nivel'] == 'alto' else 'media',
                    'data_alerta': datetime.now().isoformat()
                }
                alertas.append(alerta)
        
        # Ordenar por urgência e score
        alertas.sort(key=lambda x: (x['urgencia'] == 'alta', -x['health_score']), reverse=True)
        
        return alertas
    
    def _get_clientes(self) -> List[Dict]:
        """Simula lista de clientes"""
        return [
            {'id': 'cli_001', 'nome': 'Empresa ABC Ltda'},
            {'id': 'cli_002', 'nome': 'Transportadora XYZ'},
            {'id': 'cli_003', 'nome': 'Logística 123'}
        ]
