from functools import wraps

from aiogram import Bot, Router, F
from aiogram.types import Message, ContentType
from aiogram.methods.delete_message import DeleteMessage


router: Router = Router()


def check_bot_permissions(handler):
    @wraps(handler)
    async def inner(message: Message, bot: Bot):
        if message.chat.type == 'private':
            return await handler(message, bot)
        bot_info = await bot.get_chat_member(message.chat.id, bot.id)
        if 'включена настройка' and bot_info.can_delete_messages:
            return await handler(message, bot)
        if 'включена настройка' and not bot_info.can_delete_messages:
            return await bot.send_message(
                chat_id=message.chat.id,
                text=f'Вы включили настройку автоудаления, но у меня нет прав на это. '
                     f'Проверьте, являюсь ли я админом чата с возможностью удалять сообщения.'
                )
    return inner
  

@router.message(F.content_type == ContentType.VOICE)
@check_bot_permissions
async def process_warning_voice(message: Message, bot: Bot):
    await message.reply(text='Пожалуйста, не отправляйте голосовые сообщения в чат.')
    return DeleteMessage(chat_id=message.chat.id, message_id=message.message_id)
    

@router.message(F.content_type.in_({ContentType.VIDEO, ContentType.VIDEO_NOTE}))
@check_bot_permissions
async def process_warning_voice(message: Message, bot: Bot):
    await message.reply(text='Пожалуйста, не отправляйте видеосообщения в чат.')
    return DeleteMessage(chat_id=message.chat.id, message_id=message.message_id)


@router.message(F.content_type.in_({ContentType.DOCUMENT}))
@check_bot_permissions
async def process_warning_document(message: Message, bot: Bot):
        _allowed_formats_file = {'pdf', 'txt', 'conf', 'json', 'xml', 'yml', 'csv', 'png', 'jpg', 'jpeg'}
        file_format = message.document.file_name.split('.')[-1]
        if file_format not in _allowed_formats_file:
            await message.reply(text='Запрещено отправлять в чат файл с данным расширением.')
            return DeleteMessage(chat_id=message.chat.id, message_id=message.message_id)
        