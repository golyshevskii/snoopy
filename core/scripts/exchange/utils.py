import pandas as pd
from typing import Dict, List


async def klines_to_df(
    klines: Dict[str, List[int | float]], time_column_name: str, time_unit: str = "ms"
) -> pd.DataFrame:
    """
    Converts klines to DataFrame.

    Params:
        klines: symbol candle sticks data
        time_column_name: name of the time column
        time_unit: time unit
    """
    df = pd.DataFrame(klines)
    df[time_column_name] = pd.to_datetime(df[time_column_name], unit=time_unit)
    df.set_index(time_column_name, inplace=True)
    return df
