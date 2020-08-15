import logging
import datetime
import pytz
import math

from modules.common import constants


def get_now() -> datetime.datetime:
    return datetime.datetime.now(
        pytz.timezone(constants.TIME_ZONE)
        )

def get_date_from_string(string: str) -> datetime.datetime:
    return eval(string.replace(
        f"<StaticTzInfo '{constants.TIME_ZONE}'>", 
        f"pytz.timezone('{constants.TIME_ZONE}')"
        ))

def ordinal(n: int) -> str:
    """
    Returns the ordinal number of the number
    1 -> 1st
    3 -> 3rd
    5 -> 5th
    """
    return "%d%s" % (n, "tsnrhtdd"[(math.floor(n / 10) % 10 != 1) * (n % 10 < 4) * n % 10::4])


#%%
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



# %%
