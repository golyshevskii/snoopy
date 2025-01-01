import logging
from typing import Dict, Any
from datetime import datetime, timedelta, timezone

from config import MEXC_DATA_PATH
from logs.logger import get_logger
from core.scripts.mexc.api import get_spot_info, get_futures_info, get_futures_klines
from core.scripts.mexc.utils import MEXC_INTERVAL_KLINE_DEPTH
from core.scripts.tools.files import write_file

logger = get_logger(__name__, level=logging.DEBUG)


async def import_spot_info() -> Dict[str, Any]:
    """Imports spot exchange information."""
    logger.debug("BEGIN")

    info = get_spot_info()
    write_file(f"{MEXC_DATA_PATH}mexc_spot_info.json", info, is_json=True)

    logger.debug("END")


async def import_futures_info() -> Dict[str, Any]:
    """Imports futures exchange information."""
    logger.debug("BEGIN")

    info = get_futures_info()
    write_file(f"{MEXC_DATA_PATH}mexc_futures_info.json", info, is_json=True)

    logger.debug("END")


async def import_futures_klines(symbol: str, interval: str) -> str:
    """
    Imports MEXC futures klines for a symbol.

    Params:
        symbol: The symbol to get klines for.
        interval: The interval to get klines for.
    """
    logger.debug("BEGIN")

    now = datetime.now(tz=timezone.utc)
    end = int(datetime.timestamp(now))
    start = int(datetime.timestamp(now - timedelta(hours=MEXC_INTERVAL_KLINE_DEPTH[interval])))

    klines = get_futures_klines(symbol, interval, start, end)

    if not klines.get("success"):
        logger.warning(f"Unsuccessfull request. Details: {klines}")
        raise Exception(f"{klines}")

    file = f"{MEXC_DATA_PATH}{symbol}_{interval}.json"
    file = write_file(file, klines["data"], is_json=True)

    logger.debug("END")
    return file
