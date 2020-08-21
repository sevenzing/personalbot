from umongo import Document, fields, validate
from aiogram import types

from modules.common.utils import get_now
from modules.database import mongo_instance
from modules.common import constants
from modules.buylist import messages as buylist_messages

import logging

logging.debug('initialize list model')


def default_list():
    return {'Sample': {
        'amount': 0,
        'date': get_now()
    }}

@mongo_instance.register
class ListModel(Document):
    chat_id = fields.IntField()
    _items = fields.DictField(values=fields.DictField, default=default_list())
    messages = fields.ListField(fields.IntField(), default=[])
    
    class Meta:
        collection_name = 'list'

    def __content(self) -> list:
        '''
        Returns list in such way sorted by date:
        [ ('<<item name>>', 1), ( ... ) ]
        '''
        logging.debug(f"getting content of {self._items}")
        # item names, sorted by date
        sorted_names = sorted(
            self._items, 
            key=lambda name: self._items[name]['date'])
        
        result_list = [
            (name, self._items[name]['amount']) 
                for name in sorted_names
                ]
        logging.debug(f"generated list: {result_list}")
        return result_list

    def __update(self):
        self._items = self._items.copy()
        return self.commit()

    def add(self, items: list) -> bool:
        '''
        Add all items to list. 
        If it already exists, increment amount
        '''
        logging.debug(f"Adding {items} to buylist for chat {self.chat_id}")
        for item in items:
            if len(item) > constants.MAX_ITEM_LENGTH:
                logging.debug(f"Item {item} has length {len(item)} is more than {constants.MAX_ITEM_LENGTH}")
                return False

            self._items.setdefault(item, 
                default_list()['Sample']
                )

        for item in items:
            self._items[item]['amount'] += 1

        return self.__update()
    
    def clear(self) -> bool:
        '''
        Completely clear the list
        '''
        self._items = {}
        return self.__update()

    def generate_buttons_for_list(self) -> types.InlineKeyboardMarkup:
        '''
        Generate InlineKeyboardMarkup for the list
        If list is empty, returns empty button
        '''
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        logging.debug(f"Generate buttons for list with {len(self._items)} items")
        if len(self._items) == 0:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=buylist_messages.BUTTON_EMPTY_LIST,
                    callback_data='None',
                    )
            )

            return keyboard


        for item_name, amount in self.__content():
            name_button = types.InlineKeyboardButton(
                text = f"{item_name}: [{amount}]",
                callback_data=f"change_menu:{constants.INLINE_COMMAND_INCRESE}:{item_name}")

            decr_button = types.InlineKeyboardButton(
                text = buylist_messages.BUTTON_DECREASE,
                callback_data=f"change_menu:{constants.INLINE_COMMAND_DECREASE}:{item_name}")
            
            keyboard.add(name_button, decr_button)

        close_button = types.InlineKeyboardButton(
                text = buylist_messages.BUTTON_EXIT,
                callback_data=f"change_menu:{constants.INLINE_COMMAND_EXIT}:")

        clearlist_button = types.InlineKeyboardButton(
                text = buylist_messages.BUTTON_CLEAR,
                callback_data=f"change_menu:{constants.INLINE_COMMAND_CLEAR}:")
        
        keyboard.add(close_button, clearlist_button)

        return keyboard

    def change_amount(self, item_name: str, number: int) -> bool:
        logging.debug('called change_amount function')
        '''
        Set `amount` = `amount` + `number`
        If new amount less than one, then delete it
        
        Returns bool as result of work
        '''
        logging.debug(f"change item {item_name} for list: {self._items}")
        if item_name in self._items:
            self._items[item_name]['amount'] += number

            logging.debug(f"changed amount for {item_name} to {self._items[item_name]['amount']}")

            if self._items[item_name]['amount'] <= 0:
                self._items.pop(item_name)

            return self.__update()
        
        else:
            return False


def create_list(chat_id):
    '''
    Creates new unattached list
    '''
    _list = ListModel(chat_id=chat_id)
    _list.required_validate()
    _list.commit()
    return _list