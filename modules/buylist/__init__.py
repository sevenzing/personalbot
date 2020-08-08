from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, StateFilter

from modules.buylist.list import cmd_list
from modules.buylist.add import cmd_add, add_to_list, Form


def setup(dp: Dispatcher):
    dp.register_message_handler(cmd_list, Command('list'), state='*')
    dp.register_message_handler(cmd_add, Command('add'))
    dp.register_message_handler(add_to_list, state=Form.waiting_for_add)