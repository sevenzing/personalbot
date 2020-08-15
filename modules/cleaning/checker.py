import asyncio
from aiogram import Dispatcher

from modules.common.constants import BOT_ADMIN, REMINDER_CHECKER_INTERVAL

async def check_time(dp: Dispatcher):
    
    # TODO: check time
    
    await asyncio.sleep(REMINDER_CHECKER_INTERVAL)
    
