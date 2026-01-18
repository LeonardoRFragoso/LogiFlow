"""
Testes para o serviço de emails
"""

import pytest
from services.email_service import EmailService, email_service
import os


class TestEmailService:
    """Testes do EmailService"""
    
    def test_email_service_initialization(self):
        """Testa inicialização do serviço"""
        service = EmailService()
        
        assert service.smtp_host is not None
        assert service.smtp_port is not None
        assert service.from_email is not None
        assert service.from_name is not None
    
    def test_send_email_without_credentials(self):
        """Testa envio de email sem credenciais (modo simulação)"""
        service = EmailService()
        
        # Forçar modo sem credenciais para testar simulação
        original_user = service.smtp_user
        original_password = service.smtp_password
        
        service.smtp_user = ""
        service.smtp_password = ""
        
        result = service.send_email(
            to_email="teste@exemplo.com",
            subject="Teste",
            html_content="<p>Teste</p>",
            text_content="Teste"
        )
        
        # Em modo simulação, deve retornar True
        assert result is True
        
        # Restaurar valores originais
        service.smtp_user = original_user
        service.smtp_password = original_password
    
    def test_send_demo_confirmation(self):
        """Testa envio de confirmação de demo"""
        result = email_service.send_demo_confirmation(
            name="João Silva",
            email="joao@exemplo.com",
            company="Transportes Teste Ltda",
            vehicles="15"
        )
        
        assert result is True
    
    def test_send_welcome_email(self):
        """Testa envio de email de boas-vindas"""
        result = email_service.send_welcome_email(
            tenant_id=1,
            company_name="Transportes Exemplo SA",
            contact_name="Maria Santos",
            contact_email="maria@exemplo.com",
            subdomain="exemplo",
            plan="professional",
            admin_email="admin@exemplo.com",
            admin_password="Temp@123456"
        )
        
        assert result is True
    
    def test_send_payment_confirmation(self):
        """Testa envio de confirmação de pagamento"""
        result = email_service.send_payment_confirmation(
            contact_name="Carlos Souza",
            contact_email="carlos@exemplo.com",
            plan="Starter",
            amount=299.00,
            payment_method="PIX"
        )
        
        assert result is True
    
    def test_send_lead_notification(self):
        """Testa envio de notificação de novo lead"""
        result = email_service.send_lead_notification(
            lead_name="Ana Costa",
            lead_email="ana@exemplo.com",
            lead_company="Logística ABC",
            lead_phone="(11) 98888-7777"
        )
        
        assert result is True
    
    def test_email_html_content_generation(self):
        """Testa se o conteúdo HTML é gerado corretamente"""
        service = EmailService()
        
        # Testar se métodos não geram exceção ao formatar HTML
        try:
            service.send_demo_confirmation(
                name="Teste",
                email="teste@exemplo.com",
                company="Empresa Teste",
                vehicles="10"
            )
            success = True
        except Exception:
            success = False
        
        assert success is True


@pytest.mark.skipif(
    not os.getenv("SMTP_USER") or not os.getenv("SMTP_PASSWORD"),
    reason="Credenciais SMTP não configuradas"
)
class TestEmailServiceWithSMTP:
    """Testes que requerem SMTP configurado"""
    
    def test_send_real_email(self):
        """Testa envio real de email (requer SMTP configurado)"""
        service = EmailService()
        
        # Enviar para email de teste
        result = service.send_email(
            to_email=os.getenv("TEST_EMAIL", "teste@exemplo.com"),
            subject="Teste LogiFlow CRM - Email Service",
            html_content="<h1>Teste</h1><p>Este é um email de teste do LogiFlow CRM</p>",
            text_content="Teste - Este é um email de teste do LogiFlow CRM"
        )
        
        assert result is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
