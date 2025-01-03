from typing import Optional
from abc import ABC, abstractmethod
from pandas import DataFrame


class Exchange(ABC):
    def __init__(self, exchange: str):
        """
        Params:
            exchange: exchange name: "MEXC", "Binance"
        """
        self.exchange = exchange

    @abstractmethod
    def fetch_futures_klines(self, symbol: str, interval: str, start: int = None, end: int = None):
        """
        Fetches futures klines from the exchange.

        Params:
            symbol: symbol name
            interval: klines interval
            start: timestamp from which to get klines
            end: timestamp to which to get klines
        """
        pass

    def __str__(self):
        return self.exchange


class Indicator(ABC):
    @abstractmethod
    def calculate(self, df: DataFrame) -> DataFrame:
        """Calculates indicator for the symbol."""
        pass


class Divergence(ABC):
    def __init__(self, symbol: str, exchange: Exchange, interval_int: int, interval_str: str):
        """
        Params:
            symbol: symbol name: "BTC_USDT", "ETHUSDT"
            exchange: object Exchange
            interval_int: 900, 1800, 3600, 14400
            interval_str: string representation of interval based on exchange
        """
        self.symbol = symbol
        self.exchange = exchange
        self.interval_int = interval_int
        self.interval_str = interval_str

    @abstractmethod
    def detect(self, data: DataFrame) -> Optional[int]:
        """Detects divergence for the specified symbol and exchange."""
        pass
