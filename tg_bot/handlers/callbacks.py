from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from tg_bot.keyboards.admin_menu import SettingCallback


# callback для отключения и включения настроек 
async def callback_settings(callback: CallbackQuery, callback_data: SettingCallback):
    if callback_data.flag == 'on':
        await callback.answer(text="Включено", show_alert=True)
    elif callback_data.flag == 'of':
        await callback.answer(text="Отключено", show_alert=True)
    await callback.answer()


# регистрируем коллбеки
def register_callback(dp: Dispatcher):
    dp.callback_query.register(callback_settings, SettingCallback.filter())
