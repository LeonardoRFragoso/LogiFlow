from logging.config import fileConfig
import sys
import os

from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool
from sqlalchemy.orm import declarative_base

from alembic import context

# Adicionar o diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Criar Base local para evitar dependência circular com config.py
Base = declarative_base()

# Importar modelos (eles registram na Base ao serem importados)
try:
    from models import (
        Cliente, Motorista, Veiculo, Pedido, Entrega, 
        Cotacao, Ocorrencia, Lead, Tenant, Subscription
    )
except ImportError as e:
    print(f"Aviso: Não foi possível importar models: {e}")

# Importar novos modelos da camada de infraestrutura (Clean Architecture)
try:
    from infrastructure.persistence.models import (
        ClienteModel, CotacaoModel, PedidoModel
    )
except ImportError:
    pass  # Modelos v2 opcionais durante migração

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Configurar URL do banco de dados a partir de variáveis de ambiente
def get_database_url():
    """Constrói URL do banco a partir de variáveis de ambiente"""
    from urllib.parse import quote_plus
    
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return db_url
    
    # Construir URL PostgreSQL a partir de variáveis separadas
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", os.getenv("POSTGRES_DB", "logiflow"))
    user = os.getenv("DB_USER", os.getenv("POSTGRES_USER", "logiflow"))
    password = os.getenv("DB_PASSWORD", os.getenv("POSTGRES_PASSWORD", "logiflow123"))
    
    # URL encode password para evitar problemas com caracteres especiais
    password_encoded = quote_plus(password)
    
    return f"postgresql://{user}:{password_encoded}@{host}:{port}/{name}"

db_url = get_database_url()
print(f"Conectando ao banco: postgresql://***@{db_url.split('@')[1] if '@' in db_url else db_url}")
config.set_main_option("sqlalchemy.url", db_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
