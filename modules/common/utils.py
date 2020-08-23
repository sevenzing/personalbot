import logging
import datetime
import pytz
import math

from modules.common import constants
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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

def generate_choose_day_button() -> InlineKeyboardMarkup:
    '''
    Return buttons for choosing building message
    '''
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

def get_next_cleaning_day(building_number: int) -> datetime.datetime:
    current_date = get_now()
    while get_current_building(current_date) != building_number:
         current_date = get_next_day(current_date)
    return current_date

def days_left(date: datetime.datetime):
    return (date - get_now()).days

def month_name(date: datetime.datetime):
    return date.strftime("%B")

def get_now() -> datetime.datetime:
    return datetime.datetime.now(
        pytz.timezone(constants.TIME_ZONE)
        )

def convert_date_to_current_timezone(date):
    return date.astimezone(pytz.timezone(constants.TIME_ZONE))

def get_next_day(date: datetime):
    n = date + datetime.timedelta(days=1)
    return datetime.datetime(n.year, n.month, n.day, tzinfo=pytz.timezone(constants.TIME_ZONE))

def ordinal(n: int) -> str:
    """
    Returns the ordinal number of the number
    1 -> 1st
    3 -> 3rd
    5 -> 5th
    """
    return "%d%s" % (n, "tsnrhtdd"[(math.floor(n / 10) % 10 != 1) * (n % 10 < 4) * n % 10::4])


def parse_commad(text: str):
    '''
    Takes text of telegram message, 
    parses it into command and arguments 
    
    Returns tuple: (command, [arguments,])
    '''
    command, _, raw_args = text.partition(' ')
    sep = ',' if ',' in raw_args else '\n' if '\n' in raw_args else ' '
    args = list(
        map(lambda x: x.strip(), 
            filter(lambda x: x != '', raw_args.split(sep))
        )
    )
    return (command, args)
