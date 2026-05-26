import asyncpg

from src.config.settings import DB_CONNECTIONS_DICT


class DBManager:
    def __init__(self, db_dict: dict[str, str | int]) -> None:
        self.connection: asyncpg.Connection = None
        self.db_dict = db_dict

    async def db_connect(self) -> None:
        self.connection = await asyncpg.connect(**self.db_dict)
        print("PostgreSQL connected successfully")

    # async def insert_rooms(self, rooms: list[dict]) -> None:
    #     await self.connection.executemany(
    #         "INSERT INTO rooms (id, name) VALUES (%(id)s, %(name)s)", rooms
    #     )

    # async def insert_students(self, students: list[dict]) -> None:
    #     await self.connection.executemany(
    #         "INSERT INTO students (birthday, id, name, room, sex) VALUES (%(birthday)s, %(id)s, %(name)s, %(room)s, %(sex)s)",
    #         students,
    #     )

    async def insert_many_query(self, table_name: str, args: list[dict]):
        columns = ", ".join(args[0].keys())
        values_count = ", ".join([f"${i}" for i in range(1, len(args[0].values()) + 1)])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values_count})"
        await self.connection.executemany(query, [tuple(d.values()) for d in args])

    async def clear_data(self) -> None:
        self.connection.execute("DROP TABLE IF EXISTS students")
        self.connection.execute("DROP TABLE IF EXISTS rooms")

    async def init_db(self) -> None:
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS rooms (id INT PRIMARY KEY, name VARCHAR(255))"
        )
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS students (birthday DATE, id INT PRIMARY KEY, name VARCHAR(255), room INT REFERENCES rooms(id), sex VARCHAR(1))"
        )


db_manager = DBManager(DB_CONNECTIONS_DICT)
