import os

BOT_TOKEN = os.getenv('BOT_TOKEN', '')

BOT_ADMIN = os.getenv('BOT_ADMIN', '')

BOT_ADMIN_ALIAS = os.getenv('BOT_ADMIN_ALIAS', '')

URL_TO_SCHEDULE = os.environ.get('URL_TO_SCHEDULE', '')

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
MAX_TRACKING_LISTS = 5

INLINE_COMMAND_INCRESE = 'increase'
INLINE_COMMAND_DECREASE = 'decrese'
INLINE_COMMAND_EXIT = 'exit'
INLINE_COMMAND_CLEAR = 'clear'

BEFORE_CLEANING = 'before_cleaning'
ON_CLEANING = 'on_cleaning'

# inline query command is PREFIX:INFIX:arg
INLINE_PREFIX_CHANGE_MENU = 'change_menu'
INLINE_PREFIX_EMPTY_LIST = 'empty_list'
INLINE_PREFIX_SETBUILDING = 'setbuilding'
INLINE_PREFIX_SETREMINDER = 'setreminder'
INLINE_INFIX_TURN = 'turn'
INLINE_INFIX_TIME = 'time'
INLINE_INFIX_PLUS = 'plus'
INLINE_INFIX_MINUS = 'minus'
INLINE_INFIX_CLOSE = 'close'

REMINDER_CHECKER_INTERVAL = 10 # sec

EMOJI_RED_TRIANGLE_POINTED_UP = '🔺'
EMOJI_RED_TRIANGLE_POINTED_DOWN = '🔻'
EMOJI_X_MARK = '✘'
EMOJI_CHECK_MARK = '✔'


DEFAULT_NOTICE_HOUR_ON_CLEANING = 8
DEFAULT_NOTICE_HOUR_BEFORE_CLEANING = 20
