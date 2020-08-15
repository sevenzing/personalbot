import asyncio
from aiogram import Dispatcher
import logging
import datetime

from modules.common.database import UserModel
from modules.common.database.User import find_users
from modules.common.utils import get_now, get_date_from_string

def get_current_building(date: datetime.datetime) -> int:
    '''
    Returns number of current building 
    '''
    # TODO: remove this comment
    return 1

    _, week_number, day_number = date.isocalendar()
    if day_number not in [1, 4]:
        return
    if day_number == 1:
        return 1 if not (week_number % 2) else 2
    elif day_number == 4:
        return 4 if not (week_number % 2) else 3

async def check_time(dp: Dispatcher):
    # TODO: check time

    now = get_now()
    _, week_number, day_number = now.isocalendar()
    current_building = get_current_building(now)

    for user in find_users(
        checknotice=True, 
        chosenbuilding=current_building
        ):
        lastnotice = get_date_from_string(user.get('lastnotice'))
        logging.debug(f"last notice was at {lastnotice}")
        if now >= lastnotice and now.hour >= user.get('noticehour'):
            logging.debug(f"Make notice for {user.chat_id}")
            # TODO: make notice
            
            pass
        else:
            logging.debug(f"Skip notice for {user.chat_id}")

    
