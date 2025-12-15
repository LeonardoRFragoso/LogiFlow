"""
LogiFlow CRM - Agendador de Tarefas Automáticas
Sistema de cron jobs para NPS, CSAT, Health Score e Churn Alerts
"""

from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
import logging

from database import SessionLocal
from services.nps_service import NPSService
from services.health_score import ChurnAlertSystem
from models import NPSSurvey, Tenant, SurveyStatus

logger = logging.getLogger(__name__)


class AutomatedSurveyScheduler:
    """Agendador de Pesquisas Automáticas"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
    
    def start(self):
        """Inicia o agendador"""
        logger.info("🚀 Iniciando agendador de pesquisas automáticas...")
        
        # Agendar pesquisas NPS (30 dias) - Executar diariamente às 10:00
        self.scheduler.add_job(
            func=self.agendar_nps_30_dias,
            trigger=CronTrigger(hour=10, minute=0),
            id='nps_30_dias',
            name='Agendar Pesquisas NPS 30 dias',
            replace_existing=True
        )
        
        # Agendar pesquisas NPS (90 dias) - Executar toda segunda-feira às 10:00
        self.scheduler.add_job(
            func=self.agendar_nps_90_dias,
            trigger=CronTrigger(day_of_week='mon', hour=10, minute=0),
            id='nps_90_dias',
            name='Agendar Pesquisas NPS 90 dias',
            replace_existing=True
        )
        
        # Verificar alertas de churn - Executar a cada 6 horas
        self.scheduler.add_job(
            func=self.verificar_churn_alerts,
            trigger=CronTrigger(hour='*/6'),
            id='churn_alerts',
            name='Verificar Alertas de Churn',
            replace_existing=True
        )
        
        # Expirar pesquisas antigas - Executar diariamente às 02:00
        self.scheduler.add_job(
            func=self.expirar_pesquisas_antigas,
            trigger=CronTrigger(hour=2, minute=0),
            id='expirar_pesquisas',
            name='Expirar Pesquisas Antigas',
            replace_existing=True
        )
        
        self.scheduler.start()
        logger.info("✅ Agendador iniciado com sucesso!")
    
    def stop(self):
        """Para o agendador"""
        self.scheduler.shutdown()
        logger.info("🛑 Agendador parado")
    
    def agendar_nps_30_dias(self):
        """Agenda pesquisas NPS de 30 dias para todos os tenants"""
        logger.info("📊 Agendando pesquisas NPS (30 dias)...")
        
        db = SessionLocal()
        try:
            # Buscar todos os tenants ativos
            tenants = db.query(Tenant).filter(Tenant.status == 'active').all()
            
            total_pesquisas = 0
            for tenant in tenants:
                try:
                    nps_service = NPSService(db)
                    pesquisas = nps_service.agendar_pesquisas_automaticas(str(tenant.id))
                    total_pesquisas += len(pesquisas)
                except Exception as e:
                    logger.error(f"Erro ao agendar NPS para tenant {tenant.id}: {e}")
            
            logger.info(f"✅ {total_pesquisas} pesquisas NPS (30 dias) agendadas para {len(tenants)} tenants")
        
        except Exception as e:
            logger.error(f"Erro ao agendar NPS 30 dias: {e}")
        finally:
            db.close()
    
    def agendar_nps_90_dias(self):
        """Agenda pesquisas NPS de 90 dias para clientes antigos"""
        logger.info("📊 Agendando pesquisas NPS (90 dias)...")
        
        db = SessionLocal()
        try:
            # Buscar todos os tenants ativos
            tenants = db.query(Tenant).filter(Tenant.status == 'active').all()
            
            total_pesquisas = 0
            for tenant in tenants:
                try:
                    nps_service = NPSService(db)
                    # Este método já filtra clientes antigos para 90 dias
                    pesquisas = nps_service.agendar_pesquisas_automaticas(str(tenant.id))
                    total_pesquisas += len(pesquisas)
                except Exception as e:
                    logger.error(f"Erro ao agendar NPS 90 dias para tenant {tenant.id}: {e}")
            
            logger.info(f"✅ {total_pesquisas} pesquisas NPS (90 dias) agendadas")
        
        except Exception as e:
            logger.error(f"Erro ao agendar NPS 90 dias: {e}")
        finally:
            db.close()
    
    def verificar_churn_alerts(self):
        """Verifica e atualiza alertas de churn para todos os clientes"""
        logger.info("🚨 Verificando alertas de churn...")
        
        db = SessionLocal()
        try:
            alert_system = ChurnAlertSystem(db)
            
            # Buscar todos os tenants ativos
            tenants = db.query(Tenant).filter(Tenant.status == 'active').all()
            
            total_alertas = 0
            for tenant in tenants:
                try:
                    alertas = alert_system.verificar_alertas(str(tenant.id))
                    total_alertas += len(alertas)
                except Exception as e:
                    logger.error(f"Erro ao verificar churn para tenant {tenant.id}: {e}")
            
            logger.info(f"✅ {total_alertas} alertas de churn verificados")
        
        except Exception as e:
            logger.error(f"Erro ao verificar churn alerts: {e}")
        finally:
            db.close()
    
    def expirar_pesquisas_antigas(self):
        """Expira pesquisas não respondidas após data de expiração"""
        logger.info("⏰ Expirando pesquisas antigas...")
        
        db = SessionLocal()
        try:
            from models import CSATSurvey
            from sqlalchemy import and_
            
            agora = datetime.utcnow()
            
            # Expirar NPS
            nps_expiradas = db.query(NPSSurvey).filter(
                and_(
                    NPSSurvey.status == SurveyStatus.ENVIADA.value,
                    NPSSurvey.data_expiracao < agora
                )
            ).update({"status": SurveyStatus.EXPIRADA.value}, synchronize_session=False)
            
            # Expirar CSAT
            csat_expiradas = db.query(CSATSurvey).filter(
                and_(
                    CSATSurvey.status == SurveyStatus.ENVIADA.value,
                    CSATSurvey.data_expiracao < agora
                )
            ).update({"status": SurveyStatus.EXPIRADA.value}, synchronize_session=False)
            
            db.commit()
            
            logger.info(f"✅ {nps_expiradas} NPS e {csat_expiradas} CSAT expiradas")
        
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao expirar pesquisas: {e}")
        finally:
            db.close()


# Instância global do agendador
scheduler = AutomatedSurveyScheduler()


def start_scheduler():
    """Função para iniciar o agendador"""
    scheduler.start()


def stop_scheduler():
    """Função para parar o agendador"""
    scheduler.stop()

