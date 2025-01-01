from core.scripts.mexc.api import get_futures_klines
from core.scripts.exchange.base import Exchange
from core.scripts.exchange.utils import klines_to_df


class MEXCExchange(Exchange):
    def __init__(self):
        super().__init__("MEXC")

    async def fetch_futures_klines(self, symbol: str, interval: str, start: int = None, end: int = None):
        klines = get_futures_klines(symbol, interval, start, end)
        if not klines.get("success"):
            raise Exception(f"{klines}")

        df = await klines_to_df(klines["data"], time_column_name="time", time_unit="s")
        return df


EXCHANGES = {"MEXC": MEXCExchange}
EXCHANGE_FUTURES_LINK_MAP = {"MEXC": "https://futures.mexc.com/ru-RU/exchange/"}
