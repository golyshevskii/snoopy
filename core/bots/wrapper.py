import logging
from functools import wraps

from logs.logger import get_logger
from core.templates.message import MESSAGE

logger = get_logger(__name__, level=logging.DEBUG)


def access(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        username = update.effective_user.username

        # TODO: Get user data from DB
        user = None
        if not user:
            logger.info(f"New user {username} ({user_id})")
            await update.message.reply_markdown_v2(MESSAGE["new_start"])
            return
        elif not user["access"]:
            logger.warning(f"Access denied for {username} ({user_id})")
            await update.message.reply_markdown_v2(MESSAGE["need_sub"])
            return

        return await func(update, context, *args, **kwargs)

    return wrapped
