from aiogram import executor
import logging

from misc import dp, event_loop
from modules.buylist import setup as setup_buylist
from modules.default import setup as setup_default
from modules.cleaning import setup as setup_cleaning
from modules.default.checker import check_connection
if __name__ == '__main__':
    event_loop.run_until_complete(check_connection())
    # the order matters
    setup_default(dp, loop=event_loop)
    setup_buylist(dp)
    setup_cleaning(dp, loop=event_loop)
    
    executor.start_polling(dp, skip_updates=True, on_shutdown=check_connection)