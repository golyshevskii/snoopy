import logging
from telegram import Update
from telegram.ext import ContextTypes

from logs.logger import get_logger
from core.bots.menu import set_menu
from core.bots.wrapper import access
from core.templates.message import MESSAGE

logger = get_logger(__name__, level=logging.DEBUG)


@access
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    user_id = update.effective_user.id
    username = update.effective_user.username
    logger.debug(f"User {username} ({user_id}) started the bot")

    reply_markup = await set_menu()
    await update.message.reply_markdown_v2(MESSAGE["start"], reply_markup=reply_markup)
