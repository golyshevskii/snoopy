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

    app.job_queue.run_repeating(snipe_futures_divergence, interval=15, first=0, data={"interval": 900})
    app.job_queue.run_repeating(snipe_futures_divergence, interval=1800, first=0, data={"interval": 1800})
    app.job_queue.run_repeating(snipe_futures_divergence, interval=3600, first=0, data={"interval": 3600})
    app.job_queue.run_repeating(snipe_futures_divergence, interval=14400, first=0, data={"interval": 14400})

    app.run_polling()
    logger.debug("END")


if __name__ == "__main__":
    """Runs the main logic of the Bot"""
    run()
