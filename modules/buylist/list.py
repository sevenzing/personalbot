from aiogram import types
import logging

from modules.database.models.User import User, get_user
from modules.database.models.List import List
from modules.common import constants
from modules.buylist import messages


async def cmd_list(message: types.Message, *args, **kwargs):
    user = get_user(message.chat.id)
    _list = user.get_buy_list()
    await message.answer(
        messages.ON_CMD_LIST,
        reply_markup=_list.generate_buttons_for_list(),
        parse_mode='Markdown',
    )


