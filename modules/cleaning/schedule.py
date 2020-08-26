from aiogram import types

from modules.common.utils import get_file_by_url
from modules.common.constants import URL_TO_SCHEDULE

async def cmd_schedule(message: types.Message):
    '''
    Send photo oof schedule to the chat
    '''
    await message.answer_photo(get_file_by_url(URL_TO_SCHEDULE))