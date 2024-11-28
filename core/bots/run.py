import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from config import SNOOPY_BOT_TOKEN
from logs.logger import get_logger
from core.bots.command import start, setup
from core.bots.handler import handle_input, handle_exchange_selection, hendle_confirm_exchanges

logger = get_logger(__name__, level=logging.DEBUG)


def run():
    logger.debug("BEGIN")
    app = ApplicationBuilder().token(SNOOPY_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setup", setup))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))
    app.add_handler(CallbackQueryHandler(handle_exchange_selection, pattern="^exchange_"))
    app.add_handler(CallbackQueryHandler(hendle_confirm_exchanges, pattern="^confirm_exchanges$"))

    app.run_polling()
    logger.debug("END")


if __name__ == "__main__":
    """Runs the main logic of the Bot"""
    run()
