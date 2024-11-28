import logging
from typing import Dict, Any

from config import MEXC_DATA_PATH
from logs.logger import get_logger
from core.scripts.mexc.api import get_spot_info, get_futures_info
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
