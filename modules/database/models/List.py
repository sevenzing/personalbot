from umongo import Document, fields, validate
from aiogram import types
from aiogram.utils.exceptions import MessageToEditNotFound

from modules.common.utils import get_now
from modules.database import mongo_instance
from modules.common import constants
from modules.buylist import messages as buylist_messages
from misc import dp

import logging

logging.debug('initialize list model')


def default_list():
    return {'Sample': {
        'amount': 0,
        'date': get_now().strftime('%Y %m %d %H %M %S')
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
        Return list in such way sorted by date:
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

    def _update(self):
        self._items = self._items.copy()
        return self.commit()

    
    async def clear(self) -> bool:
        '''
        Completely clear the list
        '''
        self._items = {}
        result = self._update()
        await self.update_all_list_messages()
        return result

    def generate_buttons_for_list(self) -> types.InlineKeyboardMarkup:
        '''
        Generate InlineKeyboardMarkup for the list
        If list is empty, return empty button
        '''
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        logging.debug(f"Generate buttons for list with {len(self._items)} items")
        if len(self._items) == 0:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=buylist_messages.BUTTON_EMPTY_LIST,
                    callback_data=constants.INLINE_PREFIX_EMPTY_LIST,
                    )
            )

            return keyboard


        for item_name, amount in self.__content():
            name_button = types.InlineKeyboardButton(
                text = f"{item_name}: [{amount}]",
                callback_data=f"{constants.INLINE_PREFIX_CHANGE_MENU}:{constants.INLINE_COMMAND_INCRESE}:{item_name}")

            decr_button = types.InlineKeyboardButton(
                text = buylist_messages.BUTTON_DECREASE,
                callback_data=f"{constants.INLINE_PREFIX_CHANGE_MENU}:{constants.INLINE_COMMAND_DECREASE}:{item_name}")
            
            keyboard.add(name_button, decr_button)

        close_button = types.InlineKeyboardButton(
                text = buylist_messages.BUTTON_EXIT,
                callback_data=f"{constants.INLINE_PREFIX_CHANGE_MENU}:{constants.INLINE_COMMAND_EXIT}:")

        clearlist_button = types.InlineKeyboardButton(
                text = buylist_messages.BUTTON_CLEAR,
                callback_data=f"{constants.INLINE_PREFIX_CHANGE_MENU}:{constants.INLINE_COMMAND_CLEAR}:")
        
        keyboard.add(close_button, clearlist_button)

        return keyboard

    async def add(self, items: list) -> bool:
        '''
        Add all items to list. 
        If it already exists, increment amount
        '''
        logging.debug(f"Got {len(items)} items")
        if len(items) > constants.MAX_ITEMS_TO_ADD_AT_TIME:
            return False

        logging.debug(f"Adding {items} to buylist for chat {self.chat_id}")
        for item in items:
            if len(item) > constants.MAX_ITEM_LENGTH:
                logging.debug(f"Item {item} has length {len(item)} is more than {constants.MAX_ITEM_LENGTH}")
                return False

            result = await self.change_amount(item, +1, update_all_lists=False)
            if not result:
                return False
        
        await self.update_all_list_messages()
        return True

    async def change_amount(self, item_name: str, number: int, update_all_lists=True) -> bool:
        '''
        Set `amount` = `amount` + `number`
        If new amount less than one, then delete it
        If there is no item_name, create one with amount == number
        
        Return bool as result of work
        '''
        logging.debug(f"change item {item_name} for list: {self._items}")
        
        self._items.setdefault(item_name, 
                default_list()['Sample']
                )
        self._items[item_name]['amount'] += number

        logging.debug(f"changed amount for {item_name} to {self._items[item_name]['amount']}")

        if self._items[item_name]['amount'] <= 0:
            self._items.pop(item_name)

        result = self._update()
        if update_all_lists:
            await self.update_all_list_messages()
        
        return result
        
    async def update_all_list_messages(self):
        buttons = self.generate_buttons_for_list()
        logging.debug(f"Update all messages for chat {self.chat_id}")
        for message_id in self.messages:
            logging.debug(f"Edit message {message_id}")
            try:
                await dp.bot.edit_message_reply_markup(
                    self.chat_id, 
                    message_id, 
                    reply_markup=buttons
                )
            except MessageToEditNotFound:
                pass

def create_list(chat_id):
    '''
    Creates new unattached list
    '''
    _list = ListModel(chat_id=chat_id)
    _list.required_validate()
    _list.commit()
    return _list