from aiogram import types

from modules.default import messages
from modules.database.models.User import create_user_if_not_exists, find_user
from modules.cleaning.setbuilding import cmd_setbuilding
from modules.cleaning.setreminder import cmd_setreminder

import logging

async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """

    first_time = not find_user({'chat_id': message.chat.id})
    user = create_user_if_not_exists(message.chat.id)
    if message.from_user.username:
        user.update(username=(message.from_user.username or 'None'))
    await message.answer(messages.ON_CMD_START)
    if first_time:
        await cmd_setbuilding(message)
        await cmd_setreminder(message)
