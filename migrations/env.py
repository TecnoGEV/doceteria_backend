from logging.config import fileConfig
# from sqlalchemy import engine_from_config, pool
from alembic import context

# Importa a configuração e o Base do projeto
from config.database import Base, get_engine  # <-- ajusta o caminho se estiver diferente

# Carrega config do alembic.ini
config = context.config

# Configura log
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from src.models import *  # Importa todos os modelos para o Alembic reconhecer

# Usa o metadata dos models
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Executa migrações no modo offline."""
    url = config.get_main_option("sqlalchemy.url") or str(get_engine().url)

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Executa migrações no modo online (banco conectado)."""
    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
