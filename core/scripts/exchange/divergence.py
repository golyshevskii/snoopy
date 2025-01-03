import numpy as np
import pandas as pd
from typing import Optional, List
from datetime import datetime, timedelta, timezone
from scipy.signal import argrelextrema

from core.scripts.exchange.base import Exchange, Divergence, Indicator
from logs.logger import get_logger

logger = get_logger(__name__)

KLINES_LIMIT = {900: 25, 1800: 50, 3600: 100, 14400: 400}


class RSIMACDDivergence(Divergence):
    def __init__(
        self, price_col="close", rsi_col="rsi", macd_hist_col="macd_hist", order=3, max_candle_diff=2
    ):
        self.price_col = price_col
        self.rsi_col = rsi_col
        self.macd_hist_col = macd_hist_col
        self.order = order
        self.max_candle_diff = max_candle_diff

    def detect(self, df: pd.DataFrame) -> Optional[int]:
        if (
            self.price_col not in df.columns
            or self.rsi_col not in df.columns
            or self.macd_hist_col not in df.columns
        ):
            logger.warning(
                "Not enough columns to calculate divergence. Please check: price_col, rsi_col, macd_hist_col."
            )
            return

        price = df[self.price_col].values
        rsi = df[self.rsi_col].values
        macd_hist = df[self.macd_hist_col].values

        local_max_price = argrelextrema(price, np.greater, order=self.order)[0]
        local_min_price = argrelextrema(price, np.less, order=self.order)[0]

        local_max_rsi = argrelextrema(rsi, np.greater, order=self.order)[0]
        local_min_rsi = argrelextrema(rsi, np.less, order=self.order)[0]

        local_max_macd = argrelextrema(macd_hist, np.greater, order=self.order)[0]
        local_min_macd = argrelextrema(macd_hist, np.less, order=self.order)[0]

        # Bullish: проверим, есть ли пара экстр. цены, где цена ↓, а RSI & MACD ↑
        # Упростим: смотрим только на последние 2 экстремума
        for i in range(1, len(local_min_price)):
            curr_idx = local_min_price[i]
            prev_idx = local_min_price[i - 1]

            # Цена реально пошла ниже
            if price[curr_idx] < price[prev_idx]:
                # RSI
                rsi_min_curr = [x for x in local_min_rsi if abs(x - curr_idx) <= self.max_candle_diff]
                rsi_min_prev = [x for x in local_min_rsi if abs(x - prev_idx) <= self.max_candle_diff]

                if rsi_min_curr and rsi_min_prev:
                    if rsi[rsi_min_curr[0]] > rsi[rsi_min_prev[-1]]:
                        # Проверим MACD
                        macd_min_curr = [
                            x for x in local_min_macd if abs(x - curr_idx) <= self.max_candle_diff
                        ]
                        macd_min_prev = [
                            x for x in local_min_macd if abs(x - prev_idx) <= self.max_candle_diff
                        ]

                        if macd_min_curr and macd_min_prev:
                            if macd_hist[macd_min_curr[0]] > macd_hist[macd_min_prev[-1]]:
                                return 1

        # Bearish: проверим, есть ли пара экстр. цены, где цена ↑, а RSI & MACD ↓
        for i in range(1, len(local_max_price)):
            curr_idx = local_max_price[i]
            prev_idx = local_max_price[i - 1]

            # Цена реально пошла выше
            if price[curr_idx] > price[prev_idx]:
                # RSI
                rsi_max_curr = [x for x in local_max_rsi if abs(x - curr_idx) <= self.max_candle_diff]
                rsi_max_prev = [x for x in local_max_rsi if abs(x - prev_idx) <= self.max_candle_diff]

                if rsi_max_curr and rsi_max_prev:
                    if rsi[rsi_max_curr[0]] < rsi[rsi_max_prev[-1]]:
                        # MACD
                        macd_max_curr = [
                            x for x in local_max_macd if abs(x - curr_idx) <= self.max_candle_diff
                        ]
                        macd_max_prev = [
                            x for x in local_max_macd if abs(x - prev_idx) <= self.max_candle_diff
                        ]

                        if macd_max_curr and macd_max_prev:
                            if macd_hist[macd_max_curr[0]] < macd_hist[macd_max_prev[-1]]:
                                return 0

        return None


class DIVFutures:
    def __init__(
        self,
        symbol: str,
        exchange: Exchange,
        interval_int: int,
        interval_str: str,
        indicators: List[Indicator],
        divergence: Divergence,
    ):
        """
        Params:
            symbol: "BTC_USDT"
            exchange: object Exchange (MEXCExchange)
            interval_int: 900, 1800, 3600, 14400
            interval_str: string representation of interval based on exchange
            indicators: list of indicators to use to catch divergence
            divergence: Divergence object to catch divergence
        """
        self.symbol = symbol
        self.exchange = exchange
        self.interval_int = interval_int
        self.interval_str = interval_str
        self.indicators = indicators
        self.divergence = divergence

    def find(self) -> Optional[int]:
        logger.info(f"Catching {self.interval_str} divergence for {self.symbol}")

        now = datetime.now(timezone.utc)
        end = int(datetime.timestamp(now))
        start = int(datetime.timestamp(now - timedelta(hours=KLINES_LIMIT[self.interval_int])))

        klines = self.exchange.fetch_futures_klines(
            symbol=self.symbol, interval=self.interval_str, start=start, end=end
        )

        if klines.empty:
            logger.info(f"No klines for {self.symbol} in {self.interval_str}")
            return

        for ind in self.indicators:
            df = ind.calculate(klines)

        result = self.divergence.detect(df)
        return result
