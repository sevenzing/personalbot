from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, StateFilter

from .list import cmd_list
from .add import cmd_add, add_to_list, Form
from .callback_list import answer_callback_handler

def setup(dp: Dispatcher):
    dp.register_message_handler(cmd_list, Command('list'), state='*')
    dp.register_message_handler(cmd_add, Command('add'))
    dp.register_message_handler(add_to_list, state=Form.waiting_for_add)
    dp.register_callback_query_handler(
        answer_callback_handler, 
        lambda query: query.data.startswith('change_menu')
    )
