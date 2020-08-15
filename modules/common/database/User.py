from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram import types


from . import database
from modules.common.database.utils import (
    set_if_exists,
    set_if_not_exists,
    get_if_exists,
)

from modules.common.database.List import List


class User:
    def __init__(self, message: types.Message):
        self.chat_id = message.chat.id
        set_if_not_exists(self.key, User.default())

    
    @property
    def key(self) -> str:
        return f"data:{self.chat_id}"

    @staticmethod
    def default() -> dict:
        return {
            'list': List.default(),
            'username': '',
            'lastnotice': None,
            'checknotice': True,
            'chosenbuilding': 0
        }

    def update(self, **values) -> bool:
        '''
        Updates value in database
        '''

        data: dict = get_if_exists(self.key)
        data.update(values)
        return set_if_exists(self.key, data)
        

    
    def get(self, key):
        return get_if_exists(self.key).get(key)
    