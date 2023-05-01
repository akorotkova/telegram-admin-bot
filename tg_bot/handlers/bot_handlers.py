from aiogram import Bot, Router, F
from aiogram.types import Message, ContentType
from aiogram.methods.delete_message import DeleteMessage


router: Router = Router()


@router.message(F.voice)
async def process_warning_voice(message: Message, bot: Bot):
    # что-то делаем, если бот не админ
    await message.reply(text='Пожалуйста, не отправляйте голосовые сообщения в чат.')
    return DeleteMessage(chat_id=message.chat.id, message_id=message.message_id)


@router.message(F.content_type.in_({ContentType.VIDEO, ContentType.VIDEO_NOTE}))
async def process_warning_voice(message: Message, bot: Bot):
    # что-то делаем, если бот не админ
    await message.reply(text='Пожалуйста, не отправляйте видеосообщения в чат.')
    return DeleteMessage(chat_id=message.chat.id, message_id=message.message_id)
