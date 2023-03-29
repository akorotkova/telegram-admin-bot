import asyncio
from aiogram import Bot, Dispatcher
from tg_bot.config import load_config
from tg_bot.handlers.base_handlers import register_base_handlers
from tg_bot.handlers.admin_handlers import register_admin_handlers
from tg_bot.handlers.callbacks import register_callback


# регистрация всех хендлеров
def register_all_handlers(dp):
    register_base_handlers(dp)
    register_admin_handlers(dp)


async def main():
    config = load_config('.env')
    bot: Bot = Bot(config.tg_bot.token)
    dp: Dispatcher = Dispatcher()
    
    register_all_handlers(dp)
    register_callback(dp)
    
    # запуск бота
    await dp.start_polling(bot, close_bot_session=True)


if __name__ == '__main__':
    asyncio.run(main())
    