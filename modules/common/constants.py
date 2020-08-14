import os

BOT_TOKEN = os.getenv('BOT_TOKEN', '')


redis = {
    'host': 'redis',
    'port': 5432,

}

MAX_ITEM_LENGTH = 20

INLINE_COMMAND_INCRESE = 'increase'
INLINE_COMMAND_DECREASE = 'decrese'
INLINE_COMMAND_EXIT = 'exit'
INLINE_COMMAND_CLEAR = 'clear'

TEXT_DECREASE = '[Decrease]'
TEXT_CLEAR = '[Clear]'
TEXT_EXIT = '[Close]'
