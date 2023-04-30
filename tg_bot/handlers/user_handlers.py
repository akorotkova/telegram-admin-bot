from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from tg_bot.bot_responses import user_commands as text
from tg_bot.handlers.admin_handlers import imitation_db


router: Router = Router()


@router.message(Command(commands=['start', 'help']))
async def process_start_and_help_cmd(message: Message):
    await message.answer(text.START_AND_HELP_TEXT, parse_mode='HTML')


@router.message(Command(commands=['command']))
async def process_command_cmd(message: Message):
    await message.answer(text.COMMAND_ADMIN_BOT_TEXT, parse_mode='HTML')


@router.message(Command(commands=['about']))
async def process_about_cmd(message: Message):
    await message.reply(text.ABOUT_ADMIN_BOT_TEXT)


@router.message(Command('chat_rules', prefix='!'))
async def get_chat_rules(message: Message):
    # вытаскиваем из бд
    if imitation_db.get('link_message'):
        link_message = imitation_db['link_message']
        await message.reply(f"Правила чата:\n{link_message}", parse_mode='HTML')
    else:
        await message.reply(text.NO_CHAT_RULES)
