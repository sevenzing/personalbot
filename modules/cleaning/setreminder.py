from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging

from modules.cleaning import messages
from modules.database.models import UserModel, create_user_if_not_exists
from modules.common import constants

def generate_empty_button() -> InlineKeyboardButton:
    '''
    Generate and return empty_button
    '''
    return InlineKeyboardButton(text=' ', callback_data='None')

def generate_setreminder_buttons(user: UserModel) -> InlineKeyboardMarkup:
    '''
    Generate and return buttons to set reminder in this way:

    [✔ At the day ✔] [✘ Before the day ✘]
    [      🔺      ] [                  ]
    [     8:00     ] [                  ]
    [      🔻      ] [                  ]
    [               CLOSE               ]

    callback data of every button forms like PREFIX:INFIX:ARG
    example for setreminder buttons is setreminder:plus:on_cleaning
    '''
    keyboard = [[generate_empty_button() for _ in range(2)] for _ in range(4)]

    DOUBLE_EMOJI_CHECK_MARK = (constants.EMOJI_CHECK_MARK,) *2
    DOUBLE_EMOJI_X_MARK = (constants.EMOJI_X_MARK,) *2

    args = [constants.ON_CLEANING, constants.BEFORE_CLEANING]
    buttons_messages = [messages.BUTTON_ON_CLEANING, messages.BUTTON_BEFORE_CLEANING]

    for i, (arg, button_message) in enumerate(zip(args,buttons_messages)):
        notification_hour = user.notification[arg]

        # turn on/off button
        keyboard[0][i] = InlineKeyboardButton(
            text=button_message % (DOUBLE_EMOJI_CHECK_MARK if notification_hour != None else DOUBLE_EMOJI_X_MARK),
            callback_data=':'.join([constants.INLINE_PREFIX_SETREMINDER, constants.INLINE_INFIX_TURN, arg])
            )

        if notification_hour == None:
            # if so, leave remaining buttons as empty_buttons
            continue

        # /\ button
        keyboard[1][i] = InlineKeyboardButton(
            text=constants.EMOJI_RED_TRIANGLE_POINTED_UP,
            callback_data=':'.join([constants.INLINE_PREFIX_SETREMINDER, constants.INLINE_INFIX_PLUS, arg])
        )
        # time button
        keyboard[2][i] = InlineKeyboardButton(
            text=f"{notification_hour}:00",
            callback_data=':'.join([constants.INLINE_PREFIX_SETREMINDER, constants.INLINE_INFIX_TIME, arg])
        )
        # \/ button
        keyboard[3][i] = InlineKeyboardButton(
            text=constants.EMOJI_RED_TRIANGLE_POINTED_DOWN,
            callback_data=':'.join([constants.INLINE_PREFIX_SETREMINDER, constants.INLINE_INFIX_MINUS, arg])
        )
    
    close_button = InlineKeyboardButton(
        text='Close',
        callback_data=':'.join([constants.INLINE_PREFIX_SETREMINDER, constants.INLINE_INFIX_CLOSE, ''])
    )
    return InlineKeyboardMarkup(inline_keyboard=(keyboard + [[close_button]]))

async def cmd_setreminder(message: types.Message):
    user = create_user_if_not_exists(message.chat.id)
    
    await message.answer(
        text=messages.ON_CMD_SETREMINDER, 
        reply_markup=generate_setreminder_buttons(user)
        )


async def answer_callback_setreminder_handler(query: types.CallbackQuery):
    '''
    Answer on query from set reminder message
    '''
    logging.debug(f"got data: {query.data}")
    user = create_user_if_not_exists(query.message.chat.id)
    _, command, arg = query.data.split(':')
    answered = False
    update_message = True
    if arg:
        current_hour = user.notification[arg]
    if command == constants.INLINE_INFIX_TURN:
        current_hour = None \
            if user.notification[arg] != None else constants.DEFAULT_NOTICE_HOUR_ON_CLEANING \
                if arg == constants.ON_CLEANING else constants.DEFAULT_NOTICE_HOUR_BEFORE_CLEANING
    elif command == constants.INLINE_INFIX_PLUS:
        logging.debug('plus 1 hour')
        current_hour = (current_hour + 1) % 24
    elif command == constants.INLINE_INFIX_MINUS:
        logging.debug('minus 1 hour')
        current_hour = (current_hour - 1) % 24
    elif command == constants.INLINE_INFIX_TIME:
        # if so, just answer on query and dont update message
        update_message = False
    elif command == constants.INLINE_INFIX_CLOSE:
        await query.message.delete()
        return
    else:
        logging.warning(f"Command {command} not found")
        return

    user.notification[arg] = current_hour
    user.update(notification=user.notification)
    
    await query.answer(
                'Notification ' + \
                ('on' if arg == constants.ON_CLEANING else 'before') + \
                ' cleaning day ' + \
                (f'will be on {current_hour}:00' if current_hour else 'won\'t be sent')
                )
    if update_message:
        await query.message.edit_reply_markup(reply_markup=generate_setreminder_buttons(user))