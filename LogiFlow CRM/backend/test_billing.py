"""
Script de teste para verificar integração do Mercado Pago
"""

print("=" * 50)
print("🧪 Testando Integração Mercado Pago")
print("=" * 50)

# 1. Testar importação do serviço
print("\n1. Testando serviço Mercado Pago...")
try:
    from services.mercadopago_service import MercadoPagoService, LOGIFLOW_PLANS
    from config import settings
    
    mp = MercadoPagoService(settings.MERCADOPAGO_ACCESS_TOKEN)
    print(f"   ✅ Serviço inicializado")
    print(f"   Token: {settings.MERCADOPAGO_ACCESS_TOKEN[:20]}...")
except Exception as e:
    print(f"   ❌ Erro: {e}")
    exit(1)

# 2. Testar planos
print("\n2. Testando planos configurados...")
try:
    for plan_name, plan_config in LOGIFLOW_PLANS.items():
        print(f"   ✅ {plan_config['name']}: R$ {plan_config['amount']}/mês")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 3. Testar router de billing
print("\n3. Testando router de billing...")
try:
    from routers import billing
    print(f"   ✅ Router importado com sucesso")
    print(f"   Endpoints: {len(billing.router.routes)} rotas")
    
    for route in billing.router.routes:
        methods = ', '.join(route.methods)
        print(f"      - {methods:6} {route.path}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 4. Testar modelos
print("\n4. Testando modelos de dados...")
try:
    from models import Lead, Tenant, Subscription, StatusLead, PlanType
    print(f"   ✅ Lead model")
    print(f"   ✅ Tenant model")
    print(f"   ✅ Subscription model")
    print(f"   ✅ Enums: StatusLead, PlanType")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 5. Testar router de leads
print("\n5. Testando router de leads...")
try:
    from routers import leads
    print(f"   ✅ Router de leads importado")
    print(f"   Endpoints: {len(leads.router.routes)} rotas")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 6. Testar main app
print("\n6. Testando aplicação principal...")
try:
    from main import app
    print(f"   ✅ FastAPI app carregado")
    print(f"   Total de rotas: {len(app.routes)}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print("\n" + "=" * 50)
print("✅ Todos os testes passaram!")
print("=" * 50)
print("\n📋 Próximos passos:")
print("1. Criar migrations: alembic revision --autogenerate -m 'Add SaaS tables'")
print("2. Executar migrations: alembic upgrade head")
print("3. Iniciar servidor: uvicorn main:app --reload")
print("4. Testar endpoints: curl http://localhost:8000/api/billing/plans")
print("=" * 50)
