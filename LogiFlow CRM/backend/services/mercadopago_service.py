"""
LogiFlow CRM - Mercado Pago Integration Service
================================================
Serviço de integração com Mercado Pago para billing e pagamentos
"""

import mercadopago
from typing import Dict, Optional
from datetime import datetime, timedelta
from loguru import logger


class MercadoPagoService:
    """Serviço de integração com Mercado Pago"""
    
    def __init__(self, access_token: str):
        """
        Inicializa o cliente Mercado Pago
        
        Args:
            access_token: Token de acesso da aplicação
        """
        self.sdk = mercadopago.SDK(access_token)
        self.access_token = access_token
        logger.info("MercadoPago Service inicializado")
    
    
    # ========================================
    # Clientes (Customers)
    # ========================================
    
    def create_customer(
        self,
        email: str,
        first_name: str,
        last_name: str,
        phone: Optional[str] = None,
        identification_type: str = "CPF",
        identification_number: Optional[str] = None
    ) -> Dict:
        """
        Cria um cliente no Mercado Pago
        
        Args:
            email: Email do cliente
            first_name: Nome
            last_name: Sobrenome
            phone: Telefone
            identification_type: Tipo de documento (CPF, CNPJ)
            identification_number: Número do documento
        
        Returns:
            Dict com dados do cliente criado
        """
        try:
            customer_data = {
                "email": email,
                "first_name": first_name,
                "last_name": last_name
            }
            
            if phone:
                customer_data["phone"] = {
                    "area_code": phone[:2] if len(phone) >= 10 else "",
                    "number": phone[2:] if len(phone) >= 10 else phone
                }
            
            if identification_number:
                customer_data["identification"] = {
                    "type": identification_type,
                    "number": identification_number
                }
            
            response = self.sdk.customer().create(customer_data)
            
            if response["status"] == 201:
                logger.info(f"Cliente criado no MP: {response['response']['id']}")
                return {
                    "success": True,
                    "customer_id": response["response"]["id"],
                    "data": response["response"]
                }
            else:
                logger.error(f"Erro ao criar cliente: {response}")
                return {
                    "success": False,
                    "error": response.get("response", {}).get("message", "Erro desconhecido")
                }
        
        except Exception as e:
            logger.error(f"Exceção ao criar cliente: {e}")
            return {"success": False, "error": str(e)}
    
    
    def get_customer(self, customer_id: str) -> Dict:
        """Obtém dados de um cliente"""
        try:
            response = self.sdk.customer().get(customer_id)
            
            if response["status"] == 200:
                return {
                    "success": True,
                    "data": response["response"]
                }
            else:
                return {
                    "success": False,
                    "error": response.get("response", {}).get("message", "Cliente não encontrado")
                }
        
        except Exception as e:
            logger.error(f"Erro ao buscar cliente: {e}")
            return {"success": False, "error": str(e)}
    
    
    # ========================================
    # Assinaturas (Subscriptions)
    # ========================================
    
    def create_subscription_plan(
        self,
        reason: str,
        auto_recurring: Dict,
        back_url: str
    ) -> Dict:
        """
        Cria um plano de assinatura
        
        Args:
            reason: Descrição do plano (ex: "Plano Professional LogiFlow")
            auto_recurring: Configuração de recorrência
            back_url: URL de retorno após pagamento
        
        Example auto_recurring:
            {
                "frequency": 1,
                "frequency_type": "months",
                "transaction_amount": 599.00,
                "currency_id": "BRL"
            }
        """
        try:
            plan_data = {
                "reason": reason,
                "auto_recurring": auto_recurring,
                "back_url": back_url,
                "payment_methods_allowed": {
                    "payment_types": [
                        {"id": "credit_card"},
                        {"id": "debit_card"},
                        {"id": "ticket"}
                    ],
                    "payment_methods": []
                }
            }
            
            response = self.sdk.plan().create(plan_data)
            
            if response["status"] == 201:
                logger.info(f"Plano criado: {response['response']['id']}")
                return {
                    "success": True,
                    "plan_id": response["response"]["id"],
                    "init_point": response["response"]["init_point"],
                    "data": response["response"]
                }
            else:
                logger.error(f"Erro ao criar plano: {response}")
                return {
                    "success": False,
                    "error": response.get("response", {}).get("message", "Erro ao criar plano")
                }
        
        except Exception as e:
            logger.error(f"Exceção ao criar plano: {e}")
            return {"success": False, "error": str(e)}
    
    
    def create_subscription(
        self,
        preapproval_plan_id: str,
        payer_email: str,
        card_token_id: Optional[str] = None,
        back_url: Optional[str] = None
    ) -> Dict:
        """
        Cria uma assinatura para um cliente
        
        Args:
            preapproval_plan_id: ID do plano de assinatura
            payer_email: Email do pagador
            card_token_id: Token do cartão (opcional)
            back_url: URL de retorno
        """
        try:
            subscription_data = {
                "preapproval_plan_id": preapproval_plan_id,
                "payer_email": payer_email,
                "status": "authorized"
            }
            
            if card_token_id:
                subscription_data["card_token_id"] = card_token_id
            
            if back_url:
                subscription_data["back_url"] = back_url
            
            response = self.sdk.preapproval().create(subscription_data)
            
            if response["status"] == 201:
                logger.info(f"Assinatura criada: {response['response']['id']}")
                return {
                    "success": True,
                    "subscription_id": response["response"]["id"],
                    "init_point": response["response"].get("init_point"),
                    "data": response["response"]
                }
            else:
                logger.error(f"Erro ao criar assinatura: {response}")
                return {
                    "success": False,
                    "error": response.get("response", {}).get("message", "Erro ao criar assinatura")
                }
        
        except Exception as e:
            logger.error(f"Exceção ao criar assinatura: {e}")
            return {"success": False, "error": str(e)}
    
    
    def get_subscription(self, subscription_id: str) -> Dict:
        """Obtém dados de uma assinatura"""
        try:
            response = self.sdk.preapproval().get(subscription_id)
            
            if response["status"] == 200:
                return {
                    "success": True,
                    "data": response["response"]
                }
            else:
                return {
                    "success": False,
                    "error": "Assinatura não encontrada"
                }
        
        except Exception as e:
            logger.error(f"Erro ao buscar assinatura: {e}")
            return {"success": False, "error": str(e)}
    
    
    def cancel_subscription(self, subscription_id: str) -> Dict:
        """Cancela uma assinatura"""
        try:
            response = self.sdk.preapproval().update(
                subscription_id,
                {"status": "cancelled"}
            )
            
            if response["status"] == 200:
                logger.info(f"Assinatura cancelada: {subscription_id}")
                return {
                    "success": True,
                    "message": "Assinatura cancelada com sucesso"
                }
            else:
                return {
                    "success": False,
                    "error": "Erro ao cancelar assinatura"
                }
        
        except Exception as e:
            logger.error(f"Erro ao cancelar assinatura: {e}")
            return {"success": False, "error": str(e)}
    
    
    # ========================================
    # Pagamentos Únicos (Payments)
    # ========================================
    
    def create_payment(
        self,
        transaction_amount: float,
        description: str,
        payment_method_id: str,
        payer_email: str,
        token: Optional[str] = None,
        installments: int = 1,
        external_reference: Optional[str] = None
    ) -> Dict:
        """
        Cria um pagamento único
        
        Args:
            transaction_amount: Valor da transação
            description: Descrição do pagamento
            payment_method_id: Método de pagamento (ex: "pix", "visa", "master")
            payer_email: Email do pagador
            token: Token do cartão (para cartão de crédito)
            installments: Número de parcelas
            external_reference: Referência externa (ex: ID do pedido)
        """
        try:
            payment_data = {
                "transaction_amount": transaction_amount,
                "description": description,
                "payment_method_id": payment_method_id,
                "payer": {
                    "email": payer_email
                },
                "installments": installments
            }
            
            if token:
                payment_data["token"] = token
            
            if external_reference:
                payment_data["external_reference"] = external_reference
            
            response = self.sdk.payment().create(payment_data)
            
            if response["status"] == 201:
                logger.info(f"Pagamento criado: {response['response']['id']}")
                return {
                    "success": True,
                    "payment_id": response["response"]["id"],
                    "status": response["response"]["status"],
                    "status_detail": response["response"]["status_detail"],
                    "data": response["response"]
                }
            else:
                logger.error(f"Erro ao criar pagamento: {response}")
                return {
                    "success": False,
                    "error": response.get("response", {}).get("message", "Erro ao processar pagamento")
                }
        
        except Exception as e:
            logger.error(f"Exceção ao criar pagamento: {e}")
            return {"success": False, "error": str(e)}
    
    
    def create_pix_payment(
        self,
        transaction_amount: float,
        description: str,
        payer_email: str,
        payer_first_name: str,
        payer_last_name: str,
        payer_identification_type: str,
        payer_identification_number: str,
        external_reference: Optional[str] = None
    ) -> Dict:
        """
        Cria um pagamento PIX
        
        Returns:
            Dict com QR Code e dados do pagamento
        """
        try:
            payment_data = {
                "transaction_amount": transaction_amount,
                "description": description,
                "payment_method_id": "pix",
                "payer": {
                    "email": payer_email,
                    "first_name": payer_first_name,
                    "last_name": payer_last_name,
                    "identification": {
                        "type": payer_identification_type,
                        "number": payer_identification_number
                    }
                }
            }
            
            if external_reference:
                payment_data["external_reference"] = external_reference
            
            response = self.sdk.payment().create(payment_data)
            
            if response["status"] == 201:
                payment = response["response"]
                logger.info(f"Pagamento PIX criado: {payment['id']}")
                
                return {
                    "success": True,
                    "payment_id": payment["id"],
                    "status": payment["status"],
                    "qr_code": payment["point_of_interaction"]["transaction_data"]["qr_code"],
                    "qr_code_base64": payment["point_of_interaction"]["transaction_data"]["qr_code_base64"],
                    "ticket_url": payment["point_of_interaction"]["transaction_data"]["ticket_url"],
                    "data": payment
                }
            else:
                logger.error(f"Erro ao criar pagamento PIX: {response}")
                return {
                    "success": False,
                    "error": response.get("response", {}).get("message", "Erro ao gerar PIX")
                }
        
        except Exception as e:
            logger.error(f"Exceção ao criar pagamento PIX: {e}")
            return {"success": False, "error": str(e)}
    
    
    def get_payment(self, payment_id: str) -> Dict:
        """Obtém dados de um pagamento"""
        try:
            response = self.sdk.payment().get(payment_id)
            
            if response["status"] == 200:
                return {
                    "success": True,
                    "data": response["response"]
                }
            else:
                return {
                    "success": False,
                    "error": "Pagamento não encontrado"
                }
        
        except Exception as e:
            logger.error(f"Erro ao buscar pagamento: {e}")
            return {"success": False, "error": str(e)}
    
    
    # ========================================
    # Webhooks
    # ========================================
    
    def process_webhook(self, webhook_data: Dict) -> Dict:
        """
        Processa webhook do Mercado Pago
        
        Args:
            webhook_data: Dados recebidos do webhook
        
        Returns:
            Dict com informações processadas
        """
        try:
            action = webhook_data.get("action")
            data_id = webhook_data.get("data", {}).get("id")
            
            logger.info(f"Webhook recebido - Action: {action}, ID: {data_id}")
            
            if action == "payment.created":
                # Pagamento criado
                payment = self.get_payment(data_id)
                return {
                    "type": "payment",
                    "action": "created",
                    "payment": payment
                }
            
            elif action == "payment.updated":
                # Pagamento atualizado (aprovado, rejeitado, etc)
                payment = self.get_payment(data_id)
                return {
                    "type": "payment",
                    "action": "updated",
                    "payment": payment
                }
            
            elif action == "subscription.created":
                # Assinatura criada
                subscription = self.get_subscription(data_id)
                return {
                    "type": "subscription",
                    "action": "created",
                    "subscription": subscription
                }
            
            elif action == "subscription.updated":
                # Assinatura atualizada (cancelada, pausada, etc)
                subscription = self.get_subscription(data_id)
                return {
                    "type": "subscription",
                    "action": "updated",
                    "subscription": subscription
                }
            
            else:
                logger.warning(f"Ação de webhook não reconhecida: {action}")
                return {
                    "type": "unknown",
                    "action": action,
                    "data_id": data_id
                }
        
        except Exception as e:
            logger.error(f"Erro ao processar webhook: {e}")
            return {"success": False, "error": str(e)}


