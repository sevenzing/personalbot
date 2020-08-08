import modules.common.constants as config

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

import logging
from redis import Redis

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -15s %(funcName) -20s: %(message)s')
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger('bot')

database = Redis(**config.redis)

storage = RedisStorage2(**config.redis)
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)