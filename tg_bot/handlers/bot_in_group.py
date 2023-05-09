from aiogram import Bot, Router, F
from aiogram.filters.chat_member_updated import (
    ChatMemberUpdatedFilter,
    IS_NOT_MEMBER,
    MEMBER,
    ADMINISTRATOR
)
from aiogram.types import ChatMemberUpdated


router: Router = Router()
router.my_chat_member.filter(F.chat.type.in_({'group', 'supergroup'}))
chats_variants = {'group': 'группу', 'supergroup': 'супергруппу'}


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> MEMBER))
async def bot_added_as_member(event: ChatMemberUpdated, bot: Bot):
    chat_info = await bot.get_chat(event.chat.id)
    if chat_info.permissions.can_send_messages:
        await bot.send_message(
            chat_id=event.chat.id,
            text=f'Привет! Вы добавили меня в '
                 f'<b>{chats_variants[event.chat.type]}</b> "{event.chat.title}" '
                 f'как обычного участника.\n'
                 f'Чтобы я мог помогать вам с модерацией чата, добавьте меня в админы '
                 f'и разрешите удалять сообщения в чате.',
                 parse_mode='HTML'
        )
        if event.chat.type == 'group':
            await bot.send_message(
                chat_id=event.chat.id,
                text=f'Некоторые мои функции доступны только в <b>супергруппах</b>:\n'
                     f'https://t.me/tginfo/2856\n'
                     f'https://t.me/tginfo/1917',
                     parse_mode='HTML'
            )
    else:
        print('логирование этой ситуации')


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER >> ADMINISTRATOR))
async def bot_added_as_admin(event: ChatMemberUpdated, bot: Bot):
    await bot.send_message(
        chat_id=event.chat.id,
        text=f'Спасибо, что добавили меня в администраторы! '
             f'Теперь я буду помогать вам с модерацией.\n'
             f'Перейдите в настройки: /command'
    )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=ADMINISTRATOR))
async def bot_restricted_admin(event: ChatMemberUpdated, bot: Bot):
    chat_member = event.new_chat_member
    if not chat_member.can_delete_messages:
        await bot.send_message(
            chat_id=event.chat.id,
            text=f'Вы ограничили мне права.\n'
                 f'Чтобы я мог помогать вам с модерацией, мне нужны все права админа.'
        )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=ADMINISTRATOR >> MEMBER))
async def bot_added_as_admin(event: ChatMemberUpdated, bot: Bot):
    await bot.send_message(
        chat_id=event.chat.id,
        text=f'Вы удалили меня из администраторов чата.\n'
             f'Чтобы я мог помогать вам с модерацией, мне нужны права админа.'
    )
