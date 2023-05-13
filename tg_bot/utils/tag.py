from functools import wraps

from aiogram import types


imitation_db_msg = {}  # имитация бд для тегов 

def check_tag_in_chat(handler):
    @wraps(handler)
    async def inner(message: types.Message, *args, **kwargs):
        chat_id = message.chat.id 
        if chat_id not in imitation_db_msg:
            return await message.reply(text='В вашем чате пока что нет тегов')
        return await handler(message, *args, **kwargs)
    return inner
