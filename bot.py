from aiogram import executor
import logging

from misc import dp
from modules.buylist import setup as setup_buylist
from modules.default import setup as setup_default

if __name__ == '__main__':
    
    # the order matters
    setup_default(dp)
    setup_buylist(dp)
    
    executor.start_polling(dp, skip_updates=True)