import logging
from telegram.ext import ContextTypes

from logs.logger import get_logger
from core.scripts.exchange.exchange import EXCHANGES
from core.scripts.exchange.divergence import DIV
from core.templates.message import MESSAGE

logger = get_logger(__name__, level=logging.INFO)


async def snipe_futures_divergence(context: ContextTypes.DEFAULT_TYPE):
    """Snipes futures divergence for selected symbols on selected exchanges."""
    exdiv = dict().fromkeys(EXCHANGES.keys(), None)

    for ex in exdiv:
        exchange = EXCHANGES[ex]
        div = DIV(exchange=exchange["exchange_class"])

        for symbol in exchange["futures_symbols"]:
            div.symbol = symbol
            exdiv[ex][symbol]["result"] = await div.find()

    for chat_id, user_data in context.application.user_data.items():
        if "selected_exchanges" not in user_data and "selected_coins" not in user_data:
            continue

        selected_exchanges = user_data["selected_exchanges"]
        selected_coins = user_data["selected_coins"]

        for ex in selected_exchanges:
            for coin in selected_coins:

                result = exdiv[ex][coin]["result"]
                if result:
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=(MESSAGE["0DIV"] if result == 0 else MESSAGE["1DIV"]).format(
                            exchange=ex, symbol=coin
                        ),
                        parse_mode="MarkdownV2",
                    )
