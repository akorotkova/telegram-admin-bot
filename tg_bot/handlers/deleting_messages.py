from functools import wraps

from aiogram import Bot, Router, types, F
from aiogram.methods.delete_message import DeleteMessage


router = Router()

_allowed_formats_file = {'pdf', 'txt', 'conf', 'json', 'xml', 'yml', 'csv', 'png', 'jpg', 'jpeg'}


def check_bot_permission_to_delete(handler):
    @wraps(handler)
    async def inner(message: types.Message, bot: Bot):
        if message.chat.type == 'private':
            return await handler(message, bot)

        bot_info = await bot.get_chat_member(message.chat.id, bot.id)

        permission_to_delete: bool | None = bot_info.can_delete_messages
        config_value: bool = True  # TODO берем из базы значение настройки

        if config_value and not permission_to_delete:
            return await bot.send_message(
                chat_id=message.chat.id,
                text='Вы включили настройку автоудаления, но у меня нет прав на это. '
                     'Проверьте, являюсь ли я админом чата с возможностью удалять сообщения.'
            )
        if config_value and permission_to_delete:
            return await handler(message, bot) 
        
    return inner


@router.message(F.content_type == types.ContentType.VOICE)
@check_bot_permission_to_delete
async def process_deleting_voice(message: types.Message, bot: Bot):
    await message.reply(text='Пожалуйста, не отправляйте голосовые сообщения в чат.')
    return DeleteMessage(chat_id=message.chat.id, message_id=message.message_id)
    

@router.message(F.content_type.in_({types.ContentType.VIDEO, types.ContentType.VIDEO_NOTE}))
@check_bot_permission_to_delete
async def process_deleting_video(message: types.Message, bot: Bot):
    await message.reply(text='Пожалуйста, не отправляйте видеосообщения в чат.')
    return DeleteMessage(chat_id=message.chat.id,message_id=message.message_id)


@router.message(F.content_type == types.ContentType.DOCUMENT)
@check_bot_permission_to_delete
async def process_deleting_document(message: types.Message, bot: Bot):
    format_file = message.document.file_name.split('.')[-1]
    if format_file not in _allowed_formats_file:
        await message.reply(text='Запрещено отправлять в чат файл с данным расширением.')
        return DeleteMessage(chat_id=message.chat.id, message_id=message.message_id)
        