from aiogram import Router, types
from aiogram.filters import Command

from tg_bot.bot_responses.command_cmd_text import COMMAND_CMD_TEXT
from tg_bot.handlers.chat_rules import imitation_db
from tg_bot.utils.chat_type import check_chat_is_private
from tg_bot.utils.tag import check_tag_in_chat, imitation_db_msg


router: Router = Router()


@router.message(Command(commands=['start', 'help']))
async def process_start_and_help_cmd(message: types.Message):
    await message.reply(
        text='Привет. Я - бот для помощи с модерацией чата.\n'
             '<b>Добавь меня в группу и сделай админом.</b>\n\n'
             '/command - справка о моих командах.', 
        parse_mode='HTML'
    )


@router.message(Command(commands=['command']))
async def process_command_cmd(message: types.Message):
    await message.reply(text=COMMAND_CMD_TEXT, parse_mode='HTML')


@router.message(Command('chat_rules', prefix='!'))
@check_chat_is_private
async def get_chat_rules(message: types.Message):
    link_chat_rules: str | None = imitation_db.get(message.chat.id)  # TODO вытаскиваем из бд
    if link_chat_rules is None:
        return await message.reply(
            text='Правила чата не добавлены. Для добавления правил '
                 'используйте команду /add_chat_rules (доступна только админам)'
        )
    await message.reply(text=f'Правила чата:\n{link_chat_rules}')


@router.message(Command('get_msg', prefix='!'))
@check_chat_is_private
async def get_msg_tag(message: types.Message):
    _, *tag = message.text.split(maxsplit=1)
    if not tag:
        return await message.reply(text='Укажите тег через пробел после команды')
    text_tag = tag[0]
    try:
        tag_urls = '\n'.join(imitation_db_msg[message.chat.id][text_tag])
        await message.reply(
            text=f'Сообщения по тегу <b>{text_tag}</b>:\n{tag_urls}', 
            parse_mode='HTML'
        )
    except KeyError as e:
        await message.reply(
            text='Такого тега пока нет. Чтобы добавить тег, '
                 'используйте команду <code>!save_msg</code>', 
            parse_mode='HTML'
        )
    

@router.message(Command('get_list_msg', prefix='!'))
@check_tag_in_chat
@check_chat_is_private
async def get_list_tags(message: types.Message):
    all_tags = []
    for tag, tag_urls in imitation_db_msg[message.chat.id].items():
        all_tags.append(f"<b>{tag}</b>:\n{', '.join(tag_urls)}\n")
    all_tags = '\n'.join(all_tags)
    await message.reply(text=f'Все теги чата:\n{all_tags}', parse_mode='HTML')
