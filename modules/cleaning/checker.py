import asyncio
from aiogram import Dispatcher
import logging
import datetime
from itertools import chain, cycle

from modules.common.constants import BEFORE_CLEANING, ON_CLEANING
from modules.database.models import UserModel
from modules.cleaning import messages
from modules.common.utils import (
    get_now, 
    convert_date_to_current_timezone, 
    get_next_day, 
    get_current_building,
    )


async def check_time(dp: Dispatcher):
    '''
    Check whether the current day is a cleaning day
    for all user with checknotice=True
    '''
    now = get_now()
    _, week_number, day_number = now.isocalendar()
    current_building = get_current_building(now)
    next_day_building = get_current_building(get_next_day(now))
    
    users_today = UserModel.find({'checknotice': True, 'chosenbuilding': current_building})
    users_next_day = UserModel.find({'checknotice': True, 'chosenbuilding': next_day_building})
    for user, on_day in chain(
        zip(users_next_day, cycle([BEFORE_CLEANING])),
        zip(users_today, cycle([ON_CLEANING])),
        ):
        '''
        users_today = [a1, a2, a3]
        usets_next_day [b1, b2, b3]
        iteration: (a1, 'on_cleaning') , (a2, 'on_cleaning'), (a3, 'on_cleaning'), (b1, 'before_cleaning'), ...
        '''
        lastnotice = user.lastnotice[on_day]
        lastnotice = convert_date_to_current_timezone(lastnotice)
        notice_hour = user.notification[on_day]
        logging.debug(f"Notice hour on day: {on_day} for user {user.chat_id} is {notice_hour}")
        
        if notice_hour == None:
            continue
        logging.debug(f"last notice was at {lastnotice} ({lastnotice.tzname()}). Current hour: {now.hour}")
        
        if now >= lastnotice and now.hour >= notice_hour:
            logging.debug(f"Send notification for {user.chat_id} with username {user.username}")
            await dp.bot.send_message(
                user.chat_id, 
                messages.CLEANING_NOTIFICATION % 
                    ('today' if on_day == ON_CLEANING else 'tomorrow')
                )
            
            user.lastnotice[on_day] = get_next_day(now)
            user.update(lastnotice=user.lastnotice)
        else:
            logging.debug(f"Skip notice for {user.chat_id}")

    
