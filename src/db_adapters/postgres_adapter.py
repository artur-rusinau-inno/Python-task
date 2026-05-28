from datetime import datetime

import asyncpg
from asyncpg import Connection, Pool, Record
from asyncpg.prepared_stmt import PreparedStatement


class PostgresAdapter:
    def __init__(self, db_dsn: str) -> None:
        self.pool: Pool | None = None
        self.db_dsn = db_dsn

    async def init(self) -> None:
        await self._connect()
        await self.clear_data()
        await self.pool.execute("CREATE TABLE IF NOT EXISTS rooms (id INT PRIMARY KEY, name VARCHAR(255))")
        await self.pool.execute(
            "CREATE TABLE IF NOT EXISTS students (birthday TIMESTAMP, id INT PRIMARY KEY, name VARCHAR(255), room INT REFERENCES rooms(id), sex VARCHAR(1))"
        )

    async def clear_data(self) -> None:
        await self.pool.execute("DROP TABLE IF EXISTS students")
        await self.pool.execute("DROP TABLE IF EXISTS rooms")

    async def execute_query(self, query: str, *args) -> list[dict]:
        async with self.pool.acquire() as con:
            con: Connection
            prepared_query: PreparedStatement = await con.prepare(query)

            if prepared_query.get_attributes():
                results: list[Record] = await prepared_query.fetch(*args)
                return [dict(result) for result in results]

            else:
                await con.execute(query, *args)
                return []

    async def load_batch(self, table_name: str, data: list[dict]) -> None:

        columns = tuple(data[0].keys())

        if "birthday" in columns:
            for d in data:
                d["birthday"] = datetime.fromisoformat(d["birthday"])

        records = [tuple(d.values()) for d in data]

        await self.pool.copy_records_to_table(table_name, columns=columns, records=records)

    async def _connect(self) -> None:
        self.pool = await asyncpg.create_pool(self.db_dsn)
