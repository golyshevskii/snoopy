from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from config import SNOOPY_BOT_TOKEN
from logs.logger import get_logger
from core.bots.command import start, setup
from core.bots.menu import set_coin_inline_menu, set_exchange_inline_menu
from core.bots.handler import (
    handle_input,
    handle_exchange_selection,
    handle_confirm_exchanges,
    handle_coin_selection,
    handle_confirm_coins,
    handle_confirm_setup,
    handle_faq_question,
)
from core.bots.utils import INTERVALS, get_first_run_time
from core.scripts.exchange.manager import snipe_futures_divergence

logger = get_logger(__name__)


def run():
    logger.debug("BEGIN")
    app = ApplicationBuilder().token(SNOOPY_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setup", setup))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))

    app.add_handler(CallbackQueryHandler(set_exchange_inline_menu, pattern="^setup_exchanges$"))
    app.add_handler(CallbackQueryHandler(set_coin_inline_menu, pattern="^setup_coins$"))
    app.add_handler(CallbackQueryHandler(handle_confirm_setup, pattern="^confirm_setup$"))
    app.add_handler(CallbackQueryHandler(handle_exchange_selection, pattern="^exchange_"))
    app.add_handler(CallbackQueryHandler(handle_confirm_exchanges, pattern="^confirm_exchanges$"))
    app.add_handler(CallbackQueryHandler(handle_coin_selection, pattern="^coin_"))
    app.add_handler(CallbackQueryHandler(handle_confirm_coins, pattern="^confirm_coins$"))

    app.add_handler(CallbackQueryHandler(handle_faq_question, pattern="^faq_"))

    for interval in INTERVALS:
        first_run = get_first_run_time(interval)
        app.job_queue.run_repeating(
            snipe_futures_divergence,
            interval=interval * 60,
            first=first_run,
            data={"interval": interval * 60},
        )

    app.run_polling()
    logger.debug("END")


if __name__ == "__main__":
    """Runs the main logic of the Bot"""
    run()
