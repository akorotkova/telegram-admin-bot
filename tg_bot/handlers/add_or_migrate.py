from asyncio import sleep

from aiogram import Bot, Router, types, F
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, JOIN_TRANSITION

from tg_bot.cache import migration_cache


router: Router = Router()
chats_variants = {"group": "группу","supergroup": "супергруппу"}


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION),
                       F.chat.type.in_({"group", "supergroup"}))
async def bot_added_to_group(event: types.ChatMemberUpdated, bot: Bot):
    await sleep(1.0)
    if event.chat.id not in migration_cache.keys():
        await bot.send_message(
            chat_id=event.chat.id,
            text=f"Бот добавлен в {chats_variants[event.chat.type]}\nchat ID: {event.chat.id}"
        )


@router.message(F.migrate_to_chat_id)
async def group_to_supegroup_migration(message: types.Message, bot: Bot):
    await bot.send_message(
        message.migrate_to_chat_id,
        f"Группа повышена до супергруппы.\n"
        f"Старый ID: {message.chat.id}\n"
        f"Новый ID: {message.migrate_to_chat_id}"
    )
    migration_cache[message.migrate_to_chat_id] = True
