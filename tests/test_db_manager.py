import pytest

from managers.db_manager import DBManager
from src.config.settings import settings


@pytest.fixture
async def db():
    db = DBManager(settings.test_pg_dsn)
    await db.db_connect()
    return db


async def test_db_connection(db: DBManager):
    result = await db.connection.fetchval("SELECT 1")
    assert result
