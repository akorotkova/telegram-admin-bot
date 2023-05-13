from functools import wraps

from aiogram import types


def check_chat_is_private(handler):
    @wraps(handler)
    async def inner(message: types.Message, *args, **kwargs):
        if message.chat.type == 'private':
            return await message.reply(text='Команда недоступна в приватном чате')
        return await handler(message, *args, **kwargs)
    return inner
