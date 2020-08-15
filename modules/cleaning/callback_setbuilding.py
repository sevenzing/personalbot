from aiogram import types

from modules.cleaning import messages
from modules.common import constants
from modules.common.utils import ordinal
from modules.common.database import ListModel, UserModel

import logging

async def answer_callback_setbuilding_handler(query: types.CallbackQuery):
    _, building = query.data.split(':')
    building = int(building)

    user = UserModel(query.message)
    user.update(chosenbuilding=building)

    await query.answer(messages.QUERY_SELECTED % ordinal(user.get('chosenbuilding')))