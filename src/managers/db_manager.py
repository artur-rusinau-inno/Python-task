import datetime

import asyncpg


class DBManager:
    def __init__(self, db_dsn: str) -> None:
        self.connection: asyncpg.Connection | None = None
        self.db_dsn = db_dsn

    async def fetch(self, query: str, *args) -> list[asyncpg.Record]:
        return await self.connection.fetch(query, *args)

    async def execute(self, query: str, *args) -> None:
        await self.connection.execute(query, *args)

    async def db_connect(self) -> None:
        self.connection = await asyncpg.connect(self.db_dsn)

    async def copy_to_db(
        self, table_name: str, fetched_data: list[dict], batch_size: int = 10_000
    ) -> None:
        columns = list(fetched_data[0].keys())

        if "birthday" in columns:
            for row in fetched_data:
                row["birthday"] = datetime.datetime.fromisoformat(row["birthday"])

        records = [tuple(row.values()) for row in fetched_data]

        await self.connection.copy_records_to_table(
            table_name,
            records=records,
            columns=columns,
        )

    async def clear_data(self) -> None:
        await self.execute("DROP TABLE IF EXISTS students")
        await self.execute("DROP TABLE IF EXISTS rooms")

    async def init_db(self) -> None:
        await self.execute(
            "CREATE TABLE IF NOT EXISTS rooms (id INT PRIMARY KEY, name VARCHAR(255))"
        )
        await self.execute(
            "CREATE TABLE IF NOT EXISTS students (birthday TIMESTAMP, id INT PRIMARY KEY, name VARCHAR(255), room INT REFERENCES rooms(id), sex VARCHAR(1))"
        )
