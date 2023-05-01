from aiogram import Router, F
from aiogram.types import Message
from aiogram.methods.delete_message import DeleteMessage


router: Router = Router()


@router.message(F.voice)
async def process_warning_voice(message: Message):
    await message.reply(text='Пожалуйста, не отправляйте голосовые сообщения в чат.')
    return DeleteMessage(chat_id=message.chat.id, message_id=message.message_id)


@router.message(F.video)
async def process_warning_voice(message: Message):
    await message.reply(text='Пожалуйста, не отправляйте видеосообщения в чат.')
    return DeleteMessage(chat_id=message.chat.id, message_id=message.message_id)
