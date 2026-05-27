from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class Room:
    id: int
    name: str


@dataclass(frozen=True, slots=True, kw_only=True)
class Student:
    birthday: datetime
    id: int
    name: str
    room: int
    sex: str
