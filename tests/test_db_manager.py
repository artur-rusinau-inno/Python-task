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
def db():
    return DBManager(db_dict)


def test_init(db: DBManager):
    inited = db.init_db()
    assert inited is True
