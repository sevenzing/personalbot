from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from .restart import cmd_restart
from .sendtochats import cmd_sendtochats, process_message, process_ids, SendToChatsFSM
import logging


def setup(dp: Dispatcher, *args, **kwargs):
    logging.info('Initialize admin module')
    
    dp.register_message_handler(cmd_restart, Command('restart', prefixes='#'))
    dp.register_message_handler(cmd_sendtochats, Command('sendtochats', prefixes='#'))
    dp.register_message_handler(
        process_ids,
        state=SendToChatsFSM.waiting_for_sendtochats_ids,
    )
    dp.register_message_handler(
        process_message,
        state=SendToChatsFSM.waiting_for_sendtochats_message,
    )