# ========================================
# Planos Pré-configurados LogiFlow
# ========================================

LOGIFLOW_PLANS = {
    "starter": {
        "name": "Plano Starter",
        "description": "LogiFlow CRM - Plano Starter (até 5 usuários)",
        "amount": 299.00,
        "max_users": 5,
        "max_vehicles": 10,
        "max_orders_per_month": 500,
        "features": [
            "Até 5 usuários",
            "Até 10 veículos",
            "500 pedidos/mês",
            "Gestão de pedidos",
            "App do motorista",
            "Suporte por email"
        ]
    },
    "professional": {
        "name": "Plano Professional",
        "description": "LogiFlow CRM - Plano Professional (até 15 usuários)",
        "amount": 599.00,
        "max_users": 15,
        "max_vehicles": 30,
        "max_orders_per_month": -1,  # ilimitado
        "features": [
            "Até 15 usuários",
            "Até 30 veículos",
            "Pedidos ilimitados",
            "Todas as funcionalidades",
            "Emissão de CT-e/MDF-e",
            "Rastreamento GPS",
            "WhatsApp integrado",
            "Suporte prioritário"
        ]
    },
    "enterprise": {
        "name": "Plano Enterprise",
        "description": "LogiFlow CRM - Plano Enterprise (usuários ilimitados)",
        "amount": 1499.00,
        "max_users": -1,  # ilimitado
        "max_vehicles": -1,  # ilimitado
        "max_orders_per_month": -1,  # ilimitado
        "features": [
            "Usuários ilimitados",
            "Veículos ilimitados",
            "Pedidos ilimitados",
            "Todas as funcionalidades",
            "API personalizada",
            "Integrações customizadas",
            "Gerente de conta dedicado",
            "Suporte 24/7 prioritário",
            "Treinamento presencial"
        ]
    }
}


def get_plan_config(plan_name: str) -> Dict:
    """Retorna configuração de um plano"""
    return LOGIFLOW_PLANS.get(plan_name.lower(), LOGIFLOW_PLANS["starter"])
