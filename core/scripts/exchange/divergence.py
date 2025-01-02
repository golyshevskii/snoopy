from typing import Optional
from datetime import datetime, timedelta, timezone

from core.scripts.exchange.base import Exchange, Divergence
from logs.logger import get_logger

logger = get_logger(__name__)

KLINES_LIMIT = {900: 25, 1800: 50, 3600: 100, 14400: 400}


class DIV(Divergence):
    def __init__(self, symbol: str, exchange: Exchange, interval_int: int, interval_str: str):
        """
        Params:
            symbol: "BTC_USDT"
            exchange: object Exchange (MEXCExchange)
            interval_int: 900, 1800, 3600, 14400
            interval_str: string representation of interval based on exchange
        """
        super().__init__(symbol, exchange, interval_int, interval_str)

    def find(self) -> Optional[int]:
        logger.info(f"Catching {self.interval_str} divergence for {self.symbol}")

        now = datetime.now(timezone.utc)
        end = int(datetime.timestamp(now))
        start = int(datetime.timestamp(now - timedelta(hours=KLINES_LIMIT[self.interval_int])))

        klines = self.exchange.fetch_futures_klines(
            symbol=self.symbol, interval=self.interval_str, start=start, end=end
        )
        if klines.empty:
            return

        result = 0
        # TODO: Calculate divergence

        return result
