"""
Script para testar se as tabelas foram criadas corretamente
"""

from sqlalchemy import inspect
from database import engine
from models import Lead, Tenant, Subscription

print("=" * 60)
print("🗄️  Testando Banco de Dados - LogiFlow CRM")
print("=" * 60)

# Inspecionar banco de dados
inspector = inspect(engine)
tables = inspector.get_table_names()

print(f"\n📊 Tabelas no banco de dados: {len(tables)}")
for table in sorted(tables):
    print(f"   ✅ {table}")
    
    # Mostrar colunas de cada tabela
    columns = inspector.get_columns(table)
    print(f"      Colunas: {len(columns)}")
    for col in columns[:5]:  # Mostrar apenas as 5 primeiras
        print(f"         - {col['name']}: {col['type']}")
    if len(columns) > 5:
        print(f"         ... e mais {len(columns) - 5} colunas")
    print()

# Verificar tabelas específicas
print("\n🎯 Verificando tabelas SaaS:")
required_tables = ['leads', 'tenants', 'subscriptions']
for table in required_tables:
    if table in tables:
        print(f"   ✅ {table} - OK")
    else:
        print(f"   ❌ {table} - FALTANDO")

print("\n" + "=" * 60)
print("✅ Teste concluído!")
print("=" * 60)
