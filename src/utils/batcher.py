from typing import Iterable

from src.config.settings import settings


def batch(objects: Iterable[list[dict]]):

    batch: list[dict] = []
    i = 1

    for obj in objects:
        batch.append(obj)
        if len(batch) >= settings.BATCH_SIZE:
            yield batch
            batch = []
            i += 1

    if batch:
        yield batch
