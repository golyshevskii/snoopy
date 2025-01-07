import logging

from core.scripts.mexc.api import get_futures_klines
from core.scripts.exchange.base import Exchange
from core.scripts.exchange.divergence import RSIMACDDivergence
from core.scripts.exchange.indicator import RSII, MACDI
from core.scripts.exchange.utils import klines_to_df
from logs.logger import get_logger

logger = get_logger(__name__, level=logging.INFO)


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
        "indicators": [
            RSII(period=14, col_name="rsi"),
            MACDI(fast=12, slow=26, signal=9, hist_col="macd_hist"),
        ],
        "divergence": RSIMACDDivergence(
            price_col="close", rsi_col="rsi", macd_hist_col="macd_hist", order=3, max_candle_diff=2
        ),
        "futures_symbols": ["BTC_USDT", "ETH_USDT", "SOL_USDT"],
        "futures_link": "[MEXC](https://futures.mexc.com/exchange/{symbol}_USDT)",
        "intervals": {900: "Min15", 1800: "Min30", 3600: "Hour1", 14400: "Hour4"},
    }
}
