import asyncio

from aiogram import Bot, Dispatcher

from tg_bot.utils.logger import logger
from tg_bot.config import load_config
from tg_bot.handlers.errors import errors_handler
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
    logger.info('start bot')
    
    config = load_config('.env')

    bot = Bot(config.tg_bot.token)
    dp = Dispatcher()

    dp.errors.register(errors_handler)
    
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

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), close_bot_session=True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.critical('bot stopped')
    