import asyncio
from aiogram import Dispatcher
import logging
import datetime

from modules.database.models import UserModel
from modules.common.utils import get_now, convert_date_to_current_timezone, get_next_day

def get_current_building(date: datetime.datetime) -> int:
    '''
    Returns number of current building 
    '''
    # TODO: remove this line
    return 1

    _, week_number, day_number = date.isocalendar()
    if day_number not in [1, 4]:
        return
    if day_number == 1:
        return 1 if not (week_number % 2) else 2
    elif day_number == 4:
        return 4 if not (week_number % 2) else 3

async def check_time(dp: Dispatcher):
    now = get_now()
    _, week_number, day_number = now.isocalendar()
    current_building = get_current_building(now)
    for user in UserModel.find({
        'checknotice': True, 
        'chosenbuilding': current_building
        }):
        lastnotice = user.lastnotice
        lastnotice = convert_date_to_current_timezone(lastnotice)
        logging.debug(f"last notice was at {lastnotice} ({lastnotice.tzname()}). Current hour: {now.hour}")
        if now >= lastnotice and now.hour >= user['noticehour']:
            logging.debug(f"Make notice for {user.chat_id}")
            
            # TODO: Message variable
            await dp.bot.send_message(user.chat_id, 'Notice!')
            user.update(lastnotice=get_next_day(now))
            logging.debug(f"Made notice for {user.chat_id}")
        else:
            logging.debug(f"Skip notice for {user.chat_id}")

    
