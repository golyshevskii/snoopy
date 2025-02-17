from telegram import Update
from telegram.ext import ContextTypes, CallbackContext

from logs.logger import get_logger
from core.bots.command import setup
from core.bots.menu import set_exchange_inline_menu, set_faq_inline_menu, set_coin_inline_menu
from core.templates.button import BUTTON_MAP
from core.templates.message import MESSAGE

logger = get_logger(__name__)


async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for user input"""
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    text = update.message.text
    logger.debug(f"Handling {username} ({user_id}) user input text: {text}")

    if text == BUTTON_MAP["commands"]:
        await update.message.reply_markdown_v2(MESSAGE["commands"])
        return

    if text == BUTTON_MAP["faq"]:
        reply_markup = await set_faq_inline_menu()
        await update.message.reply_markdown_v2(MESSAGE["faq"], reply_markup=reply_markup)
        return


async def handle_exchange_selection(update: Update, context: CallbackContext):
    """Handler for exchange selection"""
    query = update.callback_query
    await query.answer()

    selected_exchanges = context.user_data.get("selected_exchanges", [])
    exchange = query.data.split("_")[1]

    if exchange in selected_exchanges:
        selected_exchanges.remove(exchange)
    else:
        selected_exchanges.append(exchange)

    context.user_data["selected_exchanges"] = selected_exchanges
    await set_exchange_inline_menu(update, context)


async def handle_coin_selection(update: Update, context: CallbackContext):
    """Handler for coin selection"""
    query = update.callback_query
    await query.answer()

    selected_coins = context.user_data.get("selected_coins", [])
    coin = query.data.split("_")[1]

    if coin in selected_coins:
        selected_coins.remove(coin)
    else:
        selected_coins.append(coin)

    context.user_data["selected_coins"] = selected_coins
    await set_coin_inline_menu(update, context)


async def handle_confirm_exchanges(update: Update, context: CallbackContext):
    """Handler for exchange selection confirmation"""
    query = update.callback_query
    await query.answer()
    await setup(update, context)


async def handle_confirm_coins(update: Update, context: CallbackContext):
    """Handler for coin selection confirmation"""
    query = update.callback_query
    await query.answer()
    await setup(update, context)


async def handle_confirm_setup(update: Update, context: CallbackContext):
    """Handler for setup confirmation"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(MESSAGE["confirm_setup"], reply_markup=None)


async def handle_faq_question(update: Update, context: CallbackContext):
    """Handler for FAQ question"""
    query = update.callback_query
    await query.answer()

    question = query.data
    logger.debug(f"User {update.effective_user.username} ({update.effective_user.id}) asked: {question}")
    await query.edit_message_text(
        f">{BUTTON_MAP[question]}\n\n\n{MESSAGE[question]}", reply_markup=None, parse_mode="MarkdownV2"
    )
