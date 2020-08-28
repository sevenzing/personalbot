from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, StateFilter
from asyncio import AbstractEventLoop
import logging

from .start import cmd_start
from .cancel import cmd_cancel
from .help import cmd_help
from .callback_empty_button import answer_callback_empty_button_handler
from modules.common.constants import CONNECTION_CHECKER_INTERVAL
from modules.common.utils import forever_run
from modules.default.checker import check_connection

def setup(dp: Dispatcher, loop: AbstractEventLoop=None, *args, **kwargs):
    logging.debug('Initialize default module')

    loop.create_task(forever_run(
        function=check_connection, 
        interval=CONNECTION_CHECKER_INTERVAL,
        ))
    
    dp.register_message_handler(cmd_start, Command('start'), state='*')
    dp.register_message_handler(cmd_help, Command('help'), state='*')
    dp.register_message_handler(cmd_cancel, Command('cancel'), state='*')
    dp.register_callback_query_handler(
        answer_callback_empty_button_handler,
        lambda query: query.data == 'None'
    )