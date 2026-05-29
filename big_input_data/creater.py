from pathlib import Path
from random import choice, choices, randint
from string import ascii_letters

import orjson


def random_json(i):
    return {
        "birthday": f"{randint(1980, 2010)}-{randint(1, 12):02d}-{randint(1, 28):02d}T00:00:00.000000",
        "id": i,
        "name": "".join(choices(ascii_letters, k=15)),
        "room": randint(0, 999),
        "sex": choice(["M", "F"]),
    }


file_path = Path(__file__).parent / "big_students_file.json"

TOTAL_RECORDS = 1_000_000
# TOTAL_RECORDS = randint(10000, 20000)
CHUNK_SIZE = 1


def main():

    with file_path.open("wb") as f:
        f.write(b"[\n")  # Открываем массив

        first_chunk = True

        for i in range(0, TOTAL_RECORDS, CHUNK_SIZE):
            # Обработка "хвоста", если TOTAL не делится ровно на CHUNK_SIZE
            current_chunk_size = min(CHUNK_SIZE, TOTAL_RECORDS - i)

            # Сериализуем каждый объект в байты
            chunk_bytes = [orjson.dumps(random_json(i)) for _ in range(current_chunk_size)]

            # Соединяем объекты через запятую
            joined_chunk = b",\n".join(chunk_bytes)

            # Если это не первый чанк, нужно поставить запятую между прошлым чанком и текущим
            if not first_chunk:
                f.write(b",\n")

            f.write(joined_chunk)
            first_chunk = False

        f.write(b"\n]")

    print(TOTAL_RECORDS)


if __name__ == "__main__":
    main()
