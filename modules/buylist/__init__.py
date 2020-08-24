from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, StateFilter

from .list import cmd_list, answer_callback_list_handler, answer_empty_list
from .add import cmd_add, add_to_list, Form

import logging

def setup(dp: Dispatcher, *args, **kwargs):
    logging.debug('Initialize buylist module')
    
    dp.register_message_handler(cmd_list, Command('list'), state='*')
    dp.register_message_handler(cmd_add, Command('add'))
    dp.register_message_handler(add_to_list, state=Form.waiting_for_add)
    dp.register_callback_query_handler(
        answer_callback_list_handler, 
        lambda query: query.data.startswith('change_menu')
    )
    dp.register_callback_query_handler(
        answer_empty_list,
        lambda query: query.data.startswith('empty_list')
    )
