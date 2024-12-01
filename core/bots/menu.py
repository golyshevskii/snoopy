from telegram import Update
from telegram.ext import CallbackContext
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from core.templates.message import MESSAGE
from core.templates.button import (
    BUTTON_MAP,
    INLINE_EXCHANGE_MENU_BUTTON,
    INLINE_FAQ_MENU_BUTTON,
    INLINE_COIN_MENU_BUTTON,
    INLINE_SETUP_MENU_BUTTON,
)


async def set_menu(only_faq=False):
    """Sets the keyboard menu"""
    if only_faq:
        keyboard = [[KeyboardButton(BUTTON_MAP["faq"])]]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    keyboard = [[KeyboardButton(BUTTON_MAP["commands"]), KeyboardButton(BUTTON_MAP["faq"])]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def set_sub_inline_menu():
    """Sets the inline subscription keyboard menu"""
    inline_keyboard = [[InlineKeyboardButton(BUTTON_MAP["sub-1m"], url="https://0xprocessing.com/")]]
    return InlineKeyboardMarkup(inline_keyboard)


async def set_setup_inline_menu():
    """Sets the inline setup keyboard menu"""
    inline_keyboard = [
        [InlineKeyboardButton(BUTTON_MAP[button], callback_data=f"setup_{button}")]
        for button in INLINE_SETUP_MENU_BUTTON
    ]
    inline_keyboard.append([InlineKeyboardButton(BUTTON_MAP["confirm"], callback_data="confirm_setup")])
    return InlineKeyboardMarkup(inline_keyboard)


async def set_exchange_inline_menu(update: Update, context: CallbackContext):
    """Sets the inline exchange keyboard menu"""
    inline_keyboard = []
    selected_exchanges = context.user_data.get("selected_exchanges", [])

    for exchange in INLINE_EXCHANGE_MENU_BUTTON:
        if exchange in selected_exchanges:
            inline_keyboard.append(
                [InlineKeyboardButton(f"■ {exchange}", callback_data=f"exchange_{exchange}")]
            )
        else:
            inline_keyboard.append(
                [InlineKeyboardButton(f"□ {exchange}", callback_data=f"exchange_{exchange}")]
            )

    inline_keyboard.append([InlineKeyboardButton(BUTTON_MAP["confirm"], callback_data="confirm_exchanges")])
    reply_markup = InlineKeyboardMarkup(inline_keyboard)

    query = update.callback_query
    await query.answer()
    await query.edit_message_text(MESSAGE["select_exchanges"], reply_markup=reply_markup)


async def set_coin_inline_menu(update: Update, context: CallbackContext):
    """Sets the inline exchange keyboard menu"""
    inline_keyboard = []
    selected_coins = context.user_data.get("selected_coins", [])

    for coin in INLINE_COIN_MENU_BUTTON:
        if coin in selected_coins:
            inline_keyboard.append([InlineKeyboardButton(f"■ {coin}", callback_data=f"coin_{coin}")])
        else:
            inline_keyboard.append([InlineKeyboardButton(f"□ {coin}", callback_data=f"coin_{coin}")])

    inline_keyboard.append([InlineKeyboardButton(BUTTON_MAP["confirm"], callback_data="confirm_coins")])
    reply_markup = InlineKeyboardMarkup(inline_keyboard)

    query = update.callback_query
    await query.answer()
    await query.edit_message_text(MESSAGE["select_coins"], reply_markup=reply_markup)


async def set_faq_inline_menu():
    """Sets the FAQ keyboard menu"""
    inline_keyboard = [
        [InlineKeyboardButton(BUTTON_MAP[button], callback_data=f"{button}")]
        for button in INLINE_FAQ_MENU_BUTTON
    ]
    return InlineKeyboardMarkup(inline_keyboard)
