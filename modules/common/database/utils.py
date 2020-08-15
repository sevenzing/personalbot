from redis import Redis
from json import dumps, loads
from typing import List, Dict
import logging

from . import database

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
        logging.debug(f'Set key {key} to value {value}')
        return True
    else:
        return False

def get_if_exists(key) -> Dict:
    '''
    Returns dict for the key in redis database
    '''
    value = database.get(key)

    if value:
        return loads(value.decode()) 
    else:
        return None

def find_suitable(key_pattern, attributes) -> List[str]:
    '''
    Search for a item in the database 
    that matches the given attributes
    '''
    keys = list(map(
        bytes.decode, 
        database.keys(pattern=key_pattern)
        ))
    suitable_keys = []
    for key in keys:
        _dict = get_if_exists(key)
        suitable = True
        for attr in attributes:
            if _dict.get(attr) != attributes[attr]:
                suitable = False
                break
        if suitable:
            suitable_keys.append(key)
    logging.debug(f"For attrs: {attributes} found {len(suitable_keys)} item(s)")
    return suitable_keys

