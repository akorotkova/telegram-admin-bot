from aiogram import Router
from aiogram.types import CallbackQuery

from tg_bot.handlers.callbacks_data import SettingCallback


router: Router = Router()


@router.callback_query(SettingCallback.filter())
async def callback_settings(callback: CallbackQuery, callback_data: SettingCallback):
    if callback_data.flag == 'on':
        await callback.answer(text="Включено", show_alert=True)
    elif callback_data.flag == 'of':
        await callback.answer(text="Отключено", show_alert=True)
    await callback.answer()
