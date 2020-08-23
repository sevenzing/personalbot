from aiogram import types
import datetime
import logging

from modules.common import constants
from modules.cleaning import messages
from modules.database.models import create_user_if_not_exists
from modules.common.utils import get_next_cleaning_day, ordinal, days_left, month_name

async def cmd_nextcleaning(message: types.Message):
    user = create_user_if_not_exists(message.chat.id)
    building_number = user.chosenbuilding
    message_to_send = ''
    if building_number == 0:
        message_to_send = messages.HAVE_NOT_BUILDING
    else:
        cleaning_date = get_next_cleaning_day(building_number)
        message_to_send = messages.NEXT_CLEANING % (
            ordinal(building_number),
            days_left(cleaning_date),
            ordinal(cleaning_date.day),
            month_name(cleaning_date),
            )
    
    await message.answer(message_to_send, parse_mode='Markdown')
