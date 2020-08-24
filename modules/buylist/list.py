from aiogram import types
import logging
from aiogram.utils.exceptions import MessageNotModified

from modules.database.models import create_user_if_not_exists
from modules.common import constants
from modules.buylist import messages


async def cmd_list(message: types.Message, *args, **kwargs):
    '''
    Send buy list to user, add message_id to messages of the list
    '''
    user = create_user_if_not_exists(message.chat.id)
    _list = user.get_buy_list()
    logging.debug(f"Send list to the chat {message.chat.id}")
    message_sent: types.Message = await message.answer(
        messages.ON_CMD_LIST,
        reply_markup=_list.generate_buttons_for_list(),
        parse_mode='Markdown',
    )
    
    logging.debug(f"Append message with list to list of messages")
    _list.messages.insert(0, message_sent.message_id)
    _list.messages = _list.messages[:constants.MAX_TRACKING_LISTS]
    _list._update()

async def answer_callback_list_handler(query: types.CallbackQuery):
    '''
    Answer on query of the list, execute the necessary command
    '''
    message = query.message
    _, command, item_name = query.data.split(':')
    user = create_user_if_not_exists(message.chat.id)
    _list = user.get_buy_list()
    logging.debug(f"Got inline query. Data: {query.data}")
    
    result = None
    if command == constants.INLINE_COMMAND_INCRESE:
        result = await _list.change_amount(item_name, 1)

    elif command == constants.INLINE_COMMAND_DECREASE:
        result = await _list.change_amount(item_name, -1)

    elif command == constants.INLINE_COMMAND_CLEAR:
        await _list.clear()
        await message.delete()
        
    elif command == constants.INLINE_COMMAND_EXIT:
        await message.delete()
    
    if result:
        try:
            await message.edit_reply_markup(
                reply_markup=_list.generate_buttons_for_list()
            )
        except MessageNotModified:
            logging.debug('Message wasnt modified. Skip it')
        await query.answer(messages.QUERY_DONE)

async def answer_empty_list(query: types.CallbackQuery):
    await query.answer(messages.QUERY_EMPTY_LIST)
