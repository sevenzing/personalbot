from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, StateFilter
from asyncio import AbstractEventLoop, sleep as async_sleep
import logging

from .checker import check_time
from modules.common.constants import BOT_ADMIN, REMINDER_CHECKER_INTERVAL


async def forever(function, interval, *args, **kwargs):
    while 1:
        logging.debug(f"Run function {function.__name__}")
        await function(*args, **kwargs)
        await async_sleep(interval)

def setup(dp: Dispatcher, loop: AbstractEventLoop = None, *args, **kwargs):
    logging.debug('Initialize cleaning')
    loop.create_task(forever(
        function=check_time, 
        interval=REMINDER_CHECKER_INTERVAL,
        dp=dp
        ))
