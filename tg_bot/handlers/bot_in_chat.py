from asyncio import sleep

from aiogram import Router, Bot, types, F
from aiogram.filters.chat_member_updated import (
    ChatMemberUpdatedFilter,
    IS_NOT_MEMBER,
    MEMBER,
    ADMINISTRATOR
)

from tg_bot.cache import migration_cache


_chats_variants = {'group': 'группу', 'supergroup': 'супергруппу'}

router = Router()
router.my_chat_member.filter(F.chat.type.in_(_chats_variants))


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> MEMBER))
async def bot_added_in_chat_as_member(event: types.ChatMemberUpdated, bot: Bot):
    await sleep(1.0)  # учитываем миграцию группы в супергруппу

    if event.chat.id not in migration_cache.keys():
        chat_info = await bot.get_chat(event.chat.id)
        
        if chat_info.permissions.can_send_messages:
            await bot.send_message(
                chat_id=event.chat.id,
                text=f'Привет! Вы добавили меня в '
                     f'<b>{_chats_variants[event.chat.type]}: "{event.chat.title}"</b> '
                     f'как обычного участника.\n'
                     f'Чтобы я мог помогать вам с модерацией чата, добавьте меня в админы '
                     f'и разрешите удалять сообщения в чате.',
                parse_mode='HTML'
            )
            if event.chat.type == 'group':
                await bot.send_message(
                    chat_id=event.chat.id,
                    text='Некоторые мои функции доступны только в <b>супергруппах</b>:\n'
                         'https://t.me/tginfo/2856\n'
                         'https://t.me/tginfo/1917',
                    parse_mode='HTML'
                )
        else:
            pass  # TODO логирование этой ситуации


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER >> ADMINISTRATOR))
async def bot_added_to_admins(event: types.ChatMemberUpdated, bot: Bot):
    await bot.send_message(
        chat_id=event.chat.id,
        text='Спасибо, что добавили меня в администраторы! '
             'Теперь я буду помогать вам с модерацией.\n'
             'Перейдите в настройки: /command'
    )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=ADMINISTRATOR >> MEMBER))
async def bot_removed_from_admins(event: types.ChatMemberUpdated, bot: Bot):
    await bot.send_message(
        chat_id=event.chat.id,
        text='Вы удалили меня из администраторов чата.\n'
             'Чтобы я мог помогать вам с модерацией, мне нужны права админа.'
    )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=ADMINISTRATOR))
async def bot_restricted_admin_rights(event: types.ChatMemberUpdated, bot: Bot):
    chat_member = event.new_chat_member
    if not chat_member.can_delete_messages:
        await bot.send_message(
            chat_id=event.chat.id,
            text='Вы ограничили мне права.\n'
                 'Чтобы я мог помогать вам с модерацией, мне нужны все права админа.'
        )
