from datetime import datetime
from aiogram import types
import logging

from modules.common import constants
from modules.buylist import messages as buylist_messages
from modules.common.utils import get_now


class List:
    '''
    list structure: {
        '<<item name>>': {
            'amount': 1,
            'date': datetime.datetime()
        }
    }
    '''

    @staticmethod
    def default():
        return {'Sample': {
            'amount': 0,
            'date': get_now().strftime('%Y %m %d %H %M %S')
        }}

    def __init__(self, user, **kwargs):
        self.user = user
        self.current_list = self.__get_list()

    def __get_list(self) -> dict:
        '''
        Returns current list from database
        '''
        return self.user['list']

    def __update(self) -> bool:
        '''
        Update value in database

        Returns bool as result of work
        '''
        return self.user.update(list=self.current_list)
    
    def __content(self) -> list:
        '''
        Returns list in such way sorted by date:
        [ ('<<item name>>', 1), ( ... ) ]
        '''
        logging.debug(f"{self.__get_list()} -- {self.current_list}")
        # item names, sorted by date
        sorted_names = sorted(
            self.current_list, 
            key=lambda name: self.current_list[name]['date'])
        
        result_list = [
            (name, self.current_list[name]['amount']) 
                for name in sorted_names
                ]
        logging.debug(f"generated list: {result_list}")
        return result_list

    def add(self, items: list) -> bool:
        '''
        Add all items to list. 
        If it already exists, increment amount
        '''
        logging.debug(f"Adding {items} to buylist for chat {self.user.chat_id}")
        for item in items:

            if len(item) > constants.MAX_ITEM_LENGTH:
                logging.debug(f"Item {item} has length {len(item)} is more than {constants.MAX_ITEM_LENGTH}")
                return False

            self.current_list.setdefault(item, 
                List.default()['Sample']
                )

        for item in items:
            self.current_list[item]['amount'] += 1

        return self.__update()

    def clear(self) -> bool:
        '''
        Completely clear the list
        '''
        self.current_list = {}
        return self.__update()

    def generate_buttons_for_list(self) -> types.InlineKeyboardMarkup:
        '''
        Generate InlineKeyboardMarkup for the list
        If list is empty, returns empty button
        '''
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        logging.debug(f"Generate buttons for list with {len(self.current_list)} items")
        if len(self.current_list) == 0:
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
        '''
        Set `amount` = `amount` + `number`
        If new amount less than one, then delete it
        
        Returns bool as result of work
        '''
        logging.debug(str(self.current_list))

        if item_name in self.current_list:
            self.current_list[item_name]['amount'] += number

            logging.debug(f"changed amount for {item_name} to {self.current_list[item_name]['amount']}")

            if self.current_list[item_name]['amount'] <= 0:
                self.current_list.pop(item_name)
        
            return self.__update()
        
        else:
            return False
