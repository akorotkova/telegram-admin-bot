from aiogram import Router, Bot, types
from aiogram.filters import Command

from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.keyboards.admin_menu import get_setting_buttons
from tg_bot.utils.chat_type import check_chat_is_private


router = Router()
router.message.filter(IsAdmin())


@router.message(Command(commands=['current_settings']))
@check_chat_is_private
async def process_current_settings_cmd(message: types.Message):
    await message.reply(
        text='<b>Текущие настройки</b>:\n...', 
        parse_mode='HTML'
    )


@router.message(Command(commands=['deleting_voice']))
async def process_deleting_voice_cmd(message: types.Message, bot: Bot):
    reply_markup = get_setting_buttons()
    await bot.send_message(
        chat_id=message.chat.id,
        text='Удаление голосовых сообщений:', 
        reply_markup=reply_markup
    ) 


@router.message(Command(commands=['deleting_video']))
async def process_deleting_video_cmd(message: types.Message, bot: Bot):
    reply_markup = get_setting_buttons()
    await bot.send_message(
        chat_id=message.chat.id, 
        text='Удаление видеосообщений:', 
        reply_markup=reply_markup
    ) 
    
    
@router.message(Command(commands=['deleting_file']))
async def process_deleting_file_cmd(message: types.Message, bot: Bot):
    reply_markup = get_setting_buttons()
    await bot.send_message(
        chat_id=message.chat.id, 
        text='Удаление файлов неразрешенного формата:', 
        reply_markup=reply_markup    
    )
    