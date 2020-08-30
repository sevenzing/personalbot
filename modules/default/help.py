from aiogram import types
import logging
from modules.default import messages

async def cmd_help(message: types.Message):
    await message.answer(messages.ON_CMD_HELP, parse_mode='Markdown')