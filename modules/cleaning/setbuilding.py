from aiogram import types
import logging

from modules.common.utils import generate_choose_day_button
from modules.cleaning import messages


async def cmd_setbuilding(message: types.Message):
    await message.answer(
        messages.CHANGE_BUILDING_MESSAGE, 
        reply_markup=generate_choose_day_button()
        )

