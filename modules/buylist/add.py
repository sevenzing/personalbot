from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from modules.buylist import messages
from modules.common.utils import parse_commad
from modules.database.models import UserModel, create_user_if_not_exists

import logging


class AddFSM(StatesGroup):
    waiting_for_add = State()

async def cmd_add(message: types.Message):
    '''
    If user write command without arguments, 
    change the state to waiting for items,
    otherwise add all items to list
    '''
    _, args = parse_commad(message.text)
    if args:
        await __add_to_list(message, items=args)
    else:
        await AddFSM.waiting_for_add.set()
        logging.debug('Set state to waiting')
        await message.answer(messages.ON_CMD_ADD)

async def add_to_list(message: types.Message, state: FSMContext):
    '''
    Executes only waiting_for_add state.
    Parse message and add all items
    '''
    _, args = parse_commad('/add ' + message.text)
    await __add_to_list(message, items=args)
    await state.finish()
    
async def __add_to_list(message: types.Message, items: list):
    '''
    Add all item to user's list
    '''
    user = create_user_if_not_exists(message.chat.id)
    _list =  user.get_buy_list()

    if await _list.add(items):
        await message.answer(messages.ADDED_TO_LIST)
    else:
        await message.answer(messages.SOMETHING_WENT_WRONG)