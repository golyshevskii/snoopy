import logging
from telegram import Update
from telegram.ext import ContextTypes, CallbackContext

from logs.logger import get_logger
from core.bots.menu import set_menu, set_exchange_inline_menu
from core.bots.wrapper import access
from core.templates.message import MESSAGE
from core.templates.command import NO_ACCESS_COMMANDS, HAS_ACCESS_COMMANDS

logger = get_logger(__name__, level=logging.DEBUG)


async def set_commands(context: ContextTypes.DEFAULT_TYPE, has_access: bool = False):
    """Sets the bot commands"""
    await context.bot.set_my_commands(HAS_ACCESS_COMMANDS if has_access else NO_ACCESS_COMMANDS)


@access
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    user_id = update.effective_user.id
    username = update.effective_user.username
    logger.debug(f"User {username} ({user_id}) started the bot")

    reply_markup = await set_menu()
    await update.message.reply_markdown_v2(MESSAGE["start"], reply_markup=reply_markup)


@access
async def setup(update: Update, context: CallbackContext):
    """Setup exchanges command handler"""
    if "selected_exchanges" not in context.user_data:
        context.user_data["selected_exchanges"] = []

    selected_exchanges = context.user_data["selected_exchanges"]
    reply_markup = await set_exchange_inline_menu(selected_exchanges)

    await update.message.reply_markdown_v2(MESSAGE["select_exchanges"], reply_markup=reply_markup)
