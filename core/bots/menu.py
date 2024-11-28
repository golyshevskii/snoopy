from telegram import KeyboardButton, ReplyKeyboardMarkup

from core.templates.button import BUTTON_MAP, MENU_BUTTON


async def set_menu():
    """Sets the keyboard menu"""
    keyboard = [[KeyboardButton(BUTTON_MAP[param])] for param in MENU_BUTTON]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
