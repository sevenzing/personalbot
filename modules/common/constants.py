import os

BOT_TOKEN = os.getenv('BOT_TOKEN', '')

BOT_ADMIN = os.getenv('BOT_ADMIN', '')

redis = {
    'host': 'redis',
    'port': 5432,

}

mongo = {
    'host': 'mongodb://root:password@mongo:27017/'
}

TIME_ZONE = 'Etc/GMT-3'

MAX_ITEM_LENGTH = 20
MAX_ITEMS_TO_ADD_AT_TIME = 1000

INLINE_COMMAND_INCRESE = 'increase'
INLINE_COMMAND_DECREASE = 'decrese'
INLINE_COMMAND_EXIT = 'exit'
INLINE_COMMAND_CLEAR = 'clear'

REMINDER_CHECKER_INTERVAL = 60 # sec
