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
                 f'{chats_variants[event.chat.type]} "{event.chat.title}" '
                 f'как обычного участника.\n'
                 f'Чтобы я мог помогать вам с модерацией чата, добавьте меня в админы.'
        )
    else:
        print('логирование этой ситуации')


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER >> ADMINISTRATOR))
async def bot_added_as_admin(event: ChatMemberUpdated, bot: Bot):
    chat_member = event.new_chat_member
    if not chat_member.can_delete_messages:
        await bot.send_message(
        chat_id=event.chat.id,
        text=f'Спасибо, что добавили меня '
             f'в администраторы, но мне нужны все права админа, '
             f'чтобы я мог помогать с модерацией!\n'
             f'Пожалуйста, добавьте мне право на удаление сообщений в чате.'
        )
    else:        
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
    else:
        await bot.send_message(
            chat_id=event.chat.id,
            text=f'Спасибо! Теперь я буду помогать вам с модерацией.\n'
                 f'Перейдите в настройки: /command'
        )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=ADMINISTRATOR >> MEMBER))
async def bot_added_as_admin(event: ChatMemberUpdated, bot: Bot):
    await bot.send_message(
        chat_id=event.chat.id,
        text=f'Вы удалили меня из администраторов чата.\n'
             f'Чтобы я мог помогать вам с модерацией, мне нужны права админа.'
    )
