from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, StateFilter
from asyncio import AbstractEventLoop, sleep as async_sleep
import logging

from .checker import check_time
from .setbuilding import cmd_setbuilding
from .callback_setbuilding import answer_callback_setbuilding_handler
from modules.common.constants import BOT_ADMIN, REMINDER_CHECKER_INTERVAL


async def forever(function, interval, *args, **kwargs):
    while 1:
        logging.debug(f"Run function {function.__name__}")
        await function(*args, **kwargs)
        await async_sleep(interval)

def setup(dp: Dispatcher, loop: AbstractEventLoop = None, *args, **kwargs):
    logging.debug('Initialize cleaning module')
    loop.create_task(forever(
        function=check_time, 
        interval=REMINDER_CHECKER_INTERVAL,
        dp=dp
        ))

    dp.register_message_handler(cmd_setbuilding, Command('setbuilding'))
    dp.register_callback_query_handler(
        answer_callback_setbuilding_handler,
        lambda query: query.data.startswith('setbuilding')
        )