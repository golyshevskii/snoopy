from typing import List
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from core.templates.button import BUTTON_MAP, INLINE_EXCHANGE_MENU_BUTTON, INLINE_FAQ_MENU_BUTTON


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


async def set_exchange_inline_menu(selected_exchanges: List[str]):
    """Sets the inline exchange keyboard menu"""
    inline_keyboard = []
    for exchange in INLINE_EXCHANGE_MENU_BUTTON:
        if exchange in selected_exchanges:
            inline_keyboard.append(
                [InlineKeyboardButton(f"☑ {exchange}", callback_data=f"exchange_{exchange}")]
            )
        else:
            inline_keyboard.append(
                [InlineKeyboardButton(f"☐ {exchange}", callback_data=f"exchange_{exchange}")]
            )

    inline_keyboard.append([InlineKeyboardButton(BUTTON_MAP["confirm"], callback_data="confirm_exchanges")])
    return InlineKeyboardMarkup(inline_keyboard)


async def set_faq_inline_menu():
    """Sets the FAQ keyboard menu"""
    inline_keyboard = [
        [InlineKeyboardButton(BUTTON_MAP[button], callback_data=f"{button}")]
        for button in INLINE_FAQ_MENU_BUTTON
    ]
    return InlineKeyboardMarkup(inline_keyboard)
