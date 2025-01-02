import asyncio
from functools import wraps
from datetime import datetime, timezone

from logs.logger import get_logger
from core.bots.menu import set_sub_inline_menu, set_menu
from core.scripts.dwh.manager import insert_user, select_user
from core.templates.message import MESSAGE
from core.templates.command import NO_ACCESS_COMMANDS, HAS_ACCESS_COMMANDS

logger = get_logger(__name__)


async def on_empty(update):
    logger.debug(f"New user {update.effective_user.username} ({update.effective_user.id})")

    only_faq = await set_menu(only_faq=True)
    reply_markup = await set_sub_inline_menu()

    await update.message.reply_markdown_v2(MESSAGE["new_start"], reply_markup=reply_markup)
    await update.message.reply_markdown_v2(MESSAGE["only_faq"], reply_markup=only_faq)

    if not update.effective_user.is_bot:
        user_data = {
            "id": update.effective_user.id,
            "username": update.effective_user.username,
            "record_updated_dtt": datetime.now(tz=timezone.utc).isoformat(),
        }

        await asyncio.get_event_loop().run_in_executor(None, insert_user, user_data)


async def on_no_access(update):
    logger.warning(f"Access denied for {update.effective_user.username} ({update.effective_user.id})")

    only_faq = await set_menu(only_faq=True)
    reply_markup = await set_sub_inline_menu()

    await update.message.reply_markdown_v2(MESSAGE["need_sub"], reply_markup=reply_markup)
    await update.message.reply_markdown_v2(MESSAGE["only_faq"], reply_markup=only_faq)


def access(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user = await asyncio.get_event_loop().run_in_executor(None, select_user, update.effective_user.id)
        await context.bot.set_my_commands(
            HAS_ACCESS_COMMANDS if not user.empty and user.has_access[0] else NO_ACCESS_COMMANDS
        )

        if user.empty:
            await on_empty(update)
            return
        elif not user.has_access[0]:
            await on_no_access(update)
            return

        return await func(update, context, *args, **kwargs)

    return wrapped
