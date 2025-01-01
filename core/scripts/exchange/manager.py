import logging
from telegram.ext import ContextTypes

from logs.logger import get_logger
from core.scripts.exchange.exchange import EXCHANGES, EXCHANGE_FUTURES_LINK_MAP

logger = get_logger(__name__, level=logging.INFO)


async def snipe_divergence(context: ContextTypes.DEFAULT_TYPE):
    """Snipes divergence for selected symbols on selected exchanges."""
    for chat_id, user_data in context.application.user_data.items():
        if "selected_exchanges" not in user_data and "selected_coins" not in user_data:
            continue

        selected_exchanges = user_data["selected_exchanges"]
        selected_coins = user_data["selected_coins"]

        for ex in selected_exchanges:
            client = EXCHANGES.get(ex)

            if not client:
                logger.warning(f"The exchange {ex} is not supported. Skipping.")
                continue

            try:
                symbols = await client.extract_symbols()
                listings = await client.catch_listings(symbols)

                ids = set()
                for listing in listings:
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=f"[{ex}]({EXCHANGE_FUTURES_LINK_MAP[ex]}{listing['symbol']}) → \#{listing['baseCoin']}",
                        parse_mode="MarkdownV2",
                    )
                    ids.add(listing["id"])

                await client.update_listed_coins(ids)

            except Exception as e:
                logger.error(f"Failed to snipe listings for {ex}. {e}")
