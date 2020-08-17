from aiogram import types
from aiogram.dispatcher import FSMContext
import logging


from modules.common.database import (
    ListModel, UserModel
)
from modules.common import constants
from modules.buylist import messages


async def cmd_list(message: types.Message, state: FSMContext, *args, **kwargs):
    user = UserModel(message)
    _list = ListModel(user)

    await message.answer(
        messages.ON_CMD_LIST,
        reply_markup=_list.generate_buttons_for_list(),
        parse_mode='Markdown',
    )


