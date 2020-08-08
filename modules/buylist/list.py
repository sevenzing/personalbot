from aiogram import types
from aiogram.dispatcher import FSMContext

import logging

from modules.common.database.User import User
from modules.common.database.List import List

from misc import logger

async def cmd_list(message: types.Message, state: FSMContext, *args, **kwargs):
    user = User(message)
    _list = List(user)

    await message.answer(f"Your list: {_list.content()}")


