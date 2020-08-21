from aiogram import types

from modules.default import messages
from modules.database.models.User import get_user

import logging

async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    user = get_user(chat_id=message.chat.id, username=message.from_user.username)
    await message.answer(messages.ON_CMD_START)
