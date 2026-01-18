"""
LogiFlow CRM - Serviço de Forecast de Vendas Enterprise
========================================================
Previsão inteligente de receita baseada no pipeline
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from loguru import logger

from models import Opportunity, SalesStage
from models_crm_enterprise import SalesForecast


class SalesForecastService:
    """
    Serviço de forecast de vendas
    
    Categorias de forecast:
    - Comprometido: oportunidades em negociação (probabilidade >= 70%)
    - Upside: oportunidades em proposta (probabilidade 40-69%)
    - Pipeline: todas as oportunidades abertas (probabilidade > 0%)
    """
    
    STAGE_PROBABILITY = {
        SalesStage.LEAD.value: 10,
        SalesStage.QUALIFICADO.value: 25,
        SalesStage.PROPOSTA.value: 50,
        SalesStage.NEGOCIACAO.value: 75,
        SalesStage.GANHO.value: 100,
        SalesStage.PERDIDO.value: 0
    }
    
    def __init__(self, db: Session):
        self.db = db
    
    def calcular_forecast_mensal(
        self,
        ano: int,
        mes: int,
        responsavel_id: Optional[str] = None,
        salvar: bool = True
    ) -> Dict[str, Any]:
        """
        Calcula forecast para um mês específico
        
        Args:
            ano: Ano do forecast
            mes: Mês do forecast
            responsavel_id: ID do responsável (None = todos)
            salvar: Se deve salvar no banco
        
        Returns:
            Dados completos do forecast
        """
        primeiro_dia = datetime(ano, mes, 1)
        if mes == 12:
            ultimo_dia = datetime(ano + 1, 1, 1) - timedelta(days=1)
        else:
            ultimo_dia = datetime(ano, mes + 1, 1) - timedelta(days=1)
        
        query = self.db.query(Opportunity).filter(
            and_(
                Opportunity.sales_stage.notin_([SalesStage.GANHO.value, SalesStage.PERDIDO.value]),
                Opportunity.data_prevista_fechamento.between(primeiro_dia, ultimo_dia)
            )
        )
        
        if responsavel_id:
            query = query.filter(Opportunity.responsavel_id == responsavel_id)
        
        oportunidades = query.all()
        
        valor_comprometido = 0.0
        valor_upside = 0.0
        valor_pipeline = 0.0
        valor_realizado = 0.0
        
        opps_comprometidas = []
        opps_upside = []
        opps_pipeline = []
        
        for opp in oportunidades:
            prob = opp.probabilidade or self.STAGE_PROBABILITY.get(opp.sales_stage, 0)
            valor = opp.valor_estimado or 0
            
            valor_pipeline += valor
            
            if prob >= 70:
                valor_comprometido += valor
                opps_comprometidas.append({
                    'id': opp.id,
                    'nome': opp.nome,
                    'valor': valor,
                    'probabilidade': prob,
                    'stage': opp.sales_stage
                })
            elif prob >= 40:
                valor_upside += valor
                opps_upside.append({
                    'id': opp.id,
                    'nome': opp.nome,
                    'valor': valor,
                    'probabilidade': prob,
                    'stage': opp.sales_stage
                })
            else:
                opps_pipeline.append({
                    'id': opp.id,
                    'nome': opp.nome,
                    'valor': valor,
                    'probabilidade': prob,
                    'stage': opp.sales_stage
                })
        
        opps_ganhas = self.db.query(Opportunity).filter(
            and_(
                Opportunity.sales_stage == SalesStage.GANHO.value,
                Opportunity.data_fechamento != None,
                extract('year', Opportunity.data_fechamento) == ano,
                extract('month', Opportunity.data_fechamento) == mes
            )
        )
        
        if responsavel_id:
            opps_ganhas = opps_ganhas.filter(Opportunity.responsavel_id == responsavel_id)
        
        valor_realizado = opps_ganhas.with_entities(
            func.sum(Opportunity.valor_estimado)
        ).scalar() or 0
        
        if salvar:
            forecast_existente = self.db.query(SalesForecast).filter(
                and_(
                    SalesForecast.ano == ano,
                    SalesForecast.mes == mes,
                    SalesForecast.responsavel_id == responsavel_id
                )
            ).first()
            
            if forecast_existente:
                forecast_existente.valor_previsto = valor_pipeline
                forecast_existente.valor_comprometido = valor_comprometido
                forecast_existente.valor_upside = valor_upside
                forecast_existente.valor_realizado = valor_realizado
                forecast_existente.numero_oportunidades = len(oportunidades)
                forecast_existente.atualizado_em = datetime.utcnow()
            else:
                forecast = SalesForecast(
                    ano=ano,
                    mes=mes,
                    responsavel_id=responsavel_id,
                    valor_previsto=valor_pipeline,
                    valor_comprometido=valor_comprometido,
                    valor_upside=valor_upside,
                    valor_realizado=valor_realizado,
                    numero_oportunidades=len(oportunidades)
                )
                self.db.add(forecast)
            
            self.db.commit()
        
        percentual_atingimento = (valor_realizado / valor_comprometido * 100) if valor_comprometido > 0 else 0
        
        return {
            'periodo': {
                'ano': ano,
                'mes': mes,
                'mes_nome': primeiro_dia.strftime('%B'),
                'primeiro_dia': primeiro_dia.isoformat(),
                'ultimo_dia': ultimo_dia.isoformat()
            },
            'valores': {
                'pipeline_total': round(float(valor_pipeline), 2),
                'comprometido': round(float(valor_comprometido), 2),
                'upside': round(float(valor_upside), 2),
                'realizado': round(float(valor_realizado), 2)
            },
            'oportunidades': {
                'total': len(oportunidades),
                'comprometidas': len(opps_comprometidas),
                'upside': len(opps_upside),
                'pipeline': len(opps_pipeline)
            },
            'atingimento': {
                'percentual': round(percentual_atingimento, 2),
                'faltante': round(float(valor_comprometido - valor_realizado), 2) if valor_comprometido > valor_realizado else 0
            },
            'detalhamento': {
                'comprometidas': opps_comprometidas[:10],
                'upside': opps_upside[:10],
                'pipeline': opps_pipeline[:10]
            },
            'responsavel_id': responsavel_id,
            'gerado_em': datetime.utcnow().isoformat()
        }
    
    def calcular_forecast_trimestral(
        self,
        ano: int,
        trimestre: int,
        responsavel_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calcula forecast para um trimestre
        
        Args:
            ano: Ano
            trimestre: 1, 2, 3 ou 4
            responsavel_id: ID do responsável (opcional)
        
        Returns:
            Forecast consolidado do trimestre
        """
        meses = {
            1: [1, 2, 3],
            2: [4, 5, 6],
            3: [7, 8, 9],
            4: [10, 11, 12]
        }
        
        meses_trimestre = meses.get(trimestre, [1, 2, 3])
        
        forecasts_mensais = []
        valor_total_pipeline = 0
        valor_total_comprometido = 0
        valor_total_upside = 0
        valor_total_realizado = 0
        
        for mes in meses_trimestre:
            forecast_mes = self.calcular_forecast_mensal(ano, mes, responsavel_id, salvar=False)
            forecasts_mensais.append(forecast_mes)
            
            valor_total_pipeline += forecast_mes['valores']['pipeline_total']
            valor_total_comprometido += forecast_mes['valores']['comprometido']
            valor_total_upside += forecast_mes['valores']['upside']
            valor_total_realizado += forecast_mes['valores']['realizado']
        
        percentual_atingimento = (valor_total_realizado / valor_total_comprometido * 100) if valor_total_comprometido > 0 else 0
        
        return {
            'periodo': {
                'ano': ano,
                'trimestre': trimestre,
                'meses': meses_trimestre
            },
            'valores': {
                'pipeline_total': round(valor_total_pipeline, 2),
                'comprometido': round(valor_total_comprometido, 2),
                'upside': round(valor_total_upside, 2),
                'realizado': round(valor_total_realizado, 2)
            },
            'atingimento': {
                'percentual': round(percentual_atingimento, 2),
                'faltante': round(valor_total_comprometido - valor_total_realizado, 2) if valor_total_comprometido > valor_total_realizado else 0
            },
            'detalhamento_mensal': forecasts_mensais,
            'responsavel_id': responsavel_id,
            'gerado_em': datetime.utcnow().isoformat()
        }
    
    def calcular_forecast_anual(
        self,
        ano: int,
        responsavel_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calcula forecast para o ano completo
        """
        forecasts_mensais = []
        valor_total_pipeline = 0
        valor_total_comprometido = 0
        valor_total_upside = 0
        valor_total_realizado = 0
        
        for mes in range(1, 13):
            forecast_mes = self.calcular_forecast_mensal(ano, mes, responsavel_id, salvar=False)
            forecasts_mensais.append(forecast_mes)
            
            valor_total_pipeline += forecast_mes['valores']['pipeline_total']
            valor_total_comprometido += forecast_mes['valores']['comprometido']
            valor_total_upside += forecast_mes['valores']['upside']
            valor_total_realizado += forecast_mes['valores']['realizado']
        
        percentual_atingimento = (valor_total_realizado / valor_total_comprometido * 100) if valor_total_comprometido > 0 else 0
        
        return {
            'periodo': {
                'ano': ano
            },
            'valores': {
                'pipeline_total': round(valor_total_pipeline, 2),
                'comprometido': round(valor_total_comprometido, 2),
                'upside': round(valor_total_upside, 2),
                'realizado': round(valor_total_realizado, 2)
            },
            'atingimento': {
                'percentual': round(percentual_atingimento, 2),
                'faltante': round(valor_total_comprometido - valor_total_realizado, 2) if valor_total_comprometido > valor_total_realizado else 0
            },
            'detalhamento_mensal': forecasts_mensais,
            'responsavel_id': responsavel_id,
            'gerado_em': datetime.utcnow().isoformat()
        }
