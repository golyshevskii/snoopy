import logging
from typing import Dict, Any

from config import MEXC_DATA_PATH
from logs.logger import get_logger
from core.scripts.mexc.api import get_exchange_info
from core.scripts.tools.files import write_file

logger = get_logger(__name__, level=logging.DEBUG)


def import_exchange_info() -> Dict[str, Any]:
    """Imports exchange information."""
    logger.debug("BEGIN")

    info = get_exchange_info()
    write_file(f"{MEXC_DATA_PATH}mexc_exchange_info.json", info, is_json=True)

    logger.debug("END")
