import logging
import datetime
import pytz
import math
import requests
import asyncio

from modules.common import constants

def get_current_building(date: datetime.datetime) -> int:
    '''
    Main function of schedule. Logic of the function
    affects on logic of notification
    Return number of current building, -1 otherwise
    '''
    
    _, week_number, day_number = date.isocalendar()
    if day_number not in [1, 4]:
        return -1
    if day_number == 1:
        return 1 if not (week_number % 2) else 2
    elif day_number == 4:
        return 4 if not (week_number % 2) else 3

def get_next_cleaning_day(building_number: int) -> datetime.datetime:
    '''
    Return next cleaning date for the given building
    '''
    current_date = get_now()
    for _ in range(365):
        if get_current_building(current_date) != building_number:
            current_date = get_next_day(current_date)
        else:
            return current_date

def days_left(date: datetime.datetime):
    '''
    Return how many days left before the date
    '''
    return (date - get_now()).days + 1

def month_name(date: datetime.datetime):
    '''
    Return month of the date
    '''
    return date.strftime("%B")

def get_now() -> datetime.datetime:
    return datetime.datetime.now(
        pytz.timezone(constants.TIME_ZONE)
        )

def convert_date_to_current_timezone(date) -> datetime.datetime:
    '''
    Return the date with default timezone
    '''
    return date.astimezone(pytz.timezone(constants.TIME_ZONE))
    
def get_next_day(date: datetime) -> datetime.datetime:
    '''
    Return date of next day of the given date
    '''
    date = convert_date_to_current_timezone(date)
    n = date + datetime.timedelta(days=1)
    return datetime.datetime(n.year, n.month, n.day, tzinfo=pytz.timezone(constants.TIME_ZONE))

def ordinal(n: int) -> str:
    """
    Return the ordinal number of the number
    1 -> 1st
    3 -> 3rd
    5 -> 5th
    """
    return "%d%s" % (n, "tsnrhtdd"[(math.floor(n / 10) % 10 != 1) * (n % 10 < 4) * n % 10::4])


def parse_commad(text: str):
    '''
    Takes text of telegram message, 
    parses it into command and arguments 
    
    Return tuple: (command, [arguments,])
    /add kek, lol, kek -> ('/add', ['kek', 'lol', 'kek'])
    '''
    command, _, raw_args = text.partition(' ')
    sep = ',' if ',' in raw_args else '\n' if '\n' in raw_args else ' '
    args = list(
        map(lambda x: x.strip(), 
            filter(lambda x: x != '', raw_args.split(sep))
        )
    )
    return (command, args)

def get_file_by_url(url):
    return requests.get(url).content



async def forever_run(function, interval, *args, **kwargs):
    while 1:
        logging.debug(f"Run function {function.__name__}")
        await function(*args, **kwargs)
        await asyncio.sleep(interval)


