import re
import logging
import asyncio
from telegram.ext import ContextTypes

from logs.logger import get_logger
from core.scripts.exchange.exchange import EXCHANGES
from core.scripts.exchange.divergence import DIVFutures
from core.templates.message import MESSAGE

logger = get_logger(__name__, level=logging.INFO)

INTERVALS = {900: "15M", 1800: "30M", 3600: "1H", 14400: "4H"}


async def snipe_futures_divergence(context: ContextTypes.DEFAULT_TYPE):
    """Snipes futures divergence for selected symbols on selected exchanges."""
    exchange_div = dict().fromkeys(EXCHANGES.keys(), None)
    interval = context.job.data["interval"]

    for ex in EXCHANGES.keys():
        exchange = EXCHANGES[ex]
        exchange_div[ex] = dict().fromkeys(exchange["futures_symbols"], None)

        div = DIVFutures(
            symbol=None,
            exchange=exchange["exchange_class"],
            interval_int=interval,
            interval_str=exchange["intervals"][interval],
            indicators=exchange["indicators"],
            divergence=exchange["divergence"],
        )

        for symbol in exchange["futures_symbols"]:
            div.symbol = symbol
            exchange_div[ex][re.sub(r"_?USDT$", "", symbol)] = (div.find(), interval)

            await asyncio.sleep(0.2)

    for chat_id, user_data in context.application.user_data.items():
        if "selected_exchanges" not in user_data and "selected_coins" not in user_data:
            continue

        selected_exchanges = user_data["selected_exchanges"]
        selected_coins = user_data["selected_coins"]

        for ex in selected_exchanges:
            for coin in selected_coins:

                result = exchange_div[ex][coin]
                if result is not None:
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=(MESSAGE["0DIV"] if result == 0 else MESSAGE["1DIV"]).format(
                            exchange=f"\[{ex}\]\({EXCHANGES[ex]['futures_link']}\)",
                            interval=INTERVALS[interval],
                            symbol=coin,
                        ),
                        parse_mode="MarkdownV2",
                    )
