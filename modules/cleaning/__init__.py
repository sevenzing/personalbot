from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, StateFilter
from asyncio import AbstractEventLoop
import logging

from .checker import check_time
from .setbuilding import cmd_setbuilding, answer_callback_setbuilding_handler
from .nextcleaning import cmd_nextcleaning
from .setreminder import cmd_setreminder, answer_callback_setreminder_handler
from .schedule import cmd_schedule

from modules.common.constants import BOT_ADMIN, REMINDER_CHECKER_INTERVAL, INLINE_PREFIX_SETBUILDING, INLINE_PREFIX_SETREMINDER
from modules.common.utils import forever_run


def setup(dp: Dispatcher, loop: AbstractEventLoop = None, *args, **kwargs):
    logging.debug('Initialize cleaning module')
    loop.create_task(forever_run(
        function=check_time, 
        interval=REMINDER_CHECKER_INTERVAL,
        dp=dp
        ))

    dp.register_message_handler(cmd_schedule, Command('schedule'))
    dp.register_message_handler(cmd_setbuilding, Command('setbuilding'))
    dp.register_message_handler(cmd_setreminder, Command('setreminder'))
    dp.register_message_handler(cmd_nextcleaning, Command('nextcleaning'))
    dp.register_callback_query_handler(
        answer_callback_setbuilding_handler,
        lambda query: query.data.startswith(INLINE_PREFIX_SETBUILDING)
        )
    dp.register_callback_query_handler(
        answer_callback_setreminder_handler,
        lambda query: query.data.startswith(INLINE_PREFIX_SETREMINDER)
    )