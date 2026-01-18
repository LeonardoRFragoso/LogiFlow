"""
Script de teste manual do sistema de emails
Execute: python scripts/test_email.py
"""

import sys
import os

# Adicionar o diretório backend ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.email_service import email_service
from loguru import logger

def test_demo_confirmation():
    """Testa email de confirmação de demo"""
    logger.info("🧪 Testando email de confirmação de demo...")
    
    result = email_service.send_demo_confirmation(
        name="João Silva",
        email="teste@exemplo.com",  # MUDE PARA SEU EMAIL REAL PARA TESTAR
        company="Transportes Teste Ltda",
        vehicles="15"
    )
    
    if result:
        logger.success("✅ Email de confirmação enviado com sucesso!")
    else:
        logger.error("❌ Falha ao enviar email de confirmação")
    
    return result


def test_welcome_email():
    """Testa email de boas-vindas"""
    logger.info("🧪 Testando email de boas-vindas...")
    
    result = email_service.send_welcome_email(
        tenant_id=1,
        company_name="Transportes Exemplo SA",
        contact_name="Maria Santos",
        contact_email="teste@exemplo.com",  # MUDE PARA SEU EMAIL REAL
        subdomain="exemplo",
        plan="professional",
        admin_email="admin@exemplo.com",
        admin_password="Temp@123456"
    )
    
    if result:
        logger.success("✅ Email de boas-vindas enviado com sucesso!")
    else:
        logger.error("❌ Falha ao enviar email de boas-vindas")
    
    return result


def test_payment_confirmation():
    """Testa email de confirmação de pagamento"""
    logger.info("🧪 Testando email de confirmação de pagamento...")
    
    result = email_service.send_payment_confirmation(
        contact_name="Carlos Souza",
        contact_email="teste@exemplo.com",  # MUDE PARA SEU EMAIL REAL
        plan="Starter",
        amount=299.00,
        payment_method="PIX"
    )
    
    if result:
        logger.success("✅ Email de confirmação de pagamento enviado com sucesso!")
    else:
        logger.error("❌ Falha ao enviar email de confirmação de pagamento")
    
    return result


def test_lead_notification():
    """Testa notificação de novo lead"""
    logger.info("🧪 Testando notificação de novo lead...")
    
    result = email_service.send_lead_notification(
        lead_name="Ana Costa",
        lead_email="ana@exemplo.com",
        lead_company="Logística ABC",
        lead_phone="(11) 98888-7777"
    )
    
    if result:
        logger.success("✅ Notificação de lead enviada com sucesso!")
    else:
        logger.error("❌ Falha ao enviar notificação de lead")
    
    return result


def main():
    """Executa todos os testes"""
    logger.info("=" * 60)
    logger.info("🚀 TESTE DO SISTEMA DE EMAILS - LogiFlow CRM")
    logger.info("=" * 60)
    
    # Verificar se SMTP está configurado
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    if not smtp_user or not smtp_password:
        logger.warning("⚠️  SMTP não configurado - emails serão simulados")
        logger.info("Para enviar emails reais, configure as variáveis:")
        logger.info("  SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD")
        logger.info("  Veja: docs/EMAIL_SETUP.md")
        print()
    else:
        logger.success(f"✅ SMTP configurado: {smtp_user}")
        print()
    
    # Menu interativo
    while True:
        print("\n" + "=" * 60)
        print("ESCOLHA UM TESTE:")
        print("=" * 60)
        print("1. Email de Confirmação de Demo")
        print("2. Email de Boas-Vindas (Credenciais)")
        print("3. Email de Confirmação de Pagamento")
        print("4. Notificação de Novo Lead")
        print("5. Testar TODOS os emails")
        print("0. Sair")
        print("=" * 60)
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == "1":
            test_demo_confirmation()
        elif choice == "2":
            test_welcome_email()
        elif choice == "3":
            test_payment_confirmation()
        elif choice == "4":
            test_lead_notification()
        elif choice == "5":
            logger.info("\n🧪 Executando TODOS os testes...\n")
            results = [
                test_demo_confirmation(),
                test_welcome_email(),
                test_payment_confirmation(),
                test_lead_notification()
            ]
            
            print("\n" + "=" * 60)
            print("RESUMO DOS TESTES")
            print("=" * 60)
            success = sum(results)
            total = len(results)
            logger.info(f"✅ Testes bem-sucedidos: {success}/{total}")
            if success == total:
                logger.success("🎉 Todos os emails foram enviados com sucesso!")
            else:
                logger.warning(f"⚠️  {total - success} teste(s) falharam")
        elif choice == "0":
            logger.info("👋 Encerrando testes...")
            break
        else:
            logger.warning("❌ Opção inválida!")
    
    print("\n" + "=" * 60)
    logger.info("✅ Testes finalizados")
    print("=" * 60)


if __name__ == "__main__":
    main()
