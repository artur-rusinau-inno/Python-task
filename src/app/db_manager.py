import asyncpg


class DBManager:
    def __init__(self, db_dict: dict[str, str | int]) -> None:
        self.connection: asyncpg.Connection | None = None
        self.db_dict = db_dict

    async def db_connect(self) -> None:
        self.connection = await asyncpg.connect(**self.db_dict)

    async def insert_many_query(self, table_name: str, args: list[dict]):
        columns = ", ".join(args[0].keys())
        values_count = ", ".join([f"${i}" for i in range(1, len(args[0].values()) + 1)])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values_count})"
        await self.connection.executemany(query, [tuple(d.values()) for d in args])

    async def clear_data(self) -> None:
        await self.connection.execute("DROP TABLE IF EXISTS students")
        await self.connection.execute("DROP TABLE IF EXISTS rooms")

    async def init_db(self) -> None:
        await self.connection.execute(
            "CREATE TABLE IF NOT EXISTS rooms (id INT PRIMARY KEY, name VARCHAR(255))"
        )
        await self.connection.execute(
            "CREATE TABLE IF NOT EXISTS students (birthday TIMESTAMP, id INT PRIMARY KEY, name VARCHAR(255), room INT REFERENCES rooms(id), sex VARCHAR(1))"
        )
