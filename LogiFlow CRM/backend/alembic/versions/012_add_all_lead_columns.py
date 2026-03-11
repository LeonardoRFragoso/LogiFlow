"""add all missing lead columns

Revision ID: 012_add_all_lead_columns
Revises: 011_add_lead_cargo_column
Create Date: 2026-03-11 17:21:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '012_add_all_lead_columns'
down_revision = '011_add_lead_cargo_column'
branch_labels = None
depends_on = None


def upgrade():
    """Add all missing columns to leads table"""
    
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_columns = [col['name'] for col in inspector.get_columns('leads')]
    
    # Lista de colunas a adicionar
    columns_to_add = {
        'cargo': ('VARCHAR(100)', None),
        'website': ('VARCHAR(255)', None),
        'linkedin': ('VARCHAR(255)', None),
        'necessidade_descrita': ('TEXT', None),
        'source_details': ('VARCHAR(255)', None),
        'lead_score': ('INTEGER', '0'),
        'estagio_maturidade': ('VARCHAR(50)', "'frio'"),
        'primeiro_contato_em': ('TIMESTAMP', None),
        'ultimo_contato_em': ('TIMESTAMP', None),
        'proximo_followup_em': ('TIMESTAMP', None),
        'converted_to_cliente_id': ('INTEGER', None),
        'motivo_descarte': ('TEXT', None),
    }
    
    # Adicionar cada coluna se não existir
    for column_name, (column_type, default_value) in columns_to_add.items():
        if column_name not in existing_columns:
            default_clause = f' DEFAULT {default_value}' if default_value else ''
            op.execute(f"""
                ALTER TABLE leads 
                ADD COLUMN {column_name} {column_type}{default_clause}
            """)
            print(f"✅ Coluna '{column_name}' adicionada à tabela 'leads'")
        else:
            print(f"ℹ️ Coluna '{column_name}' já existe na tabela 'leads'")
    
    # Criar índices para colunas importantes
    indices_to_create = [
        ('idx_leads_email', 'leads', 'email'),
        ('idx_leads_status', 'leads', 'status'),
        ('idx_leads_source', 'leads', 'source'),
        ('idx_leads_lead_score', 'leads', 'lead_score'),
        ('idx_leads_assigned_to', 'leads', 'assigned_to'),
        ('idx_leads_proximo_followup_em', 'leads', 'proximo_followup_em'),
        ('idx_leads_created_at', 'leads', 'created_at'),
    ]
    
    for index_name, table_name, column_name in indices_to_create:
        op.execute(f"""
            CREATE INDEX IF NOT EXISTS {index_name} ON {table_name}({column_name})
        """)
        print(f"✅ Índice '{index_name}' criado")
    
    # Adicionar foreign key para converted_to_cliente_id se a coluna clientes existir
    try:
        op.execute("""
            ALTER TABLE leads 
            ADD CONSTRAINT fk_leads_converted_to_cliente 
            FOREIGN KEY (converted_to_cliente_id) 
            REFERENCES clientes(id) 
            ON DELETE SET NULL
        """)
        print("✅ Foreign key 'fk_leads_converted_to_cliente' adicionada")
    except Exception as e:
        print(f"ℹ️ Foreign key já existe ou erro ao criar: {e}")
    
    # Adicionar foreign key para assigned_to se a coluna users existir
    try:
        op.execute("""
            ALTER TABLE leads 
            ADD CONSTRAINT fk_leads_assigned_to_user 
            FOREIGN KEY (assigned_to) 
            REFERENCES users(id) 
            ON DELETE SET NULL
        """)
        print("✅ Foreign key 'fk_leads_assigned_to_user' adicionada")
    except Exception as e:
        print(f"ℹ️ Foreign key já existe ou erro ao criar: {e}")


def downgrade():
    """Remove all added columns from leads table"""
    
    columns_to_remove = [
        'cargo', 'website', 'linkedin', 'necessidade_descrita',
        'source_details', 'lead_score', 'estagio_maturidade',
        'primeiro_contato_em', 'ultimo_contato_em', 'proximo_followup_em',
        'converted_to_cliente_id', 'motivo_descarte'
    ]
    
    # Remover foreign keys primeiro
    try:
        op.execute("ALTER TABLE leads DROP CONSTRAINT IF EXISTS fk_leads_converted_to_cliente")
        op.execute("ALTER TABLE leads DROP CONSTRAINT IF EXISTS fk_leads_assigned_to_user")
    except:
        pass
    
    # Remover colunas
    for column_name in columns_to_remove:
        try:
            op.drop_column('leads', column_name)
        except:
            pass
