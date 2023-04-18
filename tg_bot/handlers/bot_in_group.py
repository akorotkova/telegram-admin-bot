from aiogram import Bot, Router, F
from aiogram.filters.chat_member_updated import (
    ChatMemberUpdatedFilter,
    IS_NOT_MEMBER,
    MEMBER,
    ADMINISTRATOR
)
from aiogram.types import ChatMemberUpdated


router: Router = Router()
router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))
chats_variants = {"group": "группу", "supergroup": "супергруппу"}


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> MEMBER))
async def bot_added_as_member(event: ChatMemberUpdated, bot: Bot):
    chat_info = await bot.get_chat(event.chat.id)
    if chat_info.permissions.can_send_messages:
        await bot.send_message(
            chat_id=event.chat.id,
            text=f"Привет! Вы добавили меня в "
                 f'{chats_variants[event.chat.type]} "{event.chat.title}" '
                 f"как обычного участника. ID чата: {event.chat.id}\n"
                 f'Чтобы я мог помогать с модерацией чата, добавьте меня в админы.'
        )
    else:
        print("логирование этой ситуации")


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER >> ADMINISTRATOR))
async def bot_added_as_admin(event: ChatMemberUpdated, bot: Bot):
    await bot.send_message(
        chat_id=event.chat.id,
        text=f"Спасибо, что добавили меня в "
             f'{chats_variants[event.chat.type]} "{event.chat.title}" '
             f"как администратора. ID чата: {event.chat.id}\n"
             f'Теперь я буду помогать вам с модерацией. Перейдите в настройки: /command_admin_bot'
        )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=ADMINISTRATOR >> MEMBER))
async def bot_added_as_admin(event: ChatMemberUpdated, bot: Bot):
    await bot.send_message(
        chat_id=event.chat.id,
        text=f"Вы удалили бот из администраторов чата.\nЧтобы бот мог помогать с модерацией, ему нужны права админа."
    )
