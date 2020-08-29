from aiogram import types
from modules.common.utils import admin_only_handler
from modules.common.constants import EXIT_CODES
from misc import dp
import logging


@admin_only_handler
async def cmd_restart(message: types.Message, *args, **kwargs):
    '''
    Exit from the program if sender is admin
    '''
    logging.warning(f"Admin requests for bot restarting. Stop polling")
    await message.answer('Stop polling')
    
    dp.stop_polling()
    await dp.wait_closed()
    
    exit_code = EXIT_CODES['Restart']
    logging.warning(f"Exiting with exit code {exit_code}")
    await message.answer('Restarting...')

    exit(exit_code)
