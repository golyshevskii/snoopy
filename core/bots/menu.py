from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from core.templates.button import BUTTON_MAP, MENU_BUTTON


async def set_menu():
    """Sets the keyboard menu"""
    keyboard = [[KeyboardButton(BUTTON_MAP[param])] for param in MENU_BUTTON]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def set_sub_inline_menu():
    """Sets the inline subscription keyboard menu"""
    inline_keyboard = [
        [InlineKeyboardButton("month → $1", callback_data="sub_1m")],
        [InlineKeyboardButton("FAQ", callback_data="faq")],
    ]
    return InlineKeyboardMarkup(inline_keyboard)
