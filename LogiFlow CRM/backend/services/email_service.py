"""
Serviço de Envio de Emails
Gerencia envio de emails transacionais (boas-vindas, notificações, etc)
"""

from loguru import logger
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
from typing import Optional


class EmailService:
    """Serviço para envio de emails"""
    
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@logiflow.com.br")
        self.from_name = os.getenv("FROM_NAME", "LogiFlow CRM")
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """
        Envia um email
        """
        try:
            # Criar mensagem
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            
            # Adicionar conteúdo texto plano (fallback)
            if text_content:
                part1 = MIMEText(text_content, 'plain', 'utf-8')
                msg.attach(part1)
            
            # Adicionar conteúdo HTML
            part2 = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(part2)
            
            # Enviar email
            if not self.smtp_user or not self.smtp_password:
                logger.warning("⚠️  SMTP não configurado - email não será enviado")
                logger.info(f"📧 [SIMULADO] Email para {to_email}: {subject}")
                return True
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.success(f"✅ Email enviado para {to_email}: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao enviar email para {to_email}: {e}")
            return False
    
    def send_welcome_email(
        self,
        tenant_id: int,
        company_name: str,
        contact_name: str,
        contact_email: str,
        subdomain: str,
        plan: str,
        admin_email: str,
        admin_password: str
    ) -> bool:
        """
        Envia email de boas-vindas após provisionamento
        """
        subject = f"🎉 Bem-vindo ao LogiFlow CRM, {contact_name}!"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #2563eb 0%, #06b6d4 100%); color: white; padding: 40px 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }}
                .box {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #2563eb; }}
                .credentials {{ background: #eff6ff; padding: 15px; border-radius: 8px; margin: 15px 0; }}
                .button {{ display: inline-block; background: linear-gradient(135deg, #2563eb 0%, #06b6d4 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; margin: 20px 0; }}
                .footer {{ text-align: center; color: #6b7280; font-size: 12px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb; }}
                .highlight {{ color: #2563eb; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 Sua conta está pronta!</h1>
                    <p>Bem-vindo ao LogiFlow CRM</p>
                </div>
                
                <div class="content">
                    <p>Olá <strong>{contact_name}</strong>,</p>
                    
                    <p>É com grande satisfação que damos as boas-vindas à <strong>{company_name}</strong> ao LogiFlow CRM!</p>
                    
                    <div class="box">
                        <h2>✅ Sua conta foi criada com sucesso!</h2>
                        <p>Seu ambiente foi provisionado e está pronto para uso. Você já pode começar a gerenciar sua operação logística.</p>
                    </div>
                    
                    <div class="box">
                        <h2>🔐 Dados de Acesso</h2>
                        <div class="credentials">
                            <p><strong>URL de Acesso:</strong><br>
                            <a href="https://{subdomain}.logiflow.com.br" class="highlight">https://{subdomain}.logiflow.com.br</a></p>
                            
                            <p><strong>Email:</strong> {admin_email}</p>
                            <p><strong>Senha temporária:</strong> {admin_password}</p>
                            
                            <p style="color: #dc2626; font-size: 14px;">
                                ⚠️ Por segurança, altere sua senha no primeiro acesso!
                            </p>
                        </div>
                    </div>
                    
                    <div class="box">
                        <h2>📦 Seu Plano: {plan.upper()}</h2>
                        <p>Você tem acesso a todos os recursos do plano <strong>{plan}</strong>.</p>
                        <ul>
                            <li>✅ Gestão completa de clientes</li>
                            <li>✅ Cotações e pedidos</li>
                            <li>✅ Rastreamento de entregas</li>
                            <li>✅ App do motorista</li>
                            <li>✅ Relatórios e dashboards</li>
                        </ul>
                    </div>
                    
                    <div class="box">
                        <h2>🎯 Próximos Passos</h2>
                        <ol>
                            <li><strong>Faça login</strong> com suas credenciais</li>
                            <li><strong>Altere sua senha</strong> para uma senha segura</li>
                            <li><strong>Configure sua empresa</strong> (dados, logo, etc)</li>
                            <li><strong>Cadastre seus usuários</strong> e defina permissões</li>
                            <li><strong>Importe seus dados</strong> ou comece do zero</li>
                        </ol>
                    </div>
                    
                    <div style="text-align: center;">
                        <a href="https://{subdomain}.logiflow.com.br" class="button">
                            🚀 Acessar Minha Conta
                        </a>
                    </div>
                    
                    <div class="box">
                        <h2>💬 Precisa de Ajuda?</h2>
                        <p>Nossa equipe está disponível 24/7 para ajudar você:</p>
                        <ul>
                            <li>📧 Email: <a href="mailto:suporte@logiflow.com.br">suporte@logiflow.com.br</a></li>
                            <li>💬 WhatsApp: <a href="https://wa.me/5511999999999">(11) 99999-9999</a></li>
                            <li>📚 Central de Ajuda: <a href="https://ajuda.logiflow.com.br">ajuda.logiflow.com.br</a></li>
                        </ul>
                    </div>
                    
                    <p>Estamos muito felizes em tê-lo conosco! 🎉</p>
                    
                    <p>Atenciosamente,<br>
                    <strong>Equipe LogiFlow CRM</strong></p>
                </div>
                
                <div class="footer">
                    <p>LogiFlow CRM - Gestão Inteligente de Frotas</p>
                    <p>Este é um email automático, por favor não responda.</p>
                    <p>© 2025 LogiFlow. Todos os direitos reservados.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Bem-vindo ao LogiFlow CRM!
        
        Olá {contact_name},
        
        Sua conta foi criada com sucesso!
        
        DADOS DE ACESSO:
        URL: https://{subdomain}.logiflow.com.br
        Email: {admin_email}
        Senha: {admin_password}
        
        IMPORTANTE: Altere sua senha no primeiro acesso!
        
        Plano: {plan.upper()}
        
        Precisa de ajuda?
        Email: suporte@logiflow.com.br
        WhatsApp: (11) 99999-9999
        
        Atenciosamente,
        Equipe LogiFlow CRM
        """
        
        return self.send_email(contact_email, subject, html_content, text_content)
    
    def send_payment_confirmation(
        self,
        contact_name: str,
        contact_email: str,
        plan: str,
        amount: float,
        payment_method: str
    ) -> bool:
        """
        Envia confirmação de pagamento
        """
        subject = f"✅ Pagamento Confirmado - LogiFlow CRM"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 40px 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }}
                .box {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; }}
                .footer {{ text-align: center; color: #6b7280; font-size: 12px; margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✅ Pagamento Confirmado!</h1>
                </div>
                
                <div class="content">
                    <p>Olá <strong>{contact_name}</strong>,</p>
                    
                    <p>Confirmamos o recebimento do seu pagamento!</p>
                    
                    <div class="box">
                        <h3>Detalhes do Pagamento</h3>
                        <p><strong>Plano:</strong> {plan}</p>
                        <p><strong>Valor:</strong> R$ {amount:.2f}</p>
                        <p><strong>Forma de Pagamento:</strong> {payment_method}</p>
                    </div>
                    
                    <p>Sua assinatura está ativa e você já pode usar todos os recursos do LogiFlow CRM!</p>
                    
                    <p>Atenciosamente,<br>
                    <strong>Equipe LogiFlow CRM</strong></p>
                </div>
                
                <div class="footer">
                    <p>© 2025 LogiFlow. Todos os direitos reservados.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(contact_email, subject, html_content)
    
    def send_demo_confirmation(
        self,
        name: str,
        email: str,
        company: str,
        vehicles: Optional[str] = None
    ) -> bool:
        """
        Envia email de confirmação após solicitação de demo
        """
        subject = "Recebemos sua solicitação de demonstração! 🚀"
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #2563eb 0%, #06b6d4 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center; }}
                .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; background: #2563eb; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                .box {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #2563eb; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 LogiFlow CRM</h1>
                <p>Gestão Logística Inteligente</p>
            </div>
            
            <div class="content">
                <h2>Olá, {name}! 👋</h2>
                
                <p>Recebemos sua solicitação de demonstração do LogiFlow para a <strong>{company}</strong>!</p>
                
                <p>Nossa equipe irá entrar em contato em até <strong>24 horas úteis</strong> para agendar sua demonstração personalizada.</p>
                
                <div class="box">
                    <h3>📋 Próximos Passos:</h3>
                    <ol>
                        <li>Aguarde nosso contato por email ou telefone</li>
                        <li>Prepare suas dúvidas sobre gestão logística</li>
                        <li>Tenha em mãos informações sobre sua operação atual</li>
                    </ol>
                </div>
                
                <div class="box">
                    <h3>⚡ Enquanto isso, que tal assinar agora?</h3>
                    <p>Se você já está convencido, pode começar a usar imediatamente:</p>
                    <center>
                        <a href="http://localhost:5173/#precos" class="button">Ver Planos e Assinar Agora</a>
                    </center>
                </div>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
                
                <div class="box">
                    <h3>❓ Dúvidas Frequentes:</h3>
                    <p><strong>Quanto tempo leva para implementar?</strong><br>
                    Apenas 48 horas! Nosso sistema é provisionado automaticamente.</p>
                    
                    <p><strong>Preciso de conhecimento técnico?</strong><br>
                    Não! A interface é super intuitiva e oferecemos treinamento completo.</p>
                    
                    <p><strong>Posso cancelar quando quiser?</strong><br>
                    Sim! Sem multas ou taxas de cancelamento.</p>
                </div>
            </div>
            
            <div class="footer">
                <p>LogiFlow - Transformando a logística brasileira<br>
                📧 contato@logiflow.com.br | 📱 (11) 99999-9999<br>
                🌐 <a href="http://localhost:5173">www.logiflow.com.br</a></p>
                
                <p style="font-size: 12px; color: #999; margin-top: 20px;">
                    Você recebeu este email porque solicitou uma demonstração em nosso site.
                </p>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Olá {name},
        
        Recebemos sua solicitação de demonstração do LogiFlow para a {company}!
        
        Nossa equipe irá entrar em contato em até 24 horas úteis para agendar sua demonstração personalizada.
        
        Próximos Passos:
        1. Aguarde nosso contato por email ou telefone
        2. Prepare suas dúvidas sobre gestão logística
        3. Tenha em mãos informações sobre sua operação atual
        
        Enquanto isso, que tal assinar agora?
        Se você já está convencido, pode começar a usar imediatamente:
        http://localhost:5173/#precos
        
        Atenciosamente,
        Equipe LogiFlow CRM
        
        contato@logiflow.com.br
        (11) 99999-9999
        """
        
        return self.send_email(email, subject, html_content, text_content)
    
    def send_lead_notification(
        self,
        lead_name: str,
        lead_email: str,
        lead_company: str,
        lead_phone: str
    ) -> bool:
        """
        Envia notificação para equipe de vendas sobre novo lead
        """
        sales_email = os.getenv("SALES_EMAIL", "vendas@logiflow.com.br")
        subject = f"🎯 Novo Lead: {lead_name} - {lead_company}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
        </head>
        <body>
            <h2>🎯 Novo Lead Capturado!</h2>
            
            <p><strong>Nome:</strong> {lead_name}</p>
            <p><strong>Email:</strong> {lead_email}</p>
            <p><strong>Empresa:</strong> {lead_company}</p>
            <p><strong>Telefone:</strong> {lead_phone}</p>
            
            <p>Acesse o CRM para mais detalhes e fazer o contato.</p>
        </body>
        </html>
        """
        
        return self.send_email(sales_email, subject, html_content)


# Instância global do serviço
email_service = EmailService()


# Funções helper
def send_welcome_email(**kwargs):
    """Helper para enviar email de boas-vindas"""
    return email_service.send_welcome_email(**kwargs)


def send_payment_confirmation(**kwargs):
    """Helper para enviar confirmação de pagamento"""
    return email_service.send_payment_confirmation(**kwargs)


def send_demo_confirmation(**kwargs):
    """Helper para enviar confirmação de demo"""
    return email_service.send_demo_confirmation(**kwargs)


def send_lead_notification(**kwargs):
    """Helper para notificar equipe sobre novo lead"""
    return email_service.send_lead_notification(**kwargs)
