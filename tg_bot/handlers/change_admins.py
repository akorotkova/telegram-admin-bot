from aiogram import Router, Bot, types
from aiogram.filters.chat_member_updated import (
    ChatMemberUpdatedFilter,
    KICKED, LEFT, RESTRICTED, 
    MEMBER, ADMINISTRATOR, CREATOR
)

from tg_bot.cache import admin_cache
from tg_bot.utils.set_admins import get_admins_id_set


router: Router = Router()


@router.chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=
            (KICKED | LEFT | RESTRICTED | MEMBER) >> (ADMINISTRATOR | CREATOR)
    )
)
async def admin_promoted(event: types.ChatMemberUpdated, bot: Bot):
    admins = admin_cache.get(event.chat.id)
    if not admins:
        admin_cache[event.chat.id] = await get_admins_id_set(chat_id=event.chat.id, bot=bot)
    admin_cache[event.chat.id].add(event.new_chat_member.user.id)


@router.chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=
            (KICKED | LEFT | RESTRICTED | MEMBER) << (ADMINISTRATOR | CREATOR)
    )
)
async def admin_demoted(event: types.ChatMemberUpdated, bot: Bot):
    admins = admin_cache.get(event.chat.id)
    if not admins:
        admin_cache[event.chat.id] = await get_admins_id_set(chat_id=event.chat.id, bot=bot)
    admin_cache[event.chat.id].discard(event.new_chat_member.user.id)
