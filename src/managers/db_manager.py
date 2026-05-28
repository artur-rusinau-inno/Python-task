from db_adapters.postgres_adapter import PostgresAdapter
from src.config.settings import settings


class DBManager:
    def __init__(self, db_type: str):
        self.db_type = db_type
        self.db = None

    async def init_db(self) -> None:
        if self.db_type == "postgres":
            self.db = PostgresAdapter(settings.pg_dsn)

        else:
            ...

        await self.db.init_db()

    async def clear_data(self) -> None:
        await self.db.clear_data()
