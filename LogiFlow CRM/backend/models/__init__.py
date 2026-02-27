"""
LogiFlow CRM - Models Package
=============================
Central export point for all SQLAlchemy models
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models_main import (
    generate_uuid,
    StatusEntrega, StatusPedido, StatusMotorista, StatusVeiculo, StatusCotacao,
    StatusLead, StatusTenant, PlanType, SubscriptionStatus, PaymentGateway,
    NPSCategory, SurveyStatus, ChurnRiskLevel, SalesStage, InteractionType,
    User, RefreshToken,
    Cliente, Motorista, Veiculo, Pedido, Entrega, Cotacao, Ocorrencia,
    Lead, Tenant, Subscription,
    NPSSurvey, CSATSurvey, ChurnAlert, CustomerSuccessAction,
    GPSPosition, Opportunity, OpportunityStageHistory, CustomerInteraction,
    TenantIntegration, GPSRoute
)

from models.cte import CTe, StatusCTe
from models.mdfe import MDFe, StatusMDFe
from models.configuracao_fiscal import ConfiguracaoFiscal
from models.tenant_credentials import TenantCredentials
from models.whatsapp_message import WhatsAppMessage, WhatsAppConversation, WhatsAppConfig

__all__ = [
    "generate_uuid",
    "StatusEntrega", "StatusPedido", "StatusMotorista", "StatusVeiculo", "StatusCotacao",
    "StatusLead", "StatusTenant", "PlanType", "SubscriptionStatus", "PaymentGateway",
    "NPSCategory", "SurveyStatus", "ChurnRiskLevel", "SalesStage", "InteractionType",
    "User", "RefreshToken",
    "Cliente", "Motorista", "Veiculo", "Pedido", "Entrega", "Cotacao", "Ocorrencia",
    "Lead", "Tenant", "Subscription",
    "NPSSurvey", "CSATSurvey", "ChurnAlert", "CustomerSuccessAction",
    "GPSPosition", "Opportunity", "OpportunityStageHistory", "CustomerInteraction",
    "TenantIntegration", "GPSRoute",
    "CTe", "StatusCTe",
    "MDFe", "StatusMDFe",
    "ConfiguracaoFiscal",
    "TenantCredentials",
    "WhatsAppMessage", "WhatsAppConversation", "WhatsAppConfig",
]
