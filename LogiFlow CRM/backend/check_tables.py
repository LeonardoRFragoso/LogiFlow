import sqlite3

conn = sqlite3.connect('logiflow.db')
cur = conn.cursor()

# Listar todas as tabelas
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cur.fetchall()

print("=== TABELAS NO BANCO ===")
for table in tables:
    print(f"  - {table[0]}")

# Verificar tabelas CRM Enterprise
crm_tables = [
    'opportunities',
    'opportunity_stage_history',
    'customer_interactions',
    'cliente_field_history',
    'lead_status_history',
    'opportunity_notes',
    'opportunity_products',
    'sales_activities',
    'sales_forecasts',
    'customer_health_score_log',
    'opportunity_sla_log',
    'cliente_segmentacao',
    'email_templates'
]

print("\n=== STATUS TABELAS CRM ENTERPRISE ===")
for table_name in crm_tables:
    cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    exists = cur.fetchone()
    status = "✅ EXISTE" if exists else "❌ NÃO EXISTE"
    print(f"{status}: {table_name}")

# Verificar colunas adicionadas em clientes
print("\n=== COLUNAS NOVAS EM CLIENTES ===")
cur.execute("PRAGMA table_info(clientes)")
columns = [col[1] for col in cur.fetchall()]

new_columns = [
    'cargo_contato', 'email_contato_secundario', 'telefone_contato_secundario',
    'segmento', 'porte', 'status_comercial', 'classificacao', 'health_score',
    'health_score_anterior', 'health_score_atualizado_em', 'responsavel_comercial_id',
    'responsavel_cs_id', 'data_primeira_compra', 'data_ultima_compra', 
    'data_ultimo_contato', 'valor_total_gasto', 'ticket_medio',
    'frequencia_compra_dias', 'sla_resposta_horas', 'prioridade_atendimento',
    'tags', 'observacoes_internas'
]

for col in new_columns:
    status = "✅ EXISTE" if col in columns else "❌ NÃO EXISTE"
    print(f"{status}: {col}")

conn.close()
