"""
Configuração do Celery para LogiFlow CRM
"""

from celery import Celery
from celery.schedules import crontab
import os

# Configuração do broker Redis
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "redis123")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

CELERY_BROKER_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"
CELERY_RESULT_BACKEND = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"

# Criar instância do Celery
celery = Celery(
    "logiflow",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

# Configurações do Celery
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Sao_Paulo",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutos
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
)

# Configuração de tarefas periódicas (Beat)
celery.conf.beat_schedule = {
    'process-pending-emails': {
        'task': 'tasks.process_email_queue',
        'schedule': crontab(minute='*/5'),  # A cada 5 minutos
    },
    'check-subscription-status': {
        'task': 'tasks.check_subscriptions',
        'schedule': crontab(hour=2, minute=0),  # Diariamente às 2h
    },
}

# Importar tasks manualmente (tasks.py está no mesmo diretório)
# Isso garante que as tasks sejam registradas no Celery
try:
    import tasks
except ImportError as e:
    print(f"Warning: Could not import tasks: {e}")


@celery.task(bind=True)
def debug_task(self):
    """Task de debug"""
    print(f'Request: {self.request!r}')
