import os

BOT_TOKEN = os.getenv('BOT_TOKEN', '')


redis = {
    'host': 'redis',
    'port': 5432,

}

MAX_ITEM_LENGTH = 20