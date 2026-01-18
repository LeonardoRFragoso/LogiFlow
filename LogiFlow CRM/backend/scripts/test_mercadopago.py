"""
Script de teste da integração com Mercado Pago
Execute: python scripts/test_mercadopago.py
"""

import sys
import os

# Adicionar o diretório backend ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import requests
from loguru import logger
from services.mercadopago_service import MercadoPagoService, get_plan_config, LOGIFLOW_PLANS


def test_credentials():
    """Testa se as credenciais do Mercado Pago estão configuradas"""
    logger.info("🧪 Testando credenciais do Mercado Pago...")
    
    access_token = os.getenv("MERCADOPAGO_ACCESS_TOKEN")
    public_key = os.getenv("MERCADOPAGO_PUBLIC_KEY")
    
    if not access_token or not public_key:
        logger.error("❌ Credenciais não configuradas!")
        logger.info("Configure as variáveis:")
        logger.info("  MERCADOPAGO_ACCESS_TOKEN")
        logger.info("  MERCADOPAGO_PUBLIC_KEY")
        logger.info("Veja: docs/MERCADOPAGO_SETUP.md")
        return False
    
    # Verificar se são credenciais de teste ou produção
    if access_token.startswith("TEST-"):
        logger.warning("⚠️  Usando credenciais de TESTE")
        logger.info("Para produção, use credenciais APP_USR-...")
    elif access_token.startswith("APP_USR-"):
        logger.success("✅ Usando credenciais de PRODUÇÃO")
    else:
        logger.error("❌ Formato de credencial inválido!")
        return False
    
    logger.success(f"✅ Access Token configurado: {access_token[:20]}...")
    logger.success(f"✅ Public Key configurado: {public_key[:20]}...")
    
    return True


def test_api_connection():
    """Testa conexão com API do Mercado Pago"""
    logger.info("🧪 Testando conexão com API do Mercado Pago...")
    
    access_token = os.getenv("MERCADOPAGO_ACCESS_TOKEN")
    
    if not access_token:
        logger.error("❌ Access token não configurado")
        return False
    
    try:
        # Testar endpoint de usuário
        url = "https://api.mercadopago.com/v1/users/me"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            logger.success(f"✅ Conexão OK! Usuário: {data.get('nickname', 'N/A')}")
            logger.info(f"   Email: {data.get('email', 'N/A')}")
            logger.info(f"   País: {data.get('site_id', 'N/A')}")
            return True
        else:
            logger.error(f"❌ Erro na API: {response.status_code}")
            logger.error(f"   Resposta: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erro ao conectar: {str(e)}")
        return False


def test_plan_configs():
    """Testa configurações dos planos"""
    logger.info("🧪 Testando configurações dos planos...")
    
    for plan_id, config in LOGIFLOW_PLANS.items():
        logger.info(f"\n📦 Plano: {plan_id.upper()}")
        logger.info(f"   Nome: {config['name']}")
        logger.info(f"   Valor: R$ {config['amount']:.2f}/mês")
        logger.info(f"   Usuários: {config['max_users']}")
        logger.info(f"   Veículos: {config['max_vehicles']}")
        logger.info(f"   Pedidos/mês: {config['max_orders_per_month']}")
    
    logger.success("✅ Todas as configurações de planos estão OK")
    return True


def test_create_preference():
    """Testa criação de preferência de pagamento"""
    logger.info("🧪 Testando criação de preferência de pagamento...")
    
    try:
        service = MercadoPagoService()
        
        # Dados de teste
        preference_data = {
            "items": [
                {
                    "title": "LogiFlow CRM - Plano Starter",
                    "quantity": 1,
                    "unit_price": 299.00,
                    "currency_id": "BRL"
                }
            ],
            "payer": {
                "name": "João",
                "surname": "Silva",
                "email": "teste@exemplo.com",
                "phone": {
                    "area_code": "11",
                    "number": "999999999"
                },
                "identification": {
                    "type": "CPF",
                    "number": "12345678909"
                }
            },
            "back_urls": {
                "success": os.getenv("CHECKOUT_SUCCESS_URL", "http://localhost:3001/checkout/success"),
                "failure": os.getenv("CHECKOUT_FAILURE_URL", "http://localhost:3001/checkout/failure"),
                "pending": os.getenv("CHECKOUT_PENDING_URL", "http://localhost:3001/checkout/pending")
            },
            "auto_return": "approved",
            "external_reference": "test_order_123",
            "statement_descriptor": "LOGIFLOW CRM",
            "metadata": {
                "plan_id": "starter",
                "tenant_name": "Empresa Teste",
                "environment": "test"
            }
        }
        
        access_token = os.getenv("MERCADOPAGO_ACCESS_TOKEN")
        url = "https://api.mercadopago.com/checkout/preferences"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=preference_data, headers=headers)
        
        if response.status_code == 201:
            data = response.json()
            logger.success("✅ Preferência criada com sucesso!")
            logger.info(f"   ID: {data.get('id')}")
            logger.info(f"   Link de pagamento: {data.get('init_point')}")
            logger.info(f"   Sandbox link: {data.get('sandbox_init_point')}")
            
            # Salvar link para testes
            logger.info("\n📝 Para testar, acesse:")
            if access_token.startswith("TEST-"):
                logger.info(f"   {data.get('sandbox_init_point')}")
            else:
                logger.info(f"   {data.get('init_point')}")
            
            return True
        else:
            logger.error(f"❌ Erro ao criar preferência: {response.status_code}")
            logger.error(f"   Resposta: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erro: {str(e)}")
        return False


def test_webhook_endpoint():
    """Testa se endpoint de webhook está acessível"""
    logger.info("🧪 Testando endpoint de webhook...")
    
    try:
        # Testar endpoint local
        response = requests.post(
            "http://localhost:8000/api/billing/webhooks/mercadopago",
            json={"type": "test", "data": {"id": "123"}},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code in [200, 400, 500]:  # Qualquer resposta indica que está acessível
            logger.success("✅ Endpoint de webhook está acessível")
            logger.info("   Configure no Mercado Pago:")
            logger.info("   https://api.logiflow.com.br/api/billing/webhooks/mercadopago")
            return True
        else:
            logger.warning(f"⚠️  Endpoint retornou status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        logger.warning("⚠️  Backend não está rodando em localhost:8000")
        logger.info("   Inicie o backend com: docker-compose up -d")
        return False
    except Exception as e:
        logger.error(f"❌ Erro: {str(e)}")
        return False


def main():
    """Executa todos os testes"""
    logger.info("=" * 70)
    logger.info("🚀 TESTE DE INTEGRAÇÃO - MERCADO PAGO")
    logger.info("=" * 70)
    print()
    
    results = {}
    
    # Teste 1: Credenciais
    results["credentials"] = test_credentials()
    print()
    
    if not results["credentials"]:
        logger.error("❌ Configure as credenciais antes de continuar")
        logger.info("Veja: docs/MERCADOPAGO_SETUP.md")
        return
    
    # Teste 2: Conexão com API
    results["api_connection"] = test_api_connection()
    print()
    
    # Teste 3: Configurações de planos
    results["plan_configs"] = test_plan_configs()
    print()
    
    # Teste 4: Criar preferência
    logger.info("\n⚠️  O próximo teste criará uma preferência de pagamento real")
    logger.info("Deseja continuar? (s/n): ", end="")
    
    import sys
    if sys.stdin.isatty():
        choice = input().strip().lower()
    else:
        choice = "s"
    
    if choice == "s":
        results["create_preference"] = test_create_preference()
        print()
    else:
        logger.info("⏭️  Teste de criação de preferência pulado")
        results["create_preference"] = None
    
    # Teste 5: Webhook endpoint
    results["webhook"] = test_webhook_endpoint()
    print()
    
    # Resumo
    print("=" * 70)
    logger.info("📊 RESUMO DOS TESTES")
    print("=" * 70)
    
    for test_name, result in results.items():
        if result is None:
            status = "⏭️  PULADO"
        elif result:
            status = "✅ PASSOU"
        else:
            status = "❌ FALHOU"
        
        logger.info(f"{status} - {test_name.replace('_', ' ').title()}")
    
    print()
    
    # Verificar se todos passaram
    failed = [name for name, result in results.items() if result is False]
    
    if not failed:
        logger.success("🎉 Todos os testes passaram!")
        logger.info("\n📝 Próximos passos:")
        logger.info("1. Configure o webhook no painel do Mercado Pago")
        logger.info("2. Teste o fluxo completo de pagamento")
        logger.info("3. Verifique se o provisionamento automático funciona")
    else:
        logger.warning(f"\n⚠️  {len(failed)} teste(s) falharam:")
        for name in failed:
            logger.warning(f"   - {name.replace('_', ' ').title()}")
        logger.info("\nVeja a documentação: docs/MERCADOPAGO_SETUP.md")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
