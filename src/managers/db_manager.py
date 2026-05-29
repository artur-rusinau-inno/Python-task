from typing import Iterable, Literal

from src.adapters import PostgresAdapter
from src.config.settings import settings


class DBManager:
    def __init__(self, db_type: Literal["postgres"], *, test: bool = False) -> None:
        self.db_type = db_type
        self.db = None
        self.test = test

    async def init(self) -> None:
        if self.db_type == "postgres":
            self.db = PostgresAdapter(settings.test_pg_dsn if self.test else settings.pg_dsn)

        else:
            raise ValueError("UNSUPPORTED DB TYPE")

        await self.db.init()

    async def execute_query(self, query: str, *args) -> list[dict]:
        return await self.db.execute_query(query, *args)

    async def clear_data(self) -> None:
        await self.db.clear_data()

    async def upload_data(self, table_name: str, data: Iterable) -> None:
        for d in data:
            await self.db.load_batch(table_name, d)
