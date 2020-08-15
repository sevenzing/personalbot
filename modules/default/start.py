from aiogram import types
from aiogram.dispatcher import FSMContext

from modules.default import messages

async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    await message.answer(messages.ON_CMD_START)
