import pytest

from managers.db_manager import DBManager


@pytest.fixture
async def db():
    db = DBManager("postgres", test=True)
    await db.init()
    return db


async def test_db_connection(db: DBManager):
    result = await db.execute_query("SELECT 1")
    assert result
