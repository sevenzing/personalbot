from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from modules.common.database.User import User
from modules.common.database.List import List
from modules.common.utils import parse_commad

from misc import logger


class Form(StatesGroup):
    waiting_for_add = State()

async def cmd_add(message: types.Message):
    command, args = parse_commad(message.text)
    if args:
        await __add_to_list(message, items=args)
    else:
        await Form.waiting_for_add.set()
        logger.debug('set state to waiting')
        await message.answer('send me your list')

async def add_to_list(message: types.Message, state: FSMContext):
    await __add_to_list(message, message.text.split('\n'))
    await state.finish()
    
async def __add_to_list(message: types.Message, items: list):
    user = User(message)
    _list =  List(user)

    if _list.add(items):
        await message.answer(f"ok, I set {' '.join(items)}")
    else:
        await message.answer(f"something went wrong")