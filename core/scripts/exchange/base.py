from typing import Dict, List
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
    async def fetch_futures_klines(self, symbol: str, interval: str, start: int = None, end: int = None):
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
    async def compute(self, data: DataFrame) -> DataFrame:
        """Computes indicator for the symbol."""
        pass


class Divergence(ABC):
    def __init__(self, symbol: str, exchange: Exchange):
        """
        Params:
            symbol: symbol name: "BTC_USDT", "ETHUSDT"
            exchange: object Exchange
        """
        self.symbol = symbol
        self.exchange = exchange

    @abstractmethod
    async def find(self, data: DataFrame) -> Dict[str, List[int]]:
        """Catches divergence for the specified symbol and exchange."""
        pass
