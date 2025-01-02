from core.scripts.mexc.api import get_futures_klines
from core.scripts.exchange.base import Exchange
from core.scripts.exchange.utils import klines_to_df


class MEXCExchange(Exchange):
    def __init__(self):
        super().__init__("MEXC")

    def fetch_futures_klines(self, symbol: str, interval: str, start: int = None, end: int = None):
        klines = get_futures_klines(symbol, interval, start, end)
        if not klines.get("success"):
            raise Exception(f"{klines}")

        df = klines_to_df(klines["data"], time_column_name="time", time_unit="s")
        return df


EXCHANGES = {
    "MEXC": {
        "exchange_class": MEXCExchange(),
        "futures_symbols": ["BTC_USDT", "ETH_USDT", "SOL_USDT"],
        "futures_link": "https://futures.mexc.com/ru-RU/exchange/",
        "intervals": {900: "Min15", 1800: "Min30", 3600: "Hour1", 14400: "Hour4"},
    }
}
