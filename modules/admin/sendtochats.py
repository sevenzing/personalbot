from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import ChatNotFound, BotBlocked
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
import logging

from modules.admin.utils import admin_only_handler, send_message_to_admin
from modules.admin import messages


class SendToChatsFSM(StatesGroup):
    waiting_for_sendtochats_ids = State()
    waiting_for_sendtochats_message = State()

@admin_only_handler
async def cmd_sendtochats(message: types.Message, state: FSMContext, *args, **kwargs):
    '''
    Send a message to a chat
    '''
    await SendToChatsFSM.waiting_for_sendtochats_ids.set()
    await message.answer(messages.ON_CMD_SENDTOCHATS)

async def process_ids(message: types.Message, state: FSMContext): 
    '''
    Step for processing chat ids
    '''   
    async with state.proxy() as data:
        data['ids'] = message.text.split('\n')

    await SendToChatsFSM.waiting_for_sendtochats_message.set()
    await message.answer(messages.PROCESSED_IDS)

async def process_message(message: types.Message, state: FSMContext):
    '''
    Step for processing message
    '''
    async with state.proxy() as data:
        ids = data['ids']

        for _id in ids:
            try:
                await message.bot.send_message(_id, message.text)
                await message.answer(messages.PROCESSED_MESSAGE % _id)
            except ChatNotFound:
                await message.answer(messages.CHAT_NOT_FOUND % _id)
            except BotBlocked:
                await message.answer(messages.BOT_BLOCKED % _id)
            
    await state.finish()
