from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
import logging

from modules.common import constants
from modules.common.utils import ordinal
from modules.cleaning import messages

def generate_choose_day_button() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    for number in range(1, 4, 2):
        keyboard.add(
            InlineKeyboardButton(
                f"{ordinal(number)}", 
                callback_data=f"setbuilding:{number}"
            ), 
                
            InlineKeyboardButton(
                f"{ordinal(number + 1)}", 
                callback_data=f"setbuilding:{number + 1}"
            ),
        )
    return keyboard


async def cmd_setbuilding(message: types.Message):
    await message.answer(
        messages.CHANGE_BUILDING_MESSAGE, 
        reply_markup=generate_choose_day_button()
        )

