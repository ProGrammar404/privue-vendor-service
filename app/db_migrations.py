import asyncio
import os
from alembic import command
from alembic.config import Config


async def run_migrations():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _upgrade)


def _upgrade():
    alembic_cfg = Config("alembic.ini")
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        alembic_cfg.set_main_option("sqlalchemy.url", db_url)
    command.upgrade(alembic_cfg, "head")
