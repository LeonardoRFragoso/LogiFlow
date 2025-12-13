"""
LogiFlow CRM - Celery Configuration
"""

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('logiflow')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Scheduled tasks
app.conf.beat_schedule = {
    'verificar-cnh-vencendo': {
        'task': 'apps.frota.tasks.verificar_cnh_vencendo',
        'schedule': crontab(hour=8, minute=0),
    },
    'atualizar-sla-entregas': {
        'task': 'apps.operacional.tasks.atualizar_sla_entregas',
        'schedule': crontab(minute='*/15'),
    },
    'limpar-tokens-expirados': {
        'task': 'apps.core.tasks.limpar_tokens_expirados',
        'schedule': crontab(hour=3, minute=0),
    },
}
