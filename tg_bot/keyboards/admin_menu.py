from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup


# кнопки для включения и отключения настроек бота
def get_setting_buttons() -> InlineKeyboardMarkup:
    inline_keyboard = [[
        InlineKeyboardButton(text='Включить', callback_data='Включено'),
        InlineKeyboardButton(text='Отключить', callback_data='Отключено')
        ]]
    
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
