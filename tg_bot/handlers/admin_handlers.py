from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from tg_bot.bot_responses import admin_commands as text
from tg_bot.keyboards.admin_menu import get_setting_buttons


router: Router = Router()

imitation_db = {}  # имитация бд


# хендлер для команды /current_settings
async def process_current_settings_cmd(message: Message):
    await message.reply(text.CURRENT_SETTINGS_TEXT, parse_mode='HTML')


# хендлер для команды /deleting_voice
async def process_deleting_voice_cmd(message: Message, bot: Bot):
    reply_markup = get_setting_buttons()
    await bot.send_message(chat_id=message.chat.id, 
                           text='Удаление голосовых сообщений:', 
                           reply_markup=reply_markup)


# хендлер для команды /deleting_video
async def process_deleting_video_cmd(message: Message, bot: Bot):
    reply_markup = get_setting_buttons()
    await bot.send_message(chat_id=message.chat.id, 
                           text='Удаление видеосообщений:', 
                           reply_markup=reply_markup)


# хендлер для команды /warning_ladder
async def process_warning_ladder_cmd(message: Message, bot: Bot):
    reply_markup = get_setting_buttons()
    await bot.send_message(chat_id=message.chat.id, 
                           text='Предупреждение на лесенку\n(лесенка не удаляется):', 
                           reply_markup=reply_markup)


# хендлер для команды /deleting_ladder
async def process_deleting_ladder_cmd(message: Message, bot: Bot):
    reply_markup = get_setting_buttons()
    await bot.send_message(chat_id=message.chat.id, 
                           text='Предупреждение на лесенку\n(лесенка удаляется):', 
                           reply_markup=reply_markup)


# хендлер для команды /setting_ladder
async def process_setting_ladder_cmd(message: Message):
    await message.reply(text.SETTING_LADDER_TEXT, parse_mode='HTML')


class ChatRules(StatesGroup):
    setting_rules_chat = State()

# хендлер для команды /add_chat_rules
async def process_add_chat_rules(message: Message, state: FSMContext):
    await message.reply('Отправь ссылку на сообщение с правилами чата.')
    await state.set_state(ChatRules.setting_rules_chat)

async def process_setting_rules_chat(message: Message, state: FSMContext):
    link_message = message.text  
    imitation_db['link_message'] = link_message  # пишем в базу
    await message.reply(text.ADD_CHAT_RULES_TEXT, parse_mode='HTML')
    await state.clear()

async def process_setting_rules_chat_incorrectly(message: Message):
    await message.reply(text='Неверный формат, нужно отправить ссылку на сообщение с правилами.')

    
# регистрируем все admin хендлеры
def register_admin_handlers(router: Router):
    router.message.register(process_current_settings_cmd, Command(commands=['current_settings']))
    router.message.register(process_deleting_voice_cmd, Command(commands=['deleting_voice']))
    router.message.register(process_deleting_video_cmd, Command(commands=['deleting_video']))
    router.message.register(process_warning_ladder_cmd, Command(commands=['warning_ladder']))
    router.message.register(process_deleting_ladder_cmd, Command(commands=['deleting_ladder']))
    router.message.register(process_setting_ladder_cmd, Command(commands=['setting_ladder']))
    router.message.register(process_add_chat_rules, Command('add_chat_rules'))
    router.message.register(process_setting_rules_chat, ChatRules.setting_rules_chat, F.text.regexp(r'\b(http|https):\/\/'))
    router.message.register(process_setting_rules_chat_incorrectly, ChatRules.setting_rules_chat)
    