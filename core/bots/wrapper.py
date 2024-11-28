import logging
import asyncio
from functools import wraps
from datetime import datetime, timezone

from logs.logger import get_logger
from core.bots.menu import set_sub_inline_menu
from core.scripts.dwh.manager import insert_user, select_user
from core.templates.message import MESSAGE

logger = get_logger(__name__, level=logging.DEBUG)


def access(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        username = update.effective_user.username

        user = await asyncio.get_event_loop().run_in_executor(None, select_user, user_id)
        if user.empty:
            logger.info(f"New user {username} ({user_id})")

            reply_markup = await set_sub_inline_menu()
            await update.message.reply_markdown_v2(MESSAGE["new_start"], reply_markup=reply_markup)

            if not update.effective_user.is_bot:
                user_data = {
                    "id": user_id,
                    "username": username,
                    "record_updated_dtt": datetime.now(tz=timezone.utc).isoformat(),
                }

                await asyncio.get_event_loop().run_in_executor(None, insert_user, user_data)

            return
        elif not user.has_access[0]:
            logger.warning(f"Access denied for {username} ({user_id})")

            reply_markup = await set_sub_inline_menu()
            if func.__name__ == "start":
                await update.message.reply_markdown_v2(MESSAGE["sub_start"], reply_markup=reply_markup)
                return

            await update.message.reply_markdown_v2(MESSAGE["need_sub"], reply_markup=reply_markup)
            return

        return await func(update, context, *args, **kwargs)

    return wrapped
