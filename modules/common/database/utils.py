from redis import Redis
from json import dumps, loads

from . import database
from misc import logger

def set_if_not_exists(key, value) -> bool:
    '''
    Set value to key only if key doesnt exist

    Returns true if changed something, false overwise
    '''
    return __set(key, value, nx=True)

def set_if_exists(key, value) -> bool:
    '''
    Set value to ket only if ket exists

    Returns true if changed something, false overwise
    '''
    return __set(key, value, xx=True)

def __set(key, value, **kwargs) -> bool:
    '''
    Executes set() method for 
    redis database with agruments

    Returns true if changed something, false overwise
    '''
    if isinstance(value, dict):
        value = dumps(value)

    if database.set(key, value, **kwargs):
        logger.debug(f'Set key {key} to value {value}')
        return True
    else:
        return False

def get_if_exists(key) -> dict:
    '''
    Returns dict for the key in redis database
    '''
    value = database.get(key)

    if value:
        return loads(value.decode()) 
    else:
        return None
