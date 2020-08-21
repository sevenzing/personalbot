from aiogram import types
import logging

from modules.database.models import create_user_if_not_exists
from modules.common import constants
from modules.buylist import messages


async def cmd_list(message: types.Message, *args, **kwargs):
    user = create_user_if_not_exists(message.chat.id)
    _list = user.get_buy_list()
    message_sent: types.Message = await message.answer(
        messages.ON_CMD_LIST,
        reply_markup=_list.generate_buttons_for_list(),
        parse_mode='Markdown',
    )
    
    logging.debug(f"Append message with list to list of messages")
    _list.messages.insert(0, message_sent.message_id)
    _list.messages = _list.messages[:constants.MAX_TRACKING_LISTS]
    _list._update()
