"""Add strategic indices for performance optimization

Revision ID: 009_add_strategic_indices
Revises: 008_add_tenant_id_standalone
Create Date: 2026-02-27 14:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '009_add_strategic_indices'
down_revision = '008_add_tenant_id_standalone'
branch_labels = None
depends_on = None


def upgrade():
    """
    Cria índices estratégicos para melhorar performance de queries
    
    Estratégia:
    1. Multi-tenancy: índice em tenant_id para isolamento rápido
    2. Status: índice em campos de status (created_at, updated_at)
    3. Filtros comuns: email, cpf, cnpj, placa
    4. Relationships: foreign keys para quick joins
    5. Composite indices: combinações frequentes em WHERE clauses
    """
    
    # ===============================================
    # USERS - Índices por tenant, email, status
    # ===============================================
    op.execute("CREATE INDEX IF NOT EXISTS idx_users_tenant_id ON users(tenant_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_users_email_tenant ON users(email, tenant_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_users_tenant_status ON users(tenant_id, status)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at DESC)")
    
    # ===============================================
    # TENANTS - Índices por status e plano
    # ===============================================
    op.execute("CREATE INDEX IF NOT EXISTS idx_tenants_status ON tenants(status)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_tenants_plan ON tenants(plan)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_tenants_subdomain ON tenants(subdomain)")
    
    # ===============================================
    # CLIENTES - Índices por tenant, status, cidade
    # ===============================================
    op.execute("CREATE INDEX IF NOT EXISTS idx_clientes_tenant_id ON clientes(tenant_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_clientes_tenant_status ON clientes(tenant_id, status) WHERE status IS NOT NULL")
    op.execute("CREATE INDEX IF NOT EXISTS idx_clientes_email ON clientes(email)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_clientes_cnpj ON clientes(cnpj)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_clientes_created_at ON clientes(tenant_id, created_at DESC)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_clientes_cidade_tenant ON clientes(tenant_id, cidade)")
    
    # ===============================================
    # MOTORISTAS - Índices por tenant, status, tipo
    # ===============================================
    op.execute("CREATE INDEX IF NOT EXISTS idx_motoristas_tenant_id ON motoristas(tenant_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_motoristas_tenant_status ON motoristas(tenant_id, status)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_motoristas_cpf ON motoristas(cpf)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_motoristas_disponibilidade ON motoristas(tenant_id, disponibilidade)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_motoristas_created_at ON motoristas(tenant_id, created_at DESC)")
    
    # ===============================================
    # VEICULOS - Índices por tenant, status, placa
    # ===============================================
    op.execute("CREATE INDEX IF NOT EXISTS idx_veiculos_tenant_id ON veiculos(tenant_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_veiculos_placa ON veiculos(placa)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_veiculos_tenant_status ON veiculos(tenant_id, status)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_veiculos_created_at ON veiculos(tenant_id, created_at DESC)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_veiculos_motorista_id ON veiculos(motorista_id)")
    
    # ===============================================
    # COTACOES - Índices críticos de negócio
    # ===============================================
    op.execute("CREATE INDEX IF NOT EXISTS idx_cotacoes_tenant_id ON cotacoes(tenant_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_cotacoes_tenant_status ON cotacoes(tenant_id, status)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_cotacoes_cliente_tenant ON cotacoes(tenant_id, cliente_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_cotacoes_created_at ON cotacoes(tenant_id, created_at DESC)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_cotacoes_origem_destino ON cotacoes(tenant_id, origem, destino)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_cotacoes_data_validade ON cotacoes(data_validade) WHERE data_validade > CURRENT_TIMESTAMP")
    
    # ===============================================
    # PEDIDOS - Índices críticos de negócio
    # ===============================================
    op.execute("CREATE INDEX IF NOT EXISTS idx_pedidos_tenant_id ON pedidos(tenant_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_pedidos_tenant_status ON pedidos(tenant_id, status)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_pedidos_cliente_tenant ON pedidos(tenant_id, cliente_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_pedidos_motorista_tenant ON pedidos(tenant_id, motorista_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_pedidos_created_at ON pedidos(tenant_id, created_at DESC)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_pedidos_data_entrega ON pedidos(tenant_id, data_prevista_entrega)")
    
    # ===============================================
    # ENTREGA - Rastreamento em tempo real
    # ===============================================
    if check_table_exists('entrega'):
        op.execute("CREATE INDEX IF NOT EXISTS idx_entrega_tenant_id ON entrega(tenant_id)")
        op.execute("CREATE INDEX IF NOT EXISTS idx_entrega_pedido ON entrega(pedido_id)")
        op.execute("CREATE INDEX IF NOT EXISTS idx_entrega_status ON entrega(tenant_id, status)")
        op.execute("CREATE INDEX IF NOT EXISTS idx_entrega_motorista ON entrega(motorista_id)")
        op.execute("CREATE INDEX IF NOT EXISTS idx_entrega_data_atualizacao ON entrega(tenant_id, data_atualizacao DESC)")
    
    # ===============================================
    # GPS_TRACKING - Muitos registros, índices críticos
    # ===============================================
    if check_table_exists('gps_tracking'):
        op.execute("CREATE INDEX IF NOT EXISTS idx_gps_tracking_tenant ON gps_tracking(tenant_id)")
        op.execute("CREATE INDEX IF NOT EXISTS idx_gps_tracking_motorista ON gps_tracking(tenant_id, motorista_id)")
        op.execute("CREATE INDEX IF NOT EXISTS idx_gps_tracking_veiculo ON gps_tracking(veiculo_id)")
        op.execute("CREATE INDEX IF NOT EXISTS idx_gps_tracking_timestamp ON gps_tracking(tenant_id, timestamp DESC)")
        op.execute("CREATE INDEX IF NOT EXISTS idx_gps_tracking_timestamp_motorista ON gps_tracking(tenant_id, motorista_id, timestamp DESC)")
    
    # ===============================================
    # OCORRENCIAS - Suporte/Tickets
    # ===============================================
    if check_table_exists('ocorrencias'):
        op.execute("CREATE INDEX IF NOT EXISTS idx_ocorrencias_tenant ON ocorrencias(tenant_id)")
        op.execute("CREATE INDEX IF NOT EXISTS idx_ocorrencias_pedido ON ocorrencias(pedido_id)")
        op.execute("CREATE INDEX IF NOT EXISTS idx_ocorrencias_status ON ocorrencias(tenant_id, status)")
        op.execute("CREATE INDEX IF NOT EXISTS idx_ocorrencias_created_at ON ocorrencias(tenant_id, created_at DESC)")
    
    # ===============================================
    # LEADS - Prospecting
    # ===============================================
    if check_table_exists('leads'):
        op.execute("CREATE INDEX IF NOT EXISTS idx_leads_tenant ON leads(tenant_id)")
        op.execute("CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(tenant_id, status)")
        op.execute("CREATE INDEX IF NOT EXISTS idx_leads_created_at ON leads(tenant_id, created_at DESC)")
        op.execute("CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(email)")
    
    # ===============================================
    # BILLING - Transações financeiras
    # ===============================================
    if check_table_exists('billing'):
        op.execute("CREATE INDEX IF NOT EXISTS idx_billing_tenant ON billing(tenant_id)")
        op.execute("CREATE INDEX IF NOT EXISTS idx_billing_pedido ON billing(pedido_id)")
        op.execute("CREATE INDEX IF NOT EXISTS idx_billing_status ON billing(tenant_id, status)")
        op.execute("CREATE INDEX IF NOT EXISTS idx_billing_data ON billing(tenant_id, data_criacao DESC)")
    
    # ===============================================
    # FISCAL - Documentação fiscal
    # ===============================================
    if check_table_exists('fiscal'):
        op.execute("CREATE INDEX IF NOT EXISTS idx_fiscal_tenant ON fiscal(tenant_id)")
        op.execute("CREATE INDEX IF NOT EXISTS idx_fiscal_pedido ON fiscal(pedido_id)")
        op.execute("CREATE INDEX IF NOT EXISTS idx_fiscal_numero_nf ON fiscal(numero_nf)")
        op.execute("CREATE INDEX IF NOT EXISTS idx_fiscal_created_at ON fiscal(tenant_id, created_at DESC)")


def downgrade():
    """
    Remove todos os índices criados
    """
    # Índices de USERS
    op.execute("DROP INDEX IF EXISTS idx_users_tenant_id")
    op.execute("DROP INDEX IF EXISTS idx_users_email_tenant")
    op.execute("DROP INDEX IF EXISTS idx_users_tenant_status")
    op.execute("DROP INDEX IF EXISTS idx_users_created_at")
    
    # Índices de TENANTS
    op.execute("DROP INDEX IF EXISTS idx_tenants_status")
    op.execute("DROP INDEX IF EXISTS idx_tenants_plan")
    op.execute("DROP INDEX IF EXISTS idx_tenants_subdomain")
    
    # Índices de CLIENTES
    op.execute("DROP INDEX IF EXISTS idx_clientes_tenant_id")
    op.execute("DROP INDEX IF EXISTS idx_clientes_tenant_status")
    op.execute("DROP INDEX IF EXISTS idx_clientes_email")
    op.execute("DROP INDEX IF EXISTS idx_clientes_cnpj")
    op.execute("DROP INDEX IF EXISTS idx_clientes_created_at")
    op.execute("DROP INDEX IF EXISTS idx_clientes_cidade_tenant")
    
    # Índices de MOTORISTAS
    op.execute("DROP INDEX IF EXISTS idx_motoristas_tenant_id")
    op.execute("DROP INDEX IF EXISTS idx_motoristas_tenant_status")
    op.execute("DROP INDEX IF EXISTS idx_motoristas_cpf")
    op.execute("DROP INDEX IF EXISTS idx_motoristas_disponibilidade")
    op.execute("DROP INDEX IF EXISTS idx_motoristas_created_at")
    
    # Índices de VEICULOS
    op.execute("DROP INDEX IF EXISTS idx_veiculos_tenant_id")
    op.execute("DROP INDEX IF EXISTS idx_veiculos_placa")
    op.execute("DROP INDEX IF EXISTS idx_veiculos_tenant_status")
    op.execute("DROP INDEX IF EXISTS idx_veiculos_created_at")
    op.execute("DROP INDEX IF EXISTS idx_veiculos_motorista_id")
    
    # Índices de COTACOES
    op.execute("DROP INDEX IF EXISTS idx_cotacoes_tenant_id")
    op.execute("DROP INDEX IF EXISTS idx_cotacoes_tenant_status")
    op.execute("DROP INDEX IF EXISTS idx_cotacoes_cliente_tenant")
    op.execute("DROP INDEX IF EXISTS idx_cotacoes_created_at")
    op.execute("DROP INDEX IF EXISTS idx_cotacoes_origem_destino")
    op.execute("DROP INDEX IF EXISTS idx_cotacoes_data_validade")
    
    # Índices de PEDIDOS
    op.execute("DROP INDEX IF EXISTS idx_pedidos_tenant_id")
    op.execute("DROP INDEX IF EXISTS idx_pedidos_tenant_status")
    op.execute("DROP INDEX IF EXISTS idx_pedidos_cliente_tenant")
    op.execute("DROP INDEX IF EXISTS idx_pedidos_motorista_tenant")
    op.execute("DROP INDEX IF EXISTS idx_pedidos_created_at")
    op.execute("DROP INDEX IF EXISTS idx_pedidos_data_entrega")
    
    # Índices de ENTREGA
    op.execute("DROP INDEX IF EXISTS idx_entrega_tenant_id")
    op.execute("DROP INDEX IF EXISTS idx_entrega_pedido")
    op.execute("DROP INDEX IF EXISTS idx_entrega_status")
    op.execute("DROP INDEX IF EXISTS idx_entrega_motorista")
    op.execute("DROP INDEX IF EXISTS idx_entrega_data_atualizacao")
    
    # Índices de GPS_TRACKING
    op.execute("DROP INDEX IF EXISTS idx_gps_tracking_tenant")
    op.execute("DROP INDEX IF EXISTS idx_gps_tracking_motorista")
    op.execute("DROP INDEX IF EXISTS idx_gps_tracking_veiculo")
    op.execute("DROP INDEX IF EXISTS idx_gps_tracking_timestamp")
    op.execute("DROP INDEX IF EXISTS idx_gps_tracking_timestamp_motorista")
    
    # Índices de OCORRENCIAS
    op.execute("DROP INDEX IF EXISTS idx_ocorrencias_tenant")
    op.execute("DROP INDEX IF EXISTS idx_ocorrencias_pedido")
    op.execute("DROP INDEX IF EXISTS idx_ocorrencias_status")
    op.execute("DROP INDEX IF EXISTS idx_ocorrencias_created_at")
    
    # Índices de LEADS
    op.execute("DROP INDEX IF EXISTS idx_leads_tenant")
    op.execute("DROP INDEX IF EXISTS idx_leads_status")
    op.execute("DROP INDEX IF EXISTS idx_leads_created_at")
    op.execute("DROP INDEX IF EXISTS idx_leads_email")
    
    # Índices de BILLING
    op.execute("DROP INDEX IF EXISTS idx_billing_tenant")
    op.execute("DROP INDEX IF EXISTS idx_billing_pedido")
    op.execute("DROP INDEX IF EXISTS idx_billing_status")
    op.execute("DROP INDEX IF EXISTS idx_billing_data")
    
    # Índices de FISCAL
    op.execute("DROP INDEX IF EXISTS idx_fiscal_tenant")
    op.execute("DROP INDEX IF EXISTS idx_fiscal_pedido")
    op.execute("DROP INDEX IF EXISTS idx_fiscal_numero_nf")
    op.execute("DROP INDEX IF EXISTS idx_fiscal_created_at")


def check_table_exists(table_name: str) -> bool:
    """
    Verifica se uma tabela existe no banco
    """
    try:
        from sqlalchemy import inspect
        from database import engine
        inspector = inspect(engine)
        return table_name in inspector.get_table_names()
    except:
        return False
