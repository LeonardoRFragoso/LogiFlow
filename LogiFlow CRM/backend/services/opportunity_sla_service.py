"""
LogiFlow CRM - Serviço de SLA e Aging de Oportunidades
=======================================================
Monitoramento de tempo e alertas de oportunidades estagnadas
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Dict, Any, List
from loguru import logger

from models import Opportunity, OpportunityStageHistory, SalesStage
from models_crm_enterprise import OpportunitySLALog


class OpportunitySLAService:
    """
    Serviço de monitoramento de SLA de oportunidades
    
    SLA por estágio (dias máximos):
    - Lead: 7 dias
    - Qualificado: 14 dias
    - Proposta: 21 dias
    - Negociação: 30 dias
    """
    
    SLA_DIAS = {
        SalesStage.LEAD.value: 7,
        SalesStage.QUALIFICADO.value: 14,
        SalesStage.PROPOSTA.value: 21,
        SalesStage.NEGOCIACAO.value: 30
    }
    
    def __init__(self, db: Session):
        self.db = db
    
    def calcular_dias_no_estagio(self, oportunidade: Opportunity) -> int:
        """
        Calcula quantos dias a oportunidade está no estágio atual
        """
        ultimo_historico = self.db.query(OpportunityStageHistory).filter(
            OpportunityStageHistory.oportunidade_id == oportunidade.id
        ).order_by(OpportunityStageHistory.data_mudanca.desc()).first()
        
        if ultimo_historico:
            data_entrada_estagio = ultimo_historico.data_mudanca
        else:
            data_entrada_estagio = oportunidade.criado_em
        
        return (datetime.utcnow() - data_entrada_estagio).days
    
    def verificar_sla_oportunidade(
        self,
        oportunidade: Opportunity,
        salvar_log: bool = True
    ) -> Dict[str, Any]:
        """
        Verifica status do SLA de uma oportunidade
        
        Returns:
            {
                'oportunidade_id': 'ABC123',
                'estagio_atual': 'proposta',
                'dias_no_estagio': 18,
                'sla_dias': 21,
                'dias_restantes': 3,
                'status_sla': 'ok',  # ok, alerta, vencido
                'percentual_sla': 85.7
            }
        """
        if oportunidade.sales_stage in [SalesStage.GANHO.value, SalesStage.PERDIDO.value]:
            return {
                'oportunidade_id': oportunidade.id,
                'estagio_atual': oportunidade.sales_stage,
                'status_sla': 'fechado',
                'mensagem': 'Oportunidade já foi fechada'
            }
        
        dias_no_estagio = self.calcular_dias_no_estagio(oportunidade)
        sla_dias = self.SLA_DIAS.get(oportunidade.sales_stage, 30)
        dias_restantes = sla_dias - dias_no_estagio
        percentual_sla = (dias_no_estagio / sla_dias * 100) if sla_dias > 0 else 0
        
        if dias_restantes < 0:
            status_sla = 'vencido'
        elif dias_restantes <= 3:
            status_sla = 'alerta'
        else:
            status_sla = 'ok'
        
        if salvar_log:
            log = OpportunitySLALog(
                oportunidade_id=oportunidade.id,
                estagio=oportunidade.sales_stage,
                dias_no_estagio=dias_no_estagio,
                sla_estagio_dias=sla_dias,
                status_sla=status_sla
            )
            self.db.add(log)
            self.db.commit()
        
        return {
            'oportunidade_id': oportunidade.id,
            'oportunidade_nome': oportunidade.nome,
            'cliente_nome': oportunidade.cliente.razao_social if oportunidade.cliente else None,
            'estagio_atual': oportunidade.sales_stage,
            'dias_no_estagio': dias_no_estagio,
            'sla_dias': sla_dias,
            'dias_restantes': dias_restantes,
            'status_sla': status_sla,
            'percentual_sla': round(percentual_sla, 2),
            'valor_oportunidade': oportunidade.valor_estimado or 0,
            'responsavel': oportunidade.responsavel.nome if oportunidade.responsavel else 'Não atribuído',
            'verificado_em': datetime.utcnow().isoformat()
        }
    
    def listar_oportunidades_vencidas(self) -> List[Dict[str, Any]]:
        """
        Lista todas as oportunidades com SLA vencido
        """
        oportunidades = self.db.query(Opportunity).filter(
            Opportunity.sales_stage.notin_([SalesStage.GANHO.value, SalesStage.PERDIDO.value])
        ).all()
        
        vencidas = []
        for opp in oportunidades:
            sla_info = self.verificar_sla_oportunidade(opp, salvar_log=False)
            if sla_info.get('status_sla') == 'vencido':
                vencidas.append(sla_info)
        
        return sorted(vencidas, key=lambda x: x['dias_no_estagio'], reverse=True)
    
    def listar_oportunidades_em_alerta(self) -> List[Dict[str, Any]]:
        """
        Lista oportunidades próximas do vencimento do SLA
        """
        oportunidades = self.db.query(Opportunity).filter(
            Opportunity.sales_stage.notin_([SalesStage.GANHO.value, SalesStage.PERDIDO.value])
        ).all()
        
        alertas = []
        for opp in oportunidades:
            sla_info = self.verificar_sla_oportunidade(opp, salvar_log=False)
            if sla_info.get('status_sla') in ['alerta', 'vencido']:
                alertas.append(sla_info)
        
        return sorted(alertas, key=lambda x: x['dias_restantes'])
    
    def calcular_aging_pipeline(self) -> Dict[str, Any]:
        """
        Calcula aging (envelhecimento) do pipeline completo
        
        Returns:
            Estatísticas de aging por estágio
        """
        oportunidades = self.db.query(Opportunity).filter(
            Opportunity.sales_stage.notin_([SalesStage.GANHO.value, SalesStage.PERDIDO.value])
        ).all()
        
        aging_por_estagio = {}
        
        for stage in SalesStage:
            if stage.value in [SalesStage.GANHO.value, SalesStage.PERDIDO.value]:
                continue
            
            opps_estagio = [o for o in oportunidades if o.sales_stage == stage.value]
            
            if not opps_estagio:
                aging_por_estagio[stage.value] = {
                    'total_oportunidades': 0,
                    'dias_medio': 0,
                    'dias_minimo': 0,
                    'dias_maximo': 0,
                    'sla_dias': self.SLA_DIAS.get(stage.value, 30),
                    'dentro_sla': 0,
                    'fora_sla': 0
                }
                continue
            
            dias_lista = []
            dentro_sla = 0
            fora_sla = 0
            
            for opp in opps_estagio:
                dias = self.calcular_dias_no_estagio(opp)
                dias_lista.append(dias)
                
                sla = self.SLA_DIAS.get(stage.value, 30)
                if dias <= sla:
                    dentro_sla += 1
                else:
                    fora_sla += 1
            
            aging_por_estagio[stage.value] = {
                'total_oportunidades': len(opps_estagio),
                'dias_medio': round(sum(dias_lista) / len(dias_lista), 1) if dias_lista else 0,
                'dias_minimo': min(dias_lista) if dias_lista else 0,
                'dias_maximo': max(dias_lista) if dias_lista else 0,
                'sla_dias': self.SLA_DIAS.get(stage.value, 30),
                'dentro_sla': dentro_sla,
                'fora_sla': fora_sla,
                'percentual_fora_sla': round((fora_sla / len(opps_estagio) * 100), 2) if opps_estagio else 0
            }
        
        total_oportunidades = len(oportunidades)
        total_fora_sla = sum(v['fora_sla'] for v in aging_por_estagio.values())
        
        return {
            'resumo': {
                'total_oportunidades': total_oportunidades,
                'total_fora_sla': total_fora_sla,
                'percentual_fora_sla': round((total_fora_sla / total_oportunidades * 100), 2) if total_oportunidades > 0 else 0
            },
            'por_estagio': aging_por_estagio,
            'gerado_em': datetime.utcnow().isoformat()
        }
    
    def verificar_todas_oportunidades(self) -> Dict[str, Any]:
        """
        Verifica SLA de todas as oportunidades abertas e salva logs
        """
        oportunidades = self.db.query(Opportunity).filter(
            Opportunity.sales_stage.notin_([SalesStage.GANHO.value, SalesStage.PERDIDO.value])
        ).all()
        
        verificadas = 0
        ok_count = 0
        alerta_count = 0
        vencido_count = 0
        
        for opp in oportunidades:
            try:
                sla_info = self.verificar_sla_oportunidade(opp, salvar_log=True)
                verificadas += 1
                
                if sla_info['status_sla'] == 'ok':
                    ok_count += 1
                elif sla_info['status_sla'] == 'alerta':
                    alerta_count += 1
                elif sla_info['status_sla'] == 'vencido':
                    vencido_count += 1
                    
            except Exception as e:
                logger.error(f"Erro ao verificar SLA da oportunidade {opp.id}: {e}")
        
        return {
            'total_verificadas': verificadas,
            'status': {
                'ok': ok_count,
                'alerta': alerta_count,
                'vencido': vencido_count
            },
            'percentuais': {
                'ok': round((ok_count / verificadas * 100), 2) if verificadas > 0 else 0,
                'alerta': round((alerta_count / verificadas * 100), 2) if verificadas > 0 else 0,
                'vencido': round((vencido_count / verificadas * 100), 2) if verificadas > 0 else 0
            },
            'timestamp': datetime.utcnow().isoformat()
        }
