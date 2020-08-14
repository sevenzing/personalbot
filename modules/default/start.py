from aiogram import types
from aiogram.dispatcher import FSMContext


async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    # TODO: message variable
    await message.answer("Hi there! /list for your buy list")