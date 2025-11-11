"""
Alembic environment configuration.
"""
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.task_planner.models.base import Base
from src.task_planner.models.a2rp.base import A2RPBase
from src.task_planner.config import settings

# Import all old application models (if still needed)
from src.task_planner.models import (
    Team,
    Person,
    Resource,
    Task,
    Assignment,
    Schedule,
    ScheduleException,
)

# Import all a2rp schema models
from src.task_planner.models.a2rp import (
    # Lookups
    ProjectStatus,
    ProjectType,
    TaskStatus,
    ResourceStatus,
    ResourceType,
    ProcessingOrderStatus,
    ProcessingOrderType,
    CostType,
    Job,
    NtAccount,
    Property,
    # Organizational
    CostCenter,
    CostItem,
    Customer,
    Imputation,
    OrganizationalUnit,
    TechnicalFeature,
    WorkBreakdownStructure,
    ResourceBreakdownStructure,
    # Core
    Project,
    Task as A2RPTask,
    Resource as A2RPResource,
    Assignment as A2RPAssignment,
    AssignmentByMonth,
    # Supporting
    ProcessingOrder,
    HistoricalProjectSummary,
    HistoricalProjectSummaryResource,
    ProjectToPlan,
    ProjectToPlanOrganizationalUnit,
    TaskToPlan,
    TaskToPlanOrganizationalUnit,
)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Override sqlalchemy.url with the one from settings
config.set_main_option("sqlalchemy.url", settings.database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# Combine metadata from both Base classes to track all tables
from sqlalchemy import MetaData

combined_metadata = MetaData()

# Merge tables from both bases
for table in Base.metadata.tables.values():
    table.to_metadata(combined_metadata)

for table in A2RPBase.metadata.tables.values():
    table.to_metadata(combined_metadata)

target_metadata = combined_metadata

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
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
