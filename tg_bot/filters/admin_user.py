from dataclasses import dataclass

from aiogram import Bot, types
from aiogram.filters import BaseFilter


@dataclass
class IsAdmin(BaseFilter):
    '''фильтрация админов, пока в таком виде, дальше буду получать админов 1 раз'''

    def get_user_id(self, message: types.Message, bot: Bot) -> int:
        return message.from_user.id
    
    async def _get_chat_member(self, message: types.Message, bot: Bot):
        admins = await bot.get_chat_administrators(message.chat.id)
        target_user_id = self.get_user_id(message, bot)
        try:
            chat_member = next(filter(lambda member: member.user.id == target_user_id, admins))
        except StopIteration:
            return False
        return chat_member
    
    async def __call__(self, message: types.Message, bot: Bot):
        chat_member = await self._get_chat_member(message, bot)
        if not chat_member:
            return False
        if chat_member.status == "creator" or chat_member.status == "administrator":
            return chat_member
