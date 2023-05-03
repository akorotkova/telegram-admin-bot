from aiogram import Bot, Router, F
from aiogram.types import Message, ContentType
from aiogram.methods.delete_message import DeleteMessage


router: Router = Router()


@router.message(F.content_type == ContentType.VOICE)
async def process_warning_voice(message: Message, bot: Bot):
    # что-то делаем, если бот не админ
    await message.reply(text='Пожалуйста, не отправляйте голосовые сообщения в чат.')
    return DeleteMessage(chat_id=message.chat.id, message_id=message.message_id)


@router.message(F.content_type.in_({ContentType.VIDEO, ContentType.VIDEO_NOTE}))
async def process_warning_voice(message: Message, bot: Bot):
    # что-то делаем, если бот не админ
    await message.reply(text='Пожалуйста, не отправляйте видеосообщения в чат.')
    return DeleteMessage(chat_id=message.chat.id, message_id=message.message_id)


@router.message(F.content_type.in_({ContentType.DOCUMENT}))
async def process_warning_document(message: Message, bot: Bot):
    # что-то делаем, если бот не админ
    _allowed_formats_file = {'pdf', 'txt', 'conf', 'json', 'xml', 'yml', 'csv', 'png', 'jpg', 'jpeg'}
    file_format = message.document.file_name.split('.')[-1]
    if file_format not in _allowed_formats_file:
        await message.reply(text='Запрещено отправлять в чат файл с данным расширением.')
        return DeleteMessage(chat_id=message.chat.id, message_id=message.message_id)
        