import asyncio
from aiogram import Dispatcher
import logging
import datetime

from modules.database.models import UserModel
from modules.common.utils import get_now, convert_date_to_current_timezone, get_next_day
from modules.cleaning import messages

def get_current_building(date: datetime.datetime) -> int:
    '''
    Returns number of current building 
    '''

    _, week_number, day_number = date.isocalendar()
    if day_number not in [1, 4]:
        return
    if day_number == 1:
        return 1 if not (week_number % 2) else 2
    elif day_number == 4:
        return 4 if not (week_number % 2) else 3

async def check_time(dp: Dispatcher):
    '''
    Check whether the current day is a cleaning day
    for all user with checknotice=True
    '''
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
            logging.debug(f"Send notification for {user.chat_id} with username {user.username}")
            await dp.bot.send_message(user.chat_id, messages.CLEANING_NOTIFICATION % 'today')
            user.update(lastnotice=get_next_day(now))
        else:
            logging.debug(f"Skip notice for {user.chat_id}")

    
