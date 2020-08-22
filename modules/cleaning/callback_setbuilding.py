from aiogram import types

from modules.cleaning import messages
from modules.common import constants
from modules.common.utils import ordinal
from modules.database.models import create_user_if_not_exists

import logging

async def answer_callback_setbuilding_handler(query: types.CallbackQuery):
    '''
    Answer on query from choosing building message
    '''
    
    _, building = query.data.split(':')
    building = int(building)
    
    logging.debug(f"Got query to setbuilding to {building}")

    user = create_user_if_not_exists(query.message.chat.id)
    user.update(chosenbuilding=building)

    await query.answer(messages.QUERY_SELECTED % ordinal(user.chosenbuilding))