from tg_bot.config import load_config
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message


config = load_config('.env')
bot: Bot = Bot(config.tg_bot.token)
dp: Dispatcher = Dispatcher()


# хендлер для команды /start, тестовый запуск
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer('Тестовый запуск')


if __name__ == '__main__':
    dp.run_polling(bot)
