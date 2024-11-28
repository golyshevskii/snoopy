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
