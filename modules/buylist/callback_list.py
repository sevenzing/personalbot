from aiogram import types

from modules.common import constants
from modules.common.database import ListModel, UserModel

async def answer_callback_handler(query: types.CallbackQuery):
    message = query.message
    _, command, item_name = query.data.split(':')
    _list = ListModel(UserModel(message))
    
    if command == constants.INLINE_COMMAND_INCRESE:
        result = _list.change_amount(item_name, 1)

    elif command == constants.INLINE_COMMAND_DECREASE:
        result = _list.change_amount(item_name, -1)

    elif command == constants.INLINE_COMMAND_CLEAR:
        result = _list.clear()

    elif command == constants.INLINE_COMMAND_EXIT:
        result = message.delete()
    else:
        result = None
    
    if result:
        await query.answer('Done')
