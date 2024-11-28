import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from config import SNOOPY_BOT_TOKEN
from logs.logger import get_logger
from core.bots.command import start
from core.bots.handler import handle_input

logger = get_logger(__name__, level=logging.DEBUG)


def run():
    logger.debug("BEGIN")
    app = ApplicationBuilder().token(SNOOPY_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    # app.add_handler(CommandHandler("setup", setup))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))

    app.run_polling()
    logger.debug("END")


if __name__ == "__main__":
    """Runs the main logic of the Bot"""
    run()
