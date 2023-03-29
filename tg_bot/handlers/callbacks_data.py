from aiogram.filters.callback_data import CallbackData


class SettingCallback(CallbackData, prefix='setting'):
    flag: str
    