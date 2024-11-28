import logging
from telegram import Update
from telegram.ext import ContextTypes

from logs.logger import get_logger
from core.templates.button import BUTTON_MAP
from core.templates.message import MESSAGE

logger = get_logger(__name__, level=logging.DEBUG)


async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for user input"""
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    text = update.message.text
    logger.debug(f"Handling {username} ({user_id}) user input text: {text}")

    if text == BUTTON_MAP["commands"]:
        await update.message.reply_markdown_v2(MESSAGE["commands"])
