from typing import List
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from core.templates.button import BUTTON_MAP, MENU_BUTTON, INLINE_EXCHANGE_MENU_BUTTON


async def set_menu():
    """Sets the keyboard menu"""
    keyboard = [[KeyboardButton(BUTTON_MAP[button])] for button in MENU_BUTTON]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def set_sub_inline_menu():
    """Sets the inline subscription keyboard menu"""
    inline_keyboard = [
        [InlineKeyboardButton(BUTTON_MAP["sub-1m"], url="https://0xprocessing.com/")],
        [InlineKeyboardButton(BUTTON_MAP["faq"], callback_data="faq")],
    ]
    return InlineKeyboardMarkup(inline_keyboard)


async def set_exchange_inline_menu(selected_exchanges: List[str]):
    """Sets the inline exchange keyboard menu"""
    inline_keyboard = []
    for exchange in INLINE_EXCHANGE_MENU_BUTTON:
        if exchange in selected_exchanges:
            inline_keyboard.append(
                [InlineKeyboardButton(f"✅ {exchange}", callback_data=f"exchange_{exchange}")]
            )
        else:
            inline_keyboard.append([InlineKeyboardButton(exchange, callback_data=f"exchange_{exchange}")])

    inline_keyboard.append([InlineKeyboardButton(BUTTON_MAP["confirm"], callback_data="confirm_exchanges")])
    return InlineKeyboardMarkup(inline_keyboard)
