from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram import types

from typing import List
import logging
from . import database
from modules.common.utils import get_now, get_next_day
from modules.common.database.utils import (
    set_if_exists,
    set_if_not_exists,
    get_if_exists,
    find_suitable,
)

from modules.common.database import ListModel


class User:
    def __init__(self, message: types.Message = None, chat_id = None):
        if message:
            self.chat_id = message.chat.id
        elif chat_id:
            self.chat_id = chat_id
        
        set_if_not_exists(self.key, User.default())

    
    @property
    def key(self) -> str:
        return f"data:{self.chat_id}"

    @staticmethod
    def default() -> dict:
        return {
            'list': ListModel.default(),
            'username': '',
            'lastnotice': get_next_day(get_now()).__repr__(),
            'checknotice': True,
            'chosenbuilding': 0,
            'noticehour': 8,
        }

    def update(self, **values) -> bool:
        '''
        Updates value in database
        '''
        for key in values:
            if not (
                isinstance(values[key], int) or 
                isinstance(values[key], str) or 
                isinstance(values[key], dict)):
                
                values[key] = values[key].__repr__()

        data: dict = get_if_exists(self.key)
        data.update(values)
        return set_if_exists(self.key, data)
        

    
    def get(self, key):
        return get_if_exists(self.key).get(key)


def find_users(**attributes) -> List[User]:
    '''
    Returns list of users 
    with the following attributes
    '''
    keys = find_suitable(key_pattern='data:*', attributes=attributes)
    chat_ids = map(lambda key: key.split(':')[1], keys)
    users = map(lambda chat_id: User(chat_id=chat_id), chat_ids)

    return list(users)