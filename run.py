import asyncio

from aiogram import Bot, Dispatcher

from tg_bot.config import load_config
from tg_bot.handlers import (
    bot_in_chat,
    migrate_group,
    admin_changes_in_group,
    admin_handlers, 
    callbacks,
    user_handlers,
    bot_handlers
)


async def main():
    config = load_config('.env')

    bot = Bot(config.tg_bot.token)
    dp = Dispatcher()
    
    dp.include_routers(
        bot_in_chat.router,
        migrate_group.router,
        admin_changes_in_group.router,
        admin_handlers.router,
        callbacks.router,
        user_handlers.router,
        bot_handlers.router
    )

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), close_bot_session=True)


if __name__ == '__main__':
    asyncio.run(main())
    