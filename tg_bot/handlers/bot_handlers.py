from aiogram import Router, F
from aiogram.types import Message


router: Router = Router()


@router.message(F.voice)
async def process_warning_voice(message: Message):
    await message.reply(text='Пожалуйста, не отправляйте голосовые сообщения в чат.')
