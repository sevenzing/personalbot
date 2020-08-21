from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from modules.buylist import messages
from modules.common.utils import parse_commad
from modules.database.models.User import User, get_user
from modules.database.models.List import List

import logging


class Form(StatesGroup):
    waiting_for_add = State()

async def cmd_add(message: types.Message):
    _, args = parse_commad(message.text)
    if args:
        await __add_to_list(message, items=args)
    else:
        await Form.waiting_for_add.set()
        logging.debug('set state to waiting')
        await message.answer(messages.ON_CMD_ADD)

async def add_to_list(message: types.Message, state: FSMContext):
    '''
    Command on `waiting_for_add` states
    '''
    _, args = parse_commad('/add ' + message.text)
    await __add_to_list(message, items=args)
    await state.finish()
    
async def __add_to_list(message: types.Message, items: list):
    '''
    Add all item from `items` to user's list
    '''
    user = get_user(message.chat.id)
    _list =  user.get_buy_list()

    if _list.add(items):
        await message.answer(messages.ADDED_TO_LIST)
    else:
        await message.answer(messages.SOMETHING_WENT_WRONG)