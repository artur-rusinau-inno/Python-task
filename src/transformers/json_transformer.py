from datetime import datetime

from src.schemas.schemas import Room, Student


class JSONTransformer:
    @staticmethod
    def transform_rooms(data: list[dict]):
        return [Room(id=d["id"], name=d["name"]) for d in data]

    @staticmethod
    def transform_students(data: list[dict]):
        return [
            Student(
                birthday=datetime.fromisoformat(d["birthday"]),
                id=d["id"],
                name=d["name"],
                room=d["room"],
                sex=d["sex"],
            )
            for d in data
        ]
