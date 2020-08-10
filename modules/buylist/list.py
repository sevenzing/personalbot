from aiogram import types
from aiogram.dispatcher import FSMContext
import logging


from modules.common.database import (
    ListModel, UserModel
)
from modules.common import constants


from misc import logger

async def cmd_list(message: types.Message, state: FSMContext, *args, **kwargs):
    user = UserModel(message)
    _list = ListModel(user).content()

    await message.answer(
        "Your list:",
        reply_markup=__generate_buttons_for_list(_list))


def __generate_buttons_for_list(_list: list) -> types.InlineKeyboardMarkup:
    '''
    Generate InlineKeyboardMarkup for the _list
    '''
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    for item_name, amount in _list:
        name_button = types.InlineKeyboardButton(
            text = f"{item_name}: [{amount}]",
            callback_data=f"change_menu:{constants.INLINE_COMMAND_INCRESE}:{item_name}")

        decr_button = types.InlineKeyboardButton(
            text = constants.TEXT_DECREASE,
            callback_data=f"change_menu:{constants.INLINE_COMMAND_DECREASE}:{item_name}")
        
        keyboard.add(name_button, decr_button)

    close_button = types.InlineKeyboardButton(
            text = constants.TEXT_EXIT,
            callback_data=f"change_menu:{constants.INLINE_COMMAND_EXIT}:")

    clearlist_button = types.InlineKeyboardButton(
            text = constants.TEXT_CLEAR,
            callback_data=f"change_menu:{constants.INLINE_COMMAND_CLEAR}:")
    
    keyboard.add(close_button, clearlist_button)

    return keyboard
