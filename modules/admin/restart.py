from aiogram import types
from modules.admin.utils import admin_only_handler, send_message_to_admin
from modules.common.constants import EXIT_CODES
from misc import dp
import asyncio
import logging


@admin_only_handler
async def cmd_restart(message: types.Message, *args, **kwargs):
    '''
    Exit from the program if sender is admin
    '''
    logging.warning(f"Admin requests for bot restarting. Stop polling")
    await send_message_to_admin('Stop polling')
    
    dp.stop_polling()
    await asyncio.sleep(5)
    await dp.wait_closed()
    
    exit_code = EXIT_CODES['Restart']
    logging.warning(f"Exiting with exit code {exit_code}")
    await send_message_to_admin('Restarting...')

    exit(exit_code)
