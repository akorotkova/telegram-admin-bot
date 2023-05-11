from aiogram import Router, Bot, types, F

from tg_bot.cache import migration_cache


router = Router()


@router.message(F.migrate_to_chat_id)
async def group_to_supegroup_migration(message: types.Message, bot: Bot):  
    await bot.send_message(
        message.migrate_to_chat_id,
        f'Группа повышена до супергруппы.\n'
        f'Старый ID: {message.chat.id}\n'
        f'Новый ID: {message.migrate_to_chat_id}'
    )
    migration_cache[message.migrate_to_chat_id] = True
