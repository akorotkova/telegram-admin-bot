from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from tg_bot.bot_responses import base_commands as text


# хендлер для команды /start и /help
async def process_start_and_help_cmd(message: Message):
    await message.answer(text.START_AND_HELP_TEXT)


# хендлер для команды /command_admin_bot
async def process_command_admin_bot_cmd(message: Message):
    await message.answer(text.COMMAND_ADMIN_BOT_TEXT)


# хендлер для команды /about_admin_bot
async def process_about_admin_bot_cmd(message: Message):
    await message.reply(text.ABOUT_ADMIN_BOT_TEXT)


# регистрируем все base хендлеры
def register_base_handlers(dp: Dispatcher):
    dp.message.register(process_start_and_help_cmd, Command(commands=['start', 'help']))
    dp.message.register(process_command_admin_bot_cmd, Command(commands=['command_admin_bot']))
    dp.message.register(process_about_admin_bot_cmd, Command(commands=['about_admin_bot']))
                        