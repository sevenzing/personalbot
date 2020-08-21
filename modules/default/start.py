from aiogram import types

from modules.default import messages
from modules.database.models.User import create_user_if_not_exists

import logging

async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    user = create_user_if_not_exists(message.chat.id)
    if message.chat.id == message.from_user.id:
        user.update(username=message.from_user.username)
    await message.answer(messages.ON_CMD_START)
