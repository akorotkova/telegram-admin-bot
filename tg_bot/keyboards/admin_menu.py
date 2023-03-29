from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tg_bot.handlers.callbacks_data import SettingCallback


# кнопки для включения и отключения настроек бота
def get_setting_buttons() -> InlineKeyboardMarkup:
    
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='Включить', callback_data=SettingCallback(flag='on').pack()))  
    keyboard.row(InlineKeyboardButton(text='Отключить', callback_data=SettingCallback(flag='of').pack())) 

    return keyboard.as_markup()
