from tg_bot.config import load_config
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import tg_bot.bot_responses.text as text_responses


config = load_config('.env')
bot: Bot = Bot(config.tg_bot.token)
dp: Dispatcher = Dispatcher()


# хендлер для команды /start и /help
@dp.message(Command(commands=['start', 'help']))
async def process_start_and_help_cmd(message: Message):
    await message.answer(text_responses.START_AND_HELP_TEXT, parse_mode='HTML')


# хендлер для команды !command_admin_bot
@dp.message(Command('command_admin_bot', prefix='!'))
async def process_command_admin_bot_cmd(message: Message):
    await message.answer(text_responses.COMMAND_ADMIN_BOT_TEXT)


# хендлер для команды !about_admin_bot
@dp.message(Command('about_admin_bot', prefix='!'))
async def process_about_admin_bot_cmd(message: Message):
    await message.reply(text_responses.ABOUT_ADMIN_BOT_TEXT)


if __name__ == '__main__':
    dp.run_polling(bot)
