"""
LogiFlow CRM - Billing Router
==============================
Gerenciamento de pagamentos e assinaturas via Mercado Pago
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
from datetime import datetime, timedelta
import os

from database import get_db
from models import Tenant, Subscription, Lead, StatusLead, SubscriptionStatus, PaymentGateway
from services.mercadopago_service import MercadoPagoService, get_plan_config
from services.tenant_provisioning import provision_tenant_from_payment
from services.email_service import send_welcome_email, send_payment_confirmation
from loguru import logger
from fastapi import BackgroundTasks

router = APIRouter(prefix="/api/billing", tags=["billing"])

# Inicializar serviço Mercado Pago
MP_ACCESS_TOKEN = os.getenv("MERCADOPAGO_ACCESS_TOKEN", "")
mp_service = MercadoPagoService(MP_ACCESS_TOKEN) if MP_ACCESS_TOKEN else None


# ========================================
# Schemas
# ========================================

class CheckoutRequest(BaseModel):
    lead_id: int
    plan: str  # starter, professional, enterprise
    payment_method: str  # credit_card, pix, boleto
    card_token: Optional[str] = None  # Token do cartão (se credit_card)


class SubscriptionCreate(BaseModel):
    tenant_id: int
    plan: str
    payment_method: str
    card_token: Optional[str] = None


class WebhookPayload(BaseModel):
    action: str
    data: Dict


# ========================================
# Endpoints - Checkout
# ========================================

@router.post("/checkout")
async def create_checkout(
    checkout: CheckoutRequest,
    db: Session = Depends(get_db)
):
    """
    Criar checkout para novo cliente (lead → trial → pago)
    """
    if not mp_service:
        raise HTTPException(500, "Mercado Pago não configurado")
    
    # Buscar lead
    lead = db.query(Lead).filter(Lead.id == checkout.lead_id).first()
    if not lead:
        raise HTTPException(404, "Lead não encontrado")
    
    # Verificar se já tem tenant
    if lead.tenant_id:
        raise HTTPException(400, "Lead já convertido em cliente")
    
    # Obter configuração do plano
    plan_config = get_plan_config(checkout.plan)
    
    # Criar cliente no Mercado Pago
    name_parts = lead.name.split(" ", 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ""
    
    mp_customer = mp_service.create_customer(
        email=lead.email,
        first_name=first_name,
        last_name=last_name,
        phone=lead.phone
    )
    
    if not mp_customer["success"]:
        raise HTTPException(400, f"Erro ao criar cliente: {mp_customer['error']}")
    
    # Criar plano de assinatura no MP
    mp_plan = mp_service.create_subscription_plan(
        reason=plan_config["description"],
        auto_recurring={
            "frequency": 1,
            "frequency_type": "months",
            "transaction_amount": plan_config["amount"],
            "currency_id": "BRL"
        },
        back_url=f"https://app.logiflow.com.br/checkout/success"
    )
    
    if not mp_plan["success"]:
        raise HTTPException(400, f"Erro ao criar plano: {mp_plan['error']}")
    
    # Criar assinatura
    mp_subscription = mp_service.create_subscription(
        preapproval_plan_id=mp_plan["plan_id"],
        payer_email=lead.email,
        card_token_id=checkout.card_token,
        back_url=f"https://app.logiflow.com.br/checkout/success"
    )
    
    if not mp_subscription["success"]:
        raise HTTPException(400, f"Erro ao criar assinatura: {mp_subscription['error']}")
    
    return {
        "success": True,
        "message": "Checkout criado com sucesso",
        "init_point": mp_subscription["init_point"],
        "subscription_id": mp_subscription["subscription_id"],
        "plan": plan_config
    }


@router.post("/checkout/pix")
async def create_pix_checkout(
    checkout: CheckoutRequest,
    db: Session = Depends(get_db)
):
    """
    Criar pagamento PIX para primeira mensalidade
    """
    if not mp_service:
        raise HTTPException(500, "Mercado Pago não configurado")
    
    # Buscar lead
    lead = db.query(Lead).filter(Lead.id == checkout.lead_id).first()
    if not lead:
        raise HTTPException(404, "Lead não encontrado")
    
    # Obter configuração do plano
    plan_config = get_plan_config(checkout.plan)
    
    # Criar pagamento PIX
    name_parts = lead.name.split(" ", 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ""
    
    pix_payment = mp_service.create_pix_payment(
        transaction_amount=plan_config["amount"],
        description=f"{plan_config['name']} - Primeira mensalidade",
        payer_email=lead.email,
        payer_first_name=first_name,
        payer_last_name=last_name,
        payer_identification_type="CPF",
        payer_identification_number="00000000000",  # TODO: Coletar CPF/CNPJ
        external_reference=f"lead_{lead.id}"
    )
    
    if not pix_payment["success"]:
        raise HTTPException(400, f"Erro ao gerar PIX: {pix_payment['error']}")
    
    return {
        "success": True,
        "payment_id": pix_payment["payment_id"],
        "qr_code": pix_payment["qr_code"],
        "qr_code_base64": pix_payment["qr_code_base64"],
        "ticket_url": pix_payment["ticket_url"],
        "amount": plan_config["amount"],
        "plan": plan_config
    }


# ========================================
# Endpoints - Assinaturas
# ========================================

@router.get("/subscriptions/{tenant_id}")
async def get_tenant_subscription(
    tenant_id: int,
    db: Session = Depends(get_db)
):
    """Obter assinatura ativa de um tenant"""
    subscription = db.query(Subscription).filter(
        Subscription.tenant_id == tenant_id,
        Subscription.status.in_(["active", "trial"])
    ).first()
    
    if not subscription:
        raise HTTPException(404, "Assinatura não encontrada")
    
    return {
        "success": True,
        "subscription": {
            "id": subscription.id,
            "plan": subscription.plan,
            "status": subscription.status,
            "amount": subscription.amount,
            "current_period_end": subscription.current_period_end.isoformat(),
            "trial_ends_at": subscription.trial_ends_at.isoformat() if subscription.trial_ends_at else None
        }
    }


@router.post("/subscriptions/{subscription_id}/cancel")
async def cancel_subscription(
    subscription_id: int,
    db: Session = Depends(get_db)
):
    """Cancelar assinatura"""
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(404, "Assinatura não encontrada")
    
    # Cancelar no Mercado Pago
    if mp_service and subscription.gateway_subscription_id:
        mp_result = mp_service.cancel_subscription(subscription.gateway_subscription_id)
        if not mp_result["success"]:
            raise HTTPException(400, f"Erro ao cancelar no MP: {mp_result['error']}")
    
    # Atualizar no banco
    subscription.status = SubscriptionStatus.CANCELLED.value
    subscription.cancelled_at = datetime.utcnow()
    
    # Atualizar tenant
    tenant = db.query(Tenant).filter(Tenant.id == subscription.tenant_id).first()
    if tenant:
        tenant.status = "cancelled"
        tenant.cancelled_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "success": True,
        "message": "Assinatura cancelada com sucesso"
    }


@router.post("/subscriptions/{subscription_id}/upgrade")
async def upgrade_subscription(
    subscription_id: int,
    new_plan: str,
    db: Session = Depends(get_db)
):
    """Fazer upgrade de plano"""
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(404, "Assinatura não encontrada")
    
    # Obter configuração do novo plano
    plan_config = get_plan_config(new_plan)
    
    # Atualizar assinatura
    subscription.plan = new_plan
    subscription.amount = plan_config["amount"]
    subscription.updated_at = datetime.utcnow()
    
    # Atualizar tenant com todos os limites
    tenant = db.query(Tenant).filter(Tenant.id == subscription.tenant_id).first()
    if tenant:
        tenant.plan = new_plan
        tenant.max_users = plan_config["max_users"]
        tenant.max_vehicles = plan_config["max_vehicles"]
        tenant.max_orders_per_month = plan_config["max_orders_per_month"]
        tenant.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "success": True,
        "message": f"Plano atualizado para {plan_config['name']}",
        "new_amount": plan_config["amount"]
    }


# ========================================
# Webhooks
# ========================================

async def process_approved_payment(payment_data: dict, db: Session):
    """
    Processa pagamento aprovado em background
    
    Fluxo:
    1. Buscar lead pelo external_reference
    2. Criar subscription no DB
    3. Provisionar tenant
    4. Gerar credenciais
    5. Enviar emails (confirmação + credenciais)
    """
    try:
        logger.info(f"💳 Processando pagamento aprovado: {payment_data.get('id')}")
        
        external_ref = payment_data.get("external_reference", "")
        metadata = payment_data.get("metadata", {})
        plan_id = metadata.get("plan", "starter")
        
        # Buscar lead
        if external_ref.startswith("lead_"):
            lead_id = int(external_ref.split("_")[1])
            lead = db.query(Lead).filter(Lead.id == lead_id).first()
            
            if not lead:
                logger.error(f"❌ Lead {lead_id} não encontrado")
                return
            
            if lead.tenant_id:
                logger.warning(f"⚠️  Lead {lead_id} já tem tenant associado: {lead.tenant_id}")
                return
            
            logger.info(f"📋 Lead encontrado: {lead.name} ({lead.email})")
            
            # Criar subscription
            plan_config = get_plan_config(plan_id)
            
            subscription = Subscription(
                gateway=PaymentGateway.MERCADOPAGO.value,
                gateway_subscription_id=payment_data.get("id"),
                gateway_customer_id=payment_data.get("payer", {}).get("id"),
                plan=plan_id,
                amount=payment_data["transaction_amount"],
                status=SubscriptionStatus.ACTIVE.value,
                current_period_start=datetime.utcnow(),
                current_period_end=datetime.utcnow() + timedelta(days=30),
                created_at=datetime.utcnow()
            )
            
            db.add(subscription)
            db.commit()
            db.refresh(subscription)
            
            logger.success(f"✅ Subscription criada: ID {subscription.id}")
            
            # Provisionar tenant
            logger.info("🚀 Iniciando provisionamento de tenant...")
            
            tenant = await provision_tenant_from_payment(
                company_name=lead.company or lead.name,
                contact_name=lead.name,
                contact_email=lead.email,
                contact_phone=lead.phone or "",
                plan=plan_id,
                amount=payment_data["transaction_amount"],
                gateway_data={
                    "gateway": "mercadopago",
                    "customer_id": payment_data.get("payer", {}).get("id"),
                    "subscription_id": payment_data.get("id"),
                    "payment_id": payment_data.get("id")
                },
                lead_id=lead_id
            )
            
            if not tenant:
                logger.error("❌ Falha ao provisionar tenant")
                subscription.status = SubscriptionStatus.INCOMPLETE.value
                db.commit()
                return
            
            logger.success(f"✅ Tenant provisionado: {tenant.subdomain}")
            
            # Atualizar subscription e lead
            subscription.tenant_id = tenant.id
            lead.tenant_id = tenant.id
            lead.status = StatusLead.CONVERTIDO.value
            db.commit()
            
            # Gerar senha temporária para admin
            import secrets
            import string
            temp_password = ''.join(
                secrets.choice(string.ascii_letters + string.digits + "!@#$%") 
                for _ in range(12)
            )
            
            admin_email = lead.email
            
            # Enviar email de confirmação de pagamento
            try:
                send_payment_confirmation(
                    contact_name=lead.name,
                    contact_email=lead.email,
                    plan=plan_config["name"],
                    amount=payment_data["transaction_amount"],
                    payment_method=payment_data.get("payment_method_id", "N/A")
                )
                logger.success("✅ Email de confirmação de pagamento enviado")
            except Exception as e:
                logger.error(f"❌ Erro ao enviar confirmação de pagamento: {str(e)}")
            
            # Enviar email de boas-vindas com credenciais
            try:
                send_welcome_email(
                    tenant_id=tenant.id,
                    company_name=tenant.company_name,
                    contact_name=lead.name,
                    contact_email=lead.email,
                    subdomain=tenant.subdomain,
                    plan=plan_id,
                    admin_email=admin_email,
                    admin_password=temp_password
                )
                logger.success("✅ Email de boas-vindas com credenciais enviado")
            except Exception as e:
                logger.error(f"❌ Erro ao enviar email de boas-vindas: {str(e)}")
            
            logger.success(f"🎉 Provisionamento completo para {lead.email}!")
            
    except Exception as e:
        logger.error(f"❌ Erro ao processar pagamento aprovado: {str(e)}")
        logger.exception(e)
        
        # Marcar para retry
        # TODO: Implementar sistema de retry


@router.post("/webhooks/mercadopago")
async def mercadopago_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Webhook do Mercado Pago para notificações de pagamento
    
    Eventos processados:
    - payment.created / payment.updated → Provisionar tenant se aprovado
    - subscription.updated → Atualizar status
    """
    if not mp_service:
        logger.warning("⚠️  Mercado Pago não configurado")
        raise HTTPException(500, "Mercado Pago não configurado")
    
    try:
        webhook_data = await request.json()
        logger.info(f"📩 Webhook recebido do Mercado Pago: {webhook_data.get('type')}")
        
        # Processar webhook
        result = mp_service.process_webhook(webhook_data)
        
        if result.get("type") == "payment":
            # Processar pagamento
            payment_data = result.get("payment", {}).get("data", {})
            payment_status = payment_data.get("status")
            
            logger.info(f"💳 Pagamento {payment_data.get('id')}: {payment_status}")
            
            if payment_status == "approved":
                # Processar em background para não bloquear webhook
                background_tasks.add_task(
                    process_approved_payment,
                    payment_data,
                    db
                )
                logger.info("✅ Pagamento aprovado - processamento agendado")
                
            elif payment_status == "rejected":
                logger.warning(f"❌ Pagamento rejeitado: {payment_data.get('id')}")
                # TODO: Notificar usuário sobre falha
                
            elif payment_status == "pending":
                logger.info(f"⏳ Pagamento pendente: {payment_data.get('id')}")
                # TODO: Notificar usuário sobre pendência
        
        elif result.get("type") == "subscription":
            # Processar assinatura
            subscription_data = result.get("subscription", {}).get("data", {})
            
            logger.info(f"📋 Atualização de assinatura: {subscription_data.get('id')}")
            
            # Atualizar status no banco
            db_subscription = db.query(Subscription).filter(
                Subscription.gateway_subscription_id == subscription_data["id"]
            ).first()
            
            if db_subscription:
                old_status = db_subscription.status
                new_status = subscription_data.get("status")
                
                db_subscription.status = new_status
                db_subscription.updated_at = datetime.utcnow()
                db.commit()
                
                logger.info(f"✅ Subscription {db_subscription.id}: {old_status} → {new_status}")
                
                # Se foi cancelada, desativar tenant
                if new_status == "cancelled":
                    tenant = db.query(Tenant).filter(Tenant.id == db_subscription.tenant_id).first()
                    if tenant:
                        tenant.status = "cancelled"
                        tenant.cancelled_at = datetime.utcnow()
                        db.commit()
                        logger.warning(f"⚠️  Tenant {tenant.id} desativado por cancelamento")
        
        return {"success": True, "message": "Webhook processado"}
    
    except Exception as e:
        logger.error(f"❌ Erro ao processar webhook: {str(e)}")
        logger.exception(e)
        # Retornar 200 para evitar retry do MP em erros que não são transientes
        return {"success": False, "error": str(e)}


# ========================================
# Planos Disponíveis
# ========================================

@router.get("/plans")
async def get_available_plans():
    """Listar planos disponíveis"""
    from services.mercadopago_service import LOGIFLOW_PLANS
    
    return {
        "success": True,
        "plans": LOGIFLOW_PLANS
    }


@router.get("/plans/{plan_name}")
async def get_plan_details(plan_name: str):
    """Obter detalhes de um plano específico"""
    plan_config = get_plan_config(plan_name)
    
    return {
        "success": True,
        "plan": plan_config
    }
