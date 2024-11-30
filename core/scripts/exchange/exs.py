from datetime import datetime, timezone
from typing import List, Dict, Any

from core.scripts.mexc.api import get_futures_info
from core.scripts.exchange.base import Exchange


class MEXC(Exchange):
    def __init__(self):
        super().__init__("MEXC")

    async def extract_symbols(self):
        return get_futures_info()["data"]

    async def catch_listings(self, symbols: List[Dict[str, Any]]):
        listings = []
        min30_ago = round(datetime.now(timezone.utc).timestamp() * 1000) - 1800000

        for symbol in symbols:
            if (
                symbol["id"] not in self.listed_coins
                and symbol["isNew"]
                and symbol["openingTime"] > min30_ago
            ):
                listings.append(symbol)

        return listings
