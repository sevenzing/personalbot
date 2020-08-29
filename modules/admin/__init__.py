from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from .restart import cmd_restart

import logging


def setup(dp: Dispatcher, *args, **kwargs):
    logging.debug('Initialize admin module')
    
    dp.register_message_handler(cmd_restart, Command('restart'))
