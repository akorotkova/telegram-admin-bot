from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from tg_bot.bot_responses import user_commands as text
from tg_bot.handlers.admin_handlers import imitation_db, imitation_db_msg


router: Router = Router()


@router.message(Command(commands=['start', 'help']))
async def process_start_and_help_cmd(message: Message):
    await message.answer(text.START_AND_HELP_TEXT, parse_mode='HTML')


@router.message(Command(commands=['command']))
async def process_command_cmd(message: Message):
    await message.answer(text.COMMAND_ADMIN_BOT_TEXT, parse_mode='HTML')


# @router.message(Command(commands=['about']))
# async def process_about_cmd(message: Message):
#     await message.reply(text.ABOUT_ADMIN_BOT_TEXT)


@router.message(Command('chat_rules', prefix='!'))
async def get_chat_rules(message: Message):
    # вытаскиваем из бд
    if imitation_db.get('link_message'):
        link_message = imitation_db['link_message']
        await message.reply(f"Правила чата:\n{link_message}", parse_mode='HTML')
    else:
        await message.reply(text.NO_CHAT_RULES)


@router.message(Command('get_msg', prefix='!'))
async def get_msg_tag(message: Message):
    if message.chat.type == 'private':
        return await message.reply('Команда недоступна в приватном чате')
    _, *tag = message.text.split(maxsplit=1)
    if tag:
        chat_id = message.chat.id
        text_tag = tag[0]
        try:
            tag_urls = '\n'.join(imitation_db_msg[chat_id][text_tag])
            return message.reply(
                f'Сообщения по тегу <b>{text_tag}</b>:\n'
                f'{tag_urls}', 
                parse_mode='HTML'
            )
        except KeyError as e:
            return message.reply(
                'Такого тега пока нет. Чтобы добавить тег, '
                'используйте команду <code>!save_msg</code>', 
                parse_mode='HTML'
            )
    return await message.reply('Укажите тег через пробел после команды, '
                               'по которому хотите получить все ссылки на сообщения')


@router.message(Command('get_list_msg', prefix='!'))
async def get_list_tags(message: Message):
    if message.chat.type == 'private':
        return await message.reply('Команда недоступна в приватном чате')
    chat_id = message.chat.id 
    if chat_id not in imitation_db_msg:
        return await message.reply('В вашем чате пока что нет тегов')
    all_tags = []
    for tag, tag_urls in imitation_db_msg[chat_id].items():
        all_tags.append(f"<b>{tag}</b>:\n{', '.join(tag_urls)}\n")
    result = '\n'.join(all_tags)
    return await message.reply(
        f'Все теги чата:\n{result}',
        parse_mode='HTML' 
    )
