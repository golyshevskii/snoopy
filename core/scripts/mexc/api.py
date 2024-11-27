import logging
from pymexc import spot
from typing import List, Dict, Any

from config import MEXC_API_ACCESS_KEY, MEXC_API_SECRET_KEY
from logs.logger import get_logger

logger = get_logger(__name__, level=logging.DEBUG)

SPOT = spot.HTTP(api_key=MEXC_API_ACCESS_KEY, api_secret=MEXC_API_SECRET_KEY)


def get_exchange_info(symbol: str = None, symbols: List[str] = None) -> Dict[str, Any]:
    """Gets exchange information about trading rules and symbol information."""
    logger.debug("Getting MEXC exchange info.")
    return SPOT.exchange_info(symbol, symbols)
