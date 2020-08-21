from aiogram import types
import logging

from modules.buylist import messages
from modules.common import constants
from modules.database.models import create_user_if_not_exists


async def answer_callback_handler(query: types.CallbackQuery):
    message = query.message
    _, command, item_name = query.data.split(':')
    user = create_user_if_not_exists(message.chat.id)
    _list = user.get_buy_list()
    logging.debug(f"Got inline query. Data: {query.data}")
    
    result = None
    if command == constants.INLINE_COMMAND_INCRESE:
        result = _list.change_amount(item_name, 1)

    elif command == constants.INLINE_COMMAND_DECREASE:
        result = _list.change_amount(item_name, -1)

    elif command == constants.INLINE_COMMAND_CLEAR:
        _list.clear()
        await message.delete()
        
    elif command == constants.INLINE_COMMAND_EXIT:
        await message.delete()
    
    if result:
        await message.edit_reply_markup(
            reply_markup=_list.generate_buttons_for_list()
        )
        await query.answer(messages.QUERY_DONE)

async def answer_empty_list(query: types.CallbackQuery):
    await query.answer(messages.QUERY_EMPTY_LIST)