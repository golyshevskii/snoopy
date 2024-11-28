import logging
import pandas as pd
from typing import Any, Dict, Union, List

from config import DWH_CONN_STR
from logs.logger import get_logger
from core.scripts.tools.psql import PSQLClient
from core.scripts.dwh.table_map import RAW

logger = get_logger(__name__, level=logging.DEBUG)

DWH = PSQLClient(DWH_CONN_STR)


def select_user(user_id: int) -> pd.DataFrame:
    return DWH.execute(
        f"""
        SELECT id, has_access
          FROM {RAW['users']['schema']}.{RAW['users']['table']}
         WHERE id = {user_id};
        """,
        select=True,
    )


def insert_user(user_data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> None:
    DWH.insert(
        schema=RAW["users"]["schema"],
        table=RAW["users"]["table"],
        data=[user_data] if isinstance(user_data, dict) else user_data,
        on_conflict_do_update=True,
        constraint=RAW["users"]["constraint"],
    )


def update_user_access(user_id: int) -> None:
    DWH.execute(
        f"UPDATE {RAW['users']['schema']}.{RAW['users']['table']} SET access = True WHERE id = {user_id};"
    )
