from aiogram import Bot

from tg_bot.cache import admin_cache


async def get_admins_id_set(chat_id: int, bot: Bot):
    admins = await bot.get_chat_administrators(chat_id)
    admins = {admin.user.id for admin in admins}
    admin_cache[chat_id] = admins
    return admins
