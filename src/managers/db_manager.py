from typing import Iterable, Literal

from src.config.settings import settings
from src.db_adapters.postgres_adapter import PostgresAdapter


class DBManager:
    def __init__(self, db_type: Literal["postgres"]):
        self.db_type = db_type
        self.db = None

    async def init(self) -> None:
        if self.db_type == "postgres":
            self.db = PostgresAdapter(settings.pg_dsn)

        else:
            raise ValueError("UNSUPPORTED DB TYPE")

        await self.db.init()

    async def execute_query(self, query: str, *args):
        return await self.db.execute_query(query, *args)

    async def clear_data(self) -> None:
        await self.db.clear_data()

    async def upload_data(self, table_name: str, data: Iterable) -> None:
        for d in data:
            await self.db.load_batch(table_name, d)
