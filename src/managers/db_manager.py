from typing import Iterable, Literal

from db_adapters.postgres_adapter import PostgresAdapter
from src.config.settings import settings


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

    async def upload_data(self, data: Iterable) -> None:
        batch = []
        for i in data:
            batch.append(i)
            if len(batch) >= settings.UPLOAD_BATCH_SIZE:
                await self.db.load_batch(batch)
                batch = []

        if batch:
            await self.db.load_batch(batch)
