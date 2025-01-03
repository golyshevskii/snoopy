import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD

from core.scripts.exchange.base import Indicator


class RSII(Indicator):
    def __init__(self, period=14, col_name="rsi"):
        self.period = period
        self.col_name = col_name

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        rsi_calc = RSIIndicator(close=df["close"], window=self.period)
        df[self.col_name] = rsi_calc.rsi()
        return df


class MACDI(Indicator):
    def __init__(self, fast=12, slow=26, signal=9, hist_col="macd_hist"):
        self.fast = fast
        self.slow = slow
        self.signal = signal
        self.hist_col = hist_col

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        macd_calc = MACD(
            close=df["close"], window_slow=self.slow, window_fast=self.fast, window_sign=self.signal
        )
        df[self.hist_col] = macd_calc.macd_diff()
        return df
