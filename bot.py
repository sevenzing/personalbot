from aiogram import executor
import logging

from misc import dp, reminder_loop
from modules.buylist import setup as setup_buylist
from modules.default import setup as setup_default
from modules.cleaning import setup as setup_cleaning

if __name__ == '__main__':
    
    # the order matters
    setup_default(dp)
    setup_buylist(dp)
    setup_cleaning(dp, loop=reminder_loop)
    
    executor.start_polling(dp, skip_updates=True)