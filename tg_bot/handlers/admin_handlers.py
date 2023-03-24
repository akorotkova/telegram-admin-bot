from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from tg_bot.bot_responses import admin_commands as text


# хендлер для команды /current_settings
async def process_current_settings_cmd(message: Message):
    await message.reply(text.CURRENT_SETTINGS_TEXT)


# хендлер для команды /deleting_voice
async def process_deleting_voice_cmd(message: Message):
    await message.reply(text.DELETING_VOICE_TEXT)


# хендлер для команды /deleting_video
async def process_deleting_video_cmd(message: Message):
    await message.reply(text.DELETING_VIDEO_TEXT)


# хендлер для команды /warning_ladder
async def process_warning_ladder_cmd(message: Message):
    await message.reply(text.WARNING_LADDER_TEXT)


# хендлер для команды /deleting_ladder
async def process_deleting_ladder_cmd(message: Message):
    await message.reply(text.DELETING_LADDER_TEXT)


# хендлер для команды /setting_ladder
async def process_setting_ladder_cmd(message: Message):
    await message.reply(text.SETTING_LADDER_TEXT, parse_mode='HTML')


# регистрируем все admin хендлеры
def register_admin_handlers(dp: Dispatcher):
    dp.message.register(process_current_settings_cmd, Command(commands=['current_settings']))
    dp.message.register(process_deleting_voice_cmd, Command(commands=['deleting_voice']))
    dp.message.register(process_deleting_video_cmd, Command(commands=['deleting_video']))
    dp.message.register(process_warning_ladder_cmd, Command(commands=['warning_ladder']))
    dp.message.register(process_deleting_ladder_cmd, Command(commands=['deleting_ladder']))
    dp.message.register(process_setting_ladder_cmd, Command(commands=['setting_ladder']))
    

