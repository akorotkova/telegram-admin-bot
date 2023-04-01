import asyncio
from aiogram import Bot, Dispatcher
from tg_bot.config import Config, load_config
from tg_bot.handlers import base_handlers
from tg_bot.handlers import admin_handlers
from tg_bot.handlers.base_handlers import register_base_handlers
from tg_bot.handlers.admin_handlers import register_admin_handlers
from tg_bot.handlers.callbacks import register_callback


async def main():
    config: Config = load_config('.env')

    # инициализируем бот и диспетчер
    bot: Bot = Bot(config.tg_bot.token)
    dp: Dispatcher = Dispatcher()
    
    # регистриуем роутеры в диспетчере
    dp.include_routers(base_handlers.router, admin_handlers.router)
    
    # регистриуем хендлеры и коллбэки
    register_base_handlers(base_handlers.router)
    register_admin_handlers(admin_handlers.router)
    register_callback(admin_handlers.router)

    # запуск бота
    await dp.start_polling(bot, close_bot_session=True)


if __name__ == '__main__':
    asyncio.run(main())
    