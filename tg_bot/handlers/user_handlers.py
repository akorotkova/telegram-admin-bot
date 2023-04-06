from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.filters import Command
from tg_bot.bot_responses import user_commands as text
from tg_bot.handlers.admin_handlers import imitation_db


router: Router = Router()


# хендлер для команды /start и /help
async def process_start_and_help_cmd(message: Message):
    await message.answer(text.START_AND_HELP_TEXT, parse_mode='HTML')


# хендлер для команды /command_admin_bot
async def process_command_admin_bot_cmd(message: Message):
    await message.answer(text.COMMAND_ADMIN_BOT_TEXT, parse_mode='HTML')


# хендлер для команды /about_admin_bot
async def process_about_admin_bot_cmd(message: Message):
    await message.reply(text.ABOUT_ADMIN_BOT_TEXT)


# хендлер для команды !chat_rules
async def get_chat_rules(message: Message):
    # вытаскиваем из бд
    if imitation_db.get('link_message'):
        link_message = imitation_db['link_message']
        await message.reply(f"Правила чата:\n{link_message}", parse_mode='HTML')
    else:
        await message.reply(text.NO_CHAT_RULES)


# регистрируем все base хендлеры
def register_base_handlers(router: Router):
    router.message.register(process_start_and_help_cmd, Command(commands=['start', 'help']))
    router.message.register(process_command_admin_bot_cmd, Command(commands=['command_admin_bot']))
    router.message.register(process_about_admin_bot_cmd, Command(commands=['about_admin_bot']))
    router.message.register(get_chat_rules, Command('chat_rules', prefix='!'))
                        