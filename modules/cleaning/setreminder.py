from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging

from modules.cleaning import messages
from modules.database.models import UserModel, create_user_if_not_exists
from modules.common import constants

def generate_empty_button() -> InlineKeyboardButton:
    return InlineKeyboardButton(text=' ', callback_data='None')

def generate_setreminder_buttons(user: UserModel) -> InlineKeyboardMarkup:
    # [✔ At the day ✔] [✘ Before the day ✘]
    # [      🔺      ] [                  ]
    # [     8:00     ] [                  ]
    # [      🔻      ] [                  ]
    hour_at_day = user.notification[constants.ON_CLEANING]
    hour_before_day = user.notification[constants.BEFORE_CLEANING]
    
    keyboard = [[generate_empty_button() for _ in range(2)] for _ in range(4)]

    notification_hour_on_cleaning = user.notification[constants.ON_CLEANING]
    notification_hour_before_cleaning = user.notification[constants.BEFORE_CLEANING]

    DOUBLE_EMOJI_CHECK_MARK = (constants.EMOJI_CHECK_MARK,) *2
    DOUBLE_EMOJI_X_MARK = (constants.EMOJI_X_MARK,) *2

    ON_CLEANING_SIGNS = DOUBLE_EMOJI_CHECK_MARK if notification_hour_on_cleaning else DOUBLE_EMOJI_X_MARK
    BEFORE_CLEANING_SIGNS = DOUBLE_EMOJI_CHECK_MARK if notification_hour_before_cleaning else DOUBLE_EMOJI_X_MARK

    keyboard[0][0] = InlineKeyboardButton(
        text=messages.BUTTON_ON_CLEANING % ON_CLEANING_SIGNS, 
        callback_data=':'.join([constants.INLINE_PREFIX_SETREMINDER, constants.INLINE_INFIX_TURN, constants.ON_CLEANING]))
    keyboard[0][1] = InlineKeyboardButton(
        text=messages.BUTTON_BEFORE_CLEANING % BEFORE_CLEANING_SIGNS, 
        callback_data=':'.join([constants.INLINE_PREFIX_SETREMINDER, constants.INLINE_INFIX_TURN, constants.BEFORE_CLEANING]))
    
    for i, arg in enumerate([constants.ON_CLEANING, constants.BEFORE_CLEANING]):
        notification_hour = user.notification[arg]
        if notification_hour == None:
            continue

        # /\
        keyboard[1][i] = InlineKeyboardButton(
            text=constants.EMOJI_RED_TRIANGLE_POINTED_UP,
            callback_data=':'.join([constants.INLINE_PREFIX_SETREMINDER, constants.INLINE_INFIX_PLUS, arg])
        )
        # time
        keyboard[2][i] = InlineKeyboardButton(
            text=f"{notification_hour}:00",
            callback_data=':'.join([constants.INLINE_PREFIX_SETREMINDER, constants.INLINE_INFIX_PLUS, arg])
        )
        # \/
        keyboard[3][i] = InlineKeyboardButton(
            text=constants.EMOJI_RED_TRIANGLE_POINTED_DOWN,
            callback_data=':'.join([constants.INLINE_PREFIX_SETREMINDER, constants.INLINE_INFIX_MINUS, arg])
        )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def cmd_setreminder(message: types.Message):
    user = create_user_if_not_exists(message.chat.id)
    
    await message.answer(text='not yet', reply_markup=generate_setreminder_buttons(user))


async def answer_callback_setreminder_handler(query: types.CallbackQuery):
    '''
    Answer on query from choosing building message
    '''
    logging.debug(f"got data: {query.data}")
    user = create_user_if_not_exists(query.message.chat.id)
    _, command, arg = query.data.split(':')
    if command == constants.INLINE_INFIX_TURN:
        user.notification[arg] = None \
            if user.notification[arg] != None else constants.DEFAULT_NOTICE_HOUR_ON_CLEANING \
                if arg == constants.ON_CLEANING else constants.DEFAULT_NOTICE_HOUR_BEFORE_CLEANING
    else:
        current_hour = user.notification[arg]
        if command == constants.INLINE_INFIX_PLUS:
            logging.debug('plus 1 hour')
            current_hour = (current_hour + 1) % 24
        elif command == constants.INLINE_INFIX_MINUS:
            logging.debug('minus 1 hour')
            current_hour = (current_hour - 1) % 24
        else:
            logging.debug(f"Command {command} not found")
            return

        user.notification[arg] = current_hour

    user.update(notification=user.notification)
    await query.message.edit_reply_markup(reply_markup=generate_setreminder_buttons(user))