from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging

from modules.common import constants
from modules.common.utils import ordinal
from modules.cleaning import messages
from modules.database.models import create_user_if_not_exists

def generate_choose_day_button() -> InlineKeyboardMarkup:
    '''
    Return buttons for choosing building message
    '''
    keyboard = InlineKeyboardMarkup(row_width=2)
    for number in range(1, 4, 2):
        keyboard.add(
            InlineKeyboardButton(
                f"{ordinal(number)}", 
                callback_data=f"{constants.INLINE_PREFIX_SETBUILDING}:{number}"
            ), 
                
            InlineKeyboardButton(
                f"{ordinal(number + 1)}", 
                callback_data=f"{constants.INLINE_PREFIX_SETBUILDING}:{number + 1}"
            ),
        )
    return keyboard




async def cmd_setbuilding(message: types.Message):
    await message.answer(
        messages.CHANGE_BUILDING_MESSAGE, 
        reply_markup=generate_choose_day_button()
        )

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
