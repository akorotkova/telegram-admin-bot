from aiogram import Router, Bot, types
from aiogram.filters import Command

from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.keyboards.admin_menu import get_setting_buttons


router = Router()
router.message.filter(IsAdmin())

imitation_db_msg = {}  # имитация бд для тегов 


@router.message(Command(commands=['current_settings']))
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
    

@router.message(Command(commands=['save_msg'], prefix='!'))
async def process_save_tag_cmd(message: types.Message):
    if message.chat.type == 'private':
        return await message.reply('Команда недоступна в приватном чате')
    if message.reply_to_message is not None:
        _, *tag = message.text.split()
        if tag:
            if len(tag) != 1:
                return await message.reply('Тег должен состоять из одного слова')
            chat_id = message.chat.id
            text_tag = tag[0]
            url_msg = message.reply_to_message.get_url()
            imitation_db_msg.setdefault(chat_id, {}).setdefault(text_tag, []).append(url_msg)
            return await message.reply(f'Сообщение сохранено с тегом <b>{text_tag}</b>', parse_mode='HTML')
        return await message.reply('Укажите тег для сообщения через пробел после команды')
    return await message.reply(text='Команда должна быть отправлена реплаем на сообщение')


@router.message(Command(commands=['del_tag'], prefix='!'))
async def process_del_tag_cmd(message: types.Message):
    if message.chat.type == 'private':
        return await message.reply('Команда недоступна в приватном чате')
    chat_id = message.chat.id 
    if chat_id not in imitation_db_msg:
        return await message.reply('В вашем чате пока что нет тегов')
    _, *tag = message.text.split(maxsplit=1)
    if not tag:
        return await message.reply('Укажите тег через пробел после команды')
    chat_id = message.chat.id
    text_tag = tag[0]
    try:
        del imitation_db_msg[chat_id][text_tag]
    except KeyError as e:
        return await message.reply(f'Тег <b>{text_tag}</b> не найден', parse_mode='HTML')
    return await message.reply(f'Тег <b>{text_tag}</b> удален', parse_mode='HTML')


@router.message(Command(commands=['del_tag_msg'], prefix='!'))
async def process_del_tag_msg_cmd(message: types.Message):
    if message.chat.type == 'private':
        return await message.reply('Команда недоступна в приватном чате')
    chat_id = message.chat.id 
    if chat_id not in imitation_db_msg:
        return await message.reply('В вашем чате пока что нет тегов')
    _, *tag_and_url = message.text.split(maxsplit=2)
    if len(tag_and_url) != 2:
        return await message.reply('Укажите тег и ссылку на сообщение в формате !del_tag_msg [tag] [url]')
    chat_id = message.chat.id
    text_tag, url_msg = tag_and_url
    try:
        imitation_db_msg[chat_id][text_tag].remove(url_msg)
    except KeyError as e:
        return await message.reply(f'Тег <b>{text_tag}</b> не найден', parse_mode='HTML')
    except ValueError as e:
        return await message.reply(f'Невалидная ссылка <b>{url_msg}</b>', parse_mode='HTML')
    await message.reply(f'Ссылка {url_msg} удалена из тега <b>{text_tag}</b>', parse_mode='HTML')
    