from typing import Set
from abc import ABC, abstractmethod

from config import DATA_PATH
from core.scripts.tools.files import read_file, write_file


class Exchange(ABC):
    def __init__(self, name: str):
        self.name = name
        self.lname = name.lower()

        self.listed_coins_file = f"{DATA_PATH}{self.lname}/{self.lname}_listed_coins.json"
        self.listed_coins = set(read_file(self.listed_coins_file, is_json=True)["coins"])

    @abstractmethod
    async def extract_symbols(self):
        pass

    @abstractmethod
    async def catch_listings(self):
        pass

    async def update_listed_coins(self, ids: Set[int]):
        write_file(self.listed_coins_file, {"coins": list(self.listed_coins | ids)}, is_json=True)

    def __str__(self):
        return self.name
