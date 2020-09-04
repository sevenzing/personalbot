from misc import dp, event_loop
from modules.buylist import setup as setup_buylist
from modules.default import setup as setup_default
from modules.cleaning import setup as setup_cleaning
from modules.admin import setup as setup_admin
from modules.default.checker import check_connection
from modules.admin.utils import send_message_to_admin

from aiogram import executor
import logging

async def on_startup(dp):
    await check_connection()
    await send_message_to_admin('Starting the bot')

async def on_shutdown(dp):
    await send_message_to_admin('Shut down the bot')

if __name__ == '__main__':
    setup_default(dp, loop=event_loop)
    setup_admin(dp)
    setup_buylist(dp)
    setup_cleaning(dp, loop=event_loop)
    
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
