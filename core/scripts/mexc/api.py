import logging
from pymexc import spot, futures
from typing import List, Dict, Any

from config import MEXC_API_ACCESS_KEY, MEXC_API_SECRET_KEY
from logs.logger import get_logger

logger = get_logger(__name__, level=logging.DEBUG)

SPOT = spot.HTTP(api_key=MEXC_API_ACCESS_KEY, api_secret=MEXC_API_SECRET_KEY)
FUTURES = futures.HTTP(api_key=MEXC_API_ACCESS_KEY, api_secret=MEXC_API_SECRET_KEY)


def get_spot_info(symbol: str = None, symbols: List[str] = None) -> Dict[str, Any]:
    """Gets spot exchange information about trading rules and symbol(s)."""
    logger.debug("Getting MEXC spot exchange info.")
    return SPOT.exchange_info(symbol, symbols)


def get_futures_info(symbol: str = None) -> Dict[str, Any]:
    """Gets futures exchange information about trading rules and symbol."""
    logger.debug("Getting MEXC futures exchange info.")
    return FUTURES.detail(symbol)


def get_futures_klines(symbol: str, interval: str, start: int = None, end: int = None) -> Dict[str, Any]:
    """
    Gets futures klines for a symbol.

    Params:
        symbol: The symbol to get klines for.
        interval: The interval to get klines for.
        start: The start time to get klines for.
        end: The end time to get klines for.

        See: https://mexcdevelop.github.io/apidocs/contract_v1_en/#k-line-data
    """
    logger.debug(f"Getting MEXC futures {symbol=} klines for {interval=}.")
    return FUTURES.kline(symbol, interval, start, end)
