import asyncio

from aiogram import Bot, Dispatcher

from tg_bot.config import Config, load_config
from tg_bot.handlers import bot_in_group, add_or_migrate, admin_handlers, callbacks, user_handlers


async def main():
    config: Config = load_config('.env')

    # инициализируем бот и диспетчер
    bot: Bot = Bot(config.tg_bot.token)
    dp: Dispatcher = Dispatcher()
    
    # регистриуем роутеры в диспетчере
    dp.include_routers(
        bot_in_group.router, 
        add_or_migrate.router, 
        admin_handlers.router,
        callbacks.router,
        user_handlers.router    
    )

    # запуск бота
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), close_bot_session=True)


if __name__ == '__main__':
    asyncio.run(main())
    