from aiogram import types

from modules.common import constants
from modules.common.database import ListModel, UserModel

from misc import logger

async def answer_callback_handler(query: types.CallbackQuery):
    message = query.message
    _, command, item_name = query.data.split(':')
    _list = ListModel(UserModel(message))
    
    logger.debug(f"Got inline query. Data: {query.data}")

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
        await message.edit_reply_markup(
            reply_markup=_list.generate_buttons_for_list()
        )
        await query.answer('Done')
