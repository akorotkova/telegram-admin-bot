from aiogram import Bot, Router
from aiogram.types import CallbackQuery

from tg_bot.handlers.callbacks_data import SettingCallback
from tg_bot.cache import admin_cache
from tg_bot.utils.utils import get_admins_id_set


router: Router = Router()


@router.callback_query(SettingCallback.filter())
async def callback_settings(callback: CallbackQuery, callback_data: SettingCallback, bot: Bot):
    chat_id = callback.message.chat.id
    admins = admin_cache.get(chat_id)
    if not admins:
        admin_cache[callback.message.chat.id] = await get_admins_id_set(chat_id=chat_id, bot=bot)
    if callback.from_user.id in admins:
        if callback_data.flag == 'on':
            await callback.answer(text="Включено", show_alert=True)
        elif callback_data.flag == 'of':
            await callback.answer(text="Отключено", show_alert=True)
    else:
        await callback.answer(text="Доступно только админам", show_alert=True)
    await callback.answer()
