from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, StateFilter
from asyncio import AbstractEventLoop
import logging

from .checker import check_time



async def forever(function, *args, **kwargs):
    while 1:
        logging.debug(f"Run function {function.__name__}")
        await function(*args, **kwargs)


def setup(dp: Dispatcher, loop: AbstractEventLoop = None, *args, **kwargs):
    logging.debug('Initialize cleaning')
    loop.create_task(forever(check_time, dp=dp))