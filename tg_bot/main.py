from environs import Env
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message


env = Env()            
env.read_env()  # читаем файл .env с переменными окружения
                          
bot_token = env('BOT_TOKEN')

bot: Bot = Bot(bot_token)
dp: Dispatcher = Dispatcher()


# хендлер для команды /start, тестовый запуск
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer('Тестовый запуск')


if __name__ == '__main__':
    dp.run_polling(bot)
    