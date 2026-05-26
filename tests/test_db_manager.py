import pytest

from src.app.db_manager import DBManager

db_dict = {
    "database": "test",
    "user": "test",
    "password": "test",
    "host": "localhost",
    "port": 5433,
}


@pytest.fixture
async def db():
    db = DBManager(db_dict)
    await db.db_connect()
    return db


async def test_db_connection(db: DBManager):
    result = await db.connection.fetchval("SELECT 1")
    assert result
