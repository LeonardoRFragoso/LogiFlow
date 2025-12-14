"""
Serviço de Provisionamento Automático de Tenants
Cria e configura automaticamente novos tenants após pagamento aprovado
"""

from loguru import logger
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets
import string

from models import Tenant, Subscription, Lead, StatusLead, PlanType
from database import SessionLocal


class TenantProvisioningService:
    """Serviço para provisionar automaticamente novos tenants"""
    
    def __init__(self):
        self.db = SessionLocal()
    
    def generate_subdomain(self, company_name: str) -> str:
        """
        Gera um subdomínio único baseado no nome da empresa
        """
        # Remover caracteres especiais e espaços
        subdomain = company_name.lower()
        subdomain = ''.join(c for c in subdomain if c.isalnum() or c == '-')
        subdomain = subdomain.replace(' ', '-')
        
        # Verificar se já existe
        existing = self.db.query(Tenant).filter(Tenant.subdomain == subdomain).first()
        
        if existing:
            # Adicionar número aleatório
            random_suffix = ''.join(secrets.choice(string.digits) for _ in range(4))
            subdomain = f"{subdomain}-{random_suffix}"
        
        return subdomain
    
    def generate_db_credentials(self, subdomain: str) -> dict:
        """
        Gera credenciais únicas para o banco de dados do tenant
        """
        db_name = f"logiflow_{subdomain}"
        db_user = f"user_{subdomain}"
        db_password = secrets.token_urlsafe(16)
        
        return {
            "db_name": db_name,
            "db_user": db_user,
            "db_password": db_password
        }
    
    def create_tenant(
        self,
        company_name: str,
        contact_name: str,
        contact_email: str,
        contact_phone: str,
        plan: str,
        lead_id: int = None
    ) -> Tenant:
        """
        Cria um novo tenant com todas as configurações necessárias
        """
        try:
            logger.info(f"🏢 Iniciando provisionamento do tenant: {company_name}")
            
            # Gerar subdomínio único
            subdomain = self.generate_subdomain(company_name)
            logger.info(f"   Subdomínio gerado: {subdomain}")
            
            # Gerar credenciais do banco
            db_creds = self.generate_db_credentials(subdomain)
            logger.info(f"   Credenciais do banco geradas: {db_creds['db_name']}")
            
            # Obter limites do plano
            from services.mercadopago_service import get_plan_config
            plan_config = get_plan_config(plan)
            
            max_users = plan_config.get("max_users", 5)
            max_vehicles = plan_config.get("max_vehicles", 10)
            max_orders_per_month = plan_config.get("max_orders_per_month", 500)
            
            # Criar tenant
            tenant = Tenant(
                subdomain=subdomain,
                company_name=company_name,
                contact_name=contact_name,
                contact_email=contact_email,
                contact_phone=contact_phone,
                db_name=db_creds["db_name"],
                db_user=db_creds["db_user"],
                db_password=db_creds["db_password"],
                status="active",
                plan=plan,
                max_users=max_users,
                max_vehicles=max_vehicles,
                max_orders_per_month=max_orders_per_month,
                trial_ends_at=datetime.utcnow() + timedelta(days=14)  # 14 dias de trial
            )
            
            self.db.add(tenant)
            self.db.commit()
            self.db.refresh(tenant)
            
            logger.success(f"✅ Tenant criado com sucesso! ID: {tenant.id}")
            
            # Criar banco de dados isolado para o tenant
            try:
                from services.database_provisioning import create_tenant_database
                
                logger.info("🗄️  Provisionando banco de dados isolado...")
                db_result = create_tenant_database(
                    db_name=db_creds["db_name"],
                    db_user=db_creds["db_user"],
                    db_password=db_creds["db_password"]
                )
                
                if db_result["success"]:
                    logger.success(f"✅ Banco de dados '{db_creds['db_name']}' criado e configurado!")
                else:
                    logger.warning(f"⚠️  Erro ao criar banco isolado: {db_result.get('error')}")
                    logger.info("   Tenant usará banco compartilhado temporariamente")
            except Exception as e:
                logger.warning(f"⚠️  Erro ao provisionar banco isolado: {e}")
                logger.info("   Tenant usará banco compartilhado temporariamente")
            
            # Atualizar lead se fornecido
            if lead_id:
                lead = self.db.query(Lead).filter(Lead.id == lead_id).first()
                if lead:
                    lead.status = StatusLead.CONVERTIDO.value
                    lead.tenant_id = tenant.id
                    lead.converted_at = datetime.utcnow()
                    self.db.commit()
                    logger.info(f"   Lead #{lead_id} marcado como convertido")
            
            # TODO: Criar banco de dados específico do tenant
            # TODO: Executar migrations no banco do tenant
            # TODO: Criar usuário admin inicial
            # TODO: Enviar email de boas-vindas
            # TODO: Configurar integrações padrão
            
            return tenant
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar tenant: {e}")
            self.db.rollback()
            raise
    
    def create_subscription(
        self,
        tenant_id: int,
        plan: str,
        amount: float,
        gateway: str,
        gateway_subscription_id: str = None,
        gateway_customer_id: str = None
    ) -> Subscription:
        """
        Cria uma assinatura para o tenant
        """
        try:
            logger.info(f"💳 Criando assinatura para tenant #{tenant_id}")
            
            subscription = Subscription(
                tenant_id=tenant_id,
                plan=plan,
                status="active",
                amount=amount,
                gateway=gateway,
                gateway_subscription_id=gateway_subscription_id,
                gateway_customer_id=gateway_customer_id,
                current_period_start=datetime.utcnow(),
                current_period_end=datetime.utcnow() + timedelta(days=30),
                trial_ends_at=datetime.utcnow() + timedelta(days=14)
            )
            
            self.db.add(subscription)
            self.db.commit()
            self.db.refresh(subscription)
            
            logger.success(f"✅ Assinatura criada com sucesso! ID: {subscription.id}")
            
            return subscription
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar assinatura: {e}")
            self.db.rollback()
            raise
    
    def provision_complete_tenant(
        self,
        company_name: str,
        contact_name: str,
        contact_email: str,
        contact_phone: str,
        plan: str,
        amount: float,
        gateway: str = "mercadopago",
        gateway_subscription_id: str = None,
        gateway_customer_id: str = None,
        lead_id: int = None
    ) -> dict:
        """
        Provisiona um tenant completo com assinatura
        """
        try:
            logger.info("=" * 60)
            logger.info("🚀 INICIANDO PROVISIONAMENTO COMPLETO DE TENANT")
            logger.info("=" * 60)
            
            # Criar tenant
            tenant = self.create_tenant(
                company_name=company_name,
                contact_name=contact_name,
                contact_email=contact_email,
                contact_phone=contact_phone,
                plan=plan,
                lead_id=lead_id
            )
            
            # Criar assinatura
            subscription = self.create_subscription(
                tenant_id=tenant.id,
                plan=plan,
                amount=amount,
                gateway=gateway,
                gateway_subscription_id=gateway_subscription_id,
                gateway_customer_id=gateway_customer_id
            )
            
            logger.info("=" * 60)
            logger.success("✅ PROVISIONAMENTO COMPLETO!")
            logger.info("=" * 60)
            logger.info(f"   Tenant ID: {tenant.id}")
            logger.info(f"   Subdomínio: {tenant.subdomain}")
            logger.info(f"   URL: https://{tenant.subdomain}.logiflow.com.br")
            logger.info(f"   Plano: {plan}")
            logger.info(f"   Subscription ID: {subscription.id}")
            logger.info("=" * 60)
            
            # Enviar email de boas-vindas
            try:
                from services.email_service import send_welcome_email
                
                # Gerar senha temporária
                import secrets
                import string
                temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
                
                logger.info("📧 Enviando email de boas-vindas...")
                send_welcome_email(
                    tenant_id=tenant.id,
                    company_name=tenant.company_name,
                    contact_name=contact_name,
                    contact_email=contact_email,
                    subdomain=tenant.subdomain,
                    plan=plan,
                    admin_email=contact_email,
                    admin_password=temp_password
                )
                logger.success("✅ Email de boas-vindas enviado!")
            except Exception as e:
                logger.warning(f"⚠️  Erro ao enviar email de boas-vindas: {e}")
            
            return {
                "success": True,
                "tenant": {
                    "id": tenant.id,
                    "subdomain": tenant.subdomain,
                    "company_name": tenant.company_name,
                    "url": f"https://{tenant.subdomain}.logiflow.com.br",
                    "status": tenant.status,
                    "plan": tenant.plan,
                    "max_users": tenant.max_users,
                    "trial_ends_at": tenant.trial_ends_at.isoformat() if tenant.trial_ends_at else None
                },
                "subscription": {
                    "id": subscription.id,
                    "status": subscription.status,
                    "amount": subscription.amount,
                    "current_period_end": subscription.current_period_end.isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Erro no provisionamento completo: {e}")
            raise
    
    def deactivate_tenant(self, tenant_id: int) -> bool:
        """
        Desativa um tenant (cancelamento)
        """
        try:
            tenant = self.db.query(Tenant).filter(Tenant.id == tenant_id).first()
            if not tenant:
                raise ValueError(f"Tenant #{tenant_id} não encontrado")
            
            tenant.status = "cancelled"
            tenant.cancelled_at = datetime.utcnow()
            
            # Desativar assinaturas ativas
            subscriptions = self.db.query(Subscription).filter(
                Subscription.tenant_id == tenant_id,
                Subscription.status == "active"
            ).all()
            
            for sub in subscriptions:
                sub.status = "cancelled"
                sub.cancelled_at = datetime.utcnow()
            
            self.db.commit()
            
            logger.info(f"🔴 Tenant #{tenant_id} desativado")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao desativar tenant: {e}")
            self.db.rollback()
            raise
    
    def __del__(self):
        """Fechar sessão do banco ao destruir objeto"""
        if hasattr(self, 'db'):
            self.db.close()


# Função helper para uso fácil
def provision_tenant_from_payment(
    company_name: str,
    contact_name: str,
    contact_email: str,
    contact_phone: str,
    plan: str,
    amount: float,
    gateway_data: dict = None,
    lead_id: int = None
) -> dict:
    """
    Função helper para provisionar tenant após pagamento aprovado
    """
    service = TenantProvisioningService()
    
    return service.provision_complete_tenant(
        company_name=company_name,
        contact_name=contact_name,
        contact_email=contact_email,
        contact_phone=contact_phone,
        plan=plan,
        amount=amount,
        gateway=gateway_data.get("gateway", "mercadopago") if gateway_data else "mercadopago",
        gateway_subscription_id=gateway_data.get("subscription_id") if gateway_data else None,
        gateway_customer_id=gateway_data.get("customer_id") if gateway_data else None,
        lead_id=lead_id
    )
