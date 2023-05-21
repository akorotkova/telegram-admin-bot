from aiogram import Bot
from aiogram.types.error_event import ErrorEvent

from tg_bot.utils.logger import logger


async def errors_handler(error: ErrorEvent, bot: Bot):
    try:
        raise error.exception
    except Exception as e:
        logger.exception(
            f'Исключение "{e}". Чат: тип - {error.update.message.chat.type}, '
            f'название - {error.update.message.chat.title}.\n'
            f'Апдейт от {error.update.message.from_user.username}, '
            f'тип апдейта - {error.update.message.content_type}'
        )
