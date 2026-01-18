"""
Tasks do Celery para processamento assíncrono
"""

from celery_app import celery
from loguru import logger


@celery.task(name='tasks.process_email_queue')
def process_email_queue():
    """
    Processa fila de emails pendentes
    """
    try:
        logger.info("📧 Processando fila de emails...")
        # TODO: Implementar fila de emails
        return {"status": "success", "processed": 0}
    except Exception as e:
        logger.error(f"❌ Erro ao processar emails: {str(e)}")
        raise


@celery.task(name='tasks.check_subscriptions')
def check_subscriptions():
    """
    Verifica status das assinaturas e renova/cancela conforme necessário
    """
    try:
        logger.info("💳 Verificando status das assinaturas...")
        # TODO: Implementar verificação de assinaturas
        return {"status": "success", "checked": 0}
    except Exception as e:
        logger.error(f"❌ Erro ao verificar assinaturas: {str(e)}")
        raise


@celery.task(name='tasks.send_email_async')
def send_email_async(email_type: str, recipient: str, **kwargs):
    """
    Envia email de forma assíncrona
    """
    try:
        from services.email_service import email_service
        
        logger.info(f"📧 Enviando email {email_type} para {recipient}")
        
        if email_type == "demo_confirmation":
            result = email_service.send_demo_confirmation(**kwargs)
        elif email_type == "welcome":
            result = email_service.send_welcome_email(**kwargs)
        elif email_type == "payment_confirmation":
            result = email_service.send_payment_confirmation(**kwargs)
        else:
            raise ValueError(f"Tipo de email desconhecido: {email_type}")
        
        if result:
            logger.success(f"✅ Email enviado: {email_type} para {recipient}")
        else:
            logger.error(f"❌ Falha ao enviar email: {email_type} para {recipient}")
        
        return result
    except Exception as e:
        logger.error(f"❌ Erro ao enviar email: {str(e)}")
        raise


@celery.task(name='tasks.provision_tenant_async')
def provision_tenant_async(lead_id: int, payment_data: dict):
    """
    Provisiona tenant de forma assíncrona após pagamento
    """
    try:
        from services.tenant_provisioning import provision_tenant_from_payment
        from database import SessionLocal
        from models import Lead
        
        logger.info(f"🚀 Provisionando tenant para lead {lead_id}...")
        
        db = SessionLocal()
        try:
            lead = db.query(Lead).filter(Lead.id == lead_id).first()
            if not lead:
                raise ValueError(f"Lead {lead_id} não encontrado")
            
            tenant = provision_tenant_from_payment(
                company_name=lead.company or lead.name,
                contact_name=lead.name,
                contact_email=lead.email,
                contact_phone=lead.phone or "",
                plan=payment_data.get("plan", "starter"),
                amount=payment_data.get("amount", 0),
                gateway_data=payment_data.get("gateway_data", {}),
                lead_id=lead_id
            )
            
            if tenant:
                logger.success(f"✅ Tenant provisionado: {tenant.subdomain}")
                return {"status": "success", "tenant_id": tenant.id}
            else:
                raise Exception("Falha ao provisionar tenant")
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"❌ Erro ao provisionar tenant: {str(e)}")
        raise
