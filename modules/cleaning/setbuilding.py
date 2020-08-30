from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging

from modules.common import constants
from modules.common.utils import ordinal
from modules.cleaning import messages
from modules.database.models import create_user_if_not_exists

def generate_choose_day_button() -> InlineKeyboardMarkup:
    '''
    Return buttons for choosing building message in this way:
    [  1st  ] [  2nd  ]
    [  3rd  ] [  4th  ]
    [      CLOSE      ]
    '''
    keyboard = InlineKeyboardMarkup(row_width=2)
    for start_number in [1, 3]:
        row = []
        for number in range(start_number, start_number + 2):
            row.append(
                InlineKeyboardButton(
                    text=f"{ordinal(number)}", 
                    callback_data=':'.join([constants.INLINE_PREFIX_SETBUILDING, constants.INLINE_INFIX_CHANGE, str(number)])
                ))
        keyboard.add(*row)

    keyboard.add(InlineKeyboardButton(
        text=messages.BUTTON_EXIT,
        callback_data=':'.join([constants.INLINE_PREFIX_SETBUILDING, constants.INLINE_INFIX_CLOSE, '0'])
    ))
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
    
    _, command, building = query.data.split(':')
    logging.debug(f"Got query {query.data}")
    if command == constants.INLINE_INFIX_CHANGE:
        building = int(building)
        user = create_user_if_not_exists(query.message.chat.id)
        user.update(chosenbuilding=building)

        await query.answer(messages.QUERY_SELECTED % ordinal(user.chosenbuilding))
    elif command == constants.INLINE_INFIX_CLOSE:
        await query.message.delete()
        return
