from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.utils.chat_type import check_chat_is_private


router = Router()
router.message.filter(IsAdmin())

imitation_db = {}  # имитация бд для правил чата


class ChatRules(StatesGroup):
    setting_chat_rules = State()


@router.message(Command('add_chat_rules'))
@check_chat_is_private
async def process_add_chat_rules(message: types.Message, state: FSMContext):
    await message.reply('Отправь ссылку на сообщение с правилами чата.')
    await state.set_state(ChatRules.setting_chat_rules)


@router.message(ChatRules.setting_chat_rules, F.text.regexp(r'\b(http|https):\/\/'))
async def process_setting_chat_rules(message: types.Message, state: FSMContext):
    link_message = message.text  
    imitation_db[message.chat.id] = link_message # пишем в базу
    await message.reply(
        text='Отлично! Теперь это сообщение будет отображаться по команде '
             '<code>!chat_rules</code>, доступной всем участникам чата.',
        parse_mode='HTML'
    )
    await state.clear()


@router.message(ChatRules.setting_chat_rules)
async def process_setting_chat_rules_incorrectly(message: types.Message):
    await message.reply(text='Неверный формат, нужно отправить ссылку на сообщение с правилами.')
    