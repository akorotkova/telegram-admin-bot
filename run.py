import asyncio

from aiogram import Bot, Dispatcher

from tg_bot.config import load_config
from tg_bot.handlers import (
    bot_in_chat,
    migrate_group,
    change_admins,
    admin_commands,
    chat_rules,
    chat_tags,
    callbacks,
    user_commands,
    deleting_messages
)


async def main():
    config = load_config('.env')

    bot = Bot(config.tg_bot.token)
    dp = Dispatcher()
    
    dp.include_routers(
        bot_in_chat.router,
        migrate_group.router,
        change_admins.router,
        admin_commands.router,
        chat_rules.router,
        chat_tags.router,
        callbacks.router,
        user_commands.router,
        deleting_messages.router
    )

    await dp.start_polling(
        bot, 
        allowed_updates=dp.resolve_used_update_types(),
        close_bot_session=True
    )


if __name__ == '__main__':
    asyncio.run(main())
    