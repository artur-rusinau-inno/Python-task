import asyncpg


class PostgresAdapter:
    def __init__(self, db_dsn: str) -> None:
        self.connection: asyncpg.Connection | None = None
        self.db_dsn = db_dsn

    async def init_db(self) -> None:
        await self._connect()
        await self.execute(
            "CREATE TABLE IF NOT EXISTS rooms (id INT PRIMARY KEY, name VARCHAR(255))"
        )
        await self.execute(
            "CREATE TABLE IF NOT EXISTS students (birthday TIMESTAMP, id INT PRIMARY KEY, name VARCHAR(255), room INT REFERENCES rooms(id), sex VARCHAR(1))"
        )

    async def clear_data(self) -> None:
        await self.execute("DROP TABLE IF EXISTS students")
        await self.execute("DROP TABLE IF EXISTS rooms")

    async def fetch(self, query: str, *args) -> list[asyncpg.Record]:
        return await self.connection.fetch(query, *args)

    async def execute(self, query: str, *args) -> None:
        await self.connection.execute(query, *args)

    async def copy_to_db(self, batch_size=50_000): ...

    async def _connect(self) -> None:
        self.connection = await asyncpg.connect(self.db_dsn)
