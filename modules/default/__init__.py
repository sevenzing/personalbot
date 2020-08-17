from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, StateFilter
import logging

from .start import cmd_start
from .cancel import cmd_cancel
from .help import cmd_help


def setup(dp: Dispatcher, *args, **kwargs):
    logging.debug('Initialize default module')
    
    dp.register_message_handler(cmd_start, Command('start'), state='*')
    dp.register_message_handler(cmd_help, Command('help'), state='*')
    dp.register_message_handler(cmd_cancel, Command('cancel'), state='*')
