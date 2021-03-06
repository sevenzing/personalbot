import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from redis import Redis
from pymongo import MongoClient
from umongo import Instance
import logging

from modules.common import constants



LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -15s %(funcName) -20s: %(message)s')
LOG_LEVEL = logging.DEBUG if constants.LOG_LEVEL == 'debug' else logging.INFO if constants.LOG_LEVEL == 'info' else logging.ERROR
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
# remove debug logs from aiohttp logger
logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)
database = Redis(**constants.redis)
storage = RedisStorage2(**constants.redis)
mongo_client = MongoClient(**constants.mongo)
mongo_instance = Instance(mongo_client.personalbot)

bot = Bot(token=constants.BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

bot_id = bot.id

event_loop = asyncio.get_event_loop()

