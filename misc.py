import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from redis import Redis
import logging

from modules.common import constants


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -15s %(funcName) -20s: %(message)s')
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

database = Redis(**constants.redis)

storage = RedisStorage2(**constants.redis)
bot = Bot(token=constants.BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

reminder_loop = asyncio.get_event_loop()

