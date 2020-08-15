import os

BOT_TOKEN = os.getenv('BOT_TOKEN', '')

BOT_ADMIN = os.getenv('BOT_ADMIN', '')

redis = {
    'host': 'redis',
    'port': 5432,

}

TIME_ZONE = 'Etc/GMT-3'

MAX_ITEM_LENGTH = 20

INLINE_COMMAND_INCRESE = 'increase'
INLINE_COMMAND_DECREASE = 'decrese'
INLINE_COMMAND_EXIT = 'exit'
INLINE_COMMAND_CLEAR = 'clear'

TEXT_DECREASE = '[Decrease]'
TEXT_CLEAR = '[Clear]'
TEXT_EXIT = '[Close]'

REMINDER_CHECKER_INTERVAL = 3 # sec
