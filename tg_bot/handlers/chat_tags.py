from aiogram import Router, types
from aiogram.filters import Command

from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.utils.chat_type import check_chat_is_private


router = Router()
router.message.filter(IsAdmin())

imitation_db_msg = {}  # имитация бд для тегов 
        

@router.message(Command(commands=['save_msg'], prefix='!'))
@check_chat_is_private
async def process_save_msg(message: types.Message):
    if message.reply_to_message is not None:
        _, *tag = message.text.split()

        if tag:
            if len(tag) == 1:
                text_tag = tag[0]
                url_msg = message.reply_to_message.get_url()
                imitation_db_msg.setdefault(message.chat.id, {}).setdefault(text_tag, []).append(url_msg)
                return await message.reply(text=f'Сообщение сохранено с тегом <b>{text_tag}</b>', parse_mode='HTML')
            return await message.reply(text='Тег должен состоять из одного слова')       
        return await message.reply(text='Укажите тег через пробел после команды')
    
    await message.reply(text='Команда должна быть отправлена реплаем на сообщение')


@router.message(Command(commands=['del_tag'], prefix='!'))
@check_chat_is_private
async def process_del_tag(message: types.Message):
    chat_id = message.chat.id 
    if chat_id not in imitation_db_msg:
        return await message.reply(text='В вашем чате пока что нет тегов')
    
    _, *tag = message.text.split(maxsplit=1)
    if tag:
        text_tag = tag[0]
        try:
            del imitation_db_msg[chat_id][text_tag]
        except KeyError as e:
            return await message.reply(text=f'Тег <b>{text_tag}</b> не найден', parse_mode='HTML')
        return await message.reply(text=f'Тег <b>{text_tag}</b> удален', parse_mode='HTML')
    
    await message.reply(text='Укажите тег через пробел после команды')
    

@router.message(Command(commands=['del_tag_msg'], prefix='!'))
@check_chat_is_private
async def process_del_tag_msg(message: types.Message):
    chat_id = message.chat.id 
    if chat_id not in imitation_db_msg:
        return await message.reply(text='В вашем чате пока что нет тегов')
    
    _, *tag_and_url = message.text.split(maxsplit=2)
    if tag_and_url:
        if len(tag_and_url) == 2:
            text_tag, url_msg = tag_and_url
            try:
                imitation_db_msg[chat_id][text_tag].remove(url_msg)
            except KeyError as e:
                return await message.reply(text=f'Тег <b>{text_tag}</b> не найден', parse_mode='HTML')
            except ValueError as e:
                return await message.reply(text=f'Невалидная ссылка <b>{url_msg}</b>', parse_mode='HTML')
            return await message.reply(text=f'Ссылка {url_msg} удалена из тега <b>{text_tag}</b>', parse_mode='HTML')
        
    await message.reply(text='Укажите тег и ссылку на сообщение в формате !del_tag_msg [tag] [url]')
    