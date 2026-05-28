from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    @abstractmethod
    async def init(self):
        pass

    @abstractmethod
    async def execute_query(self, query: str, *args):
        pass

    @abstractmethod
    async def upload_data(self):
        pass

    @abstractmethod
    async def clear_data(self):
        pass
