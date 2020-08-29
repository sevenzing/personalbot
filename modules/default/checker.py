import aiohttp
import logging
import sys
from modules.common.constants import URL_TO_CHECK_INTERNET_CONNECTION, EXIT_CODES

from concurrent.futures._base import TimeoutError
from aiohttp.client_exceptions import ClientConnectorError


session = aiohttp.ClientSession()

async def check_connection(*args, **kwargs):
    logging.debug('Trying to connect internet')

    try:
        async with session.get(URL_TO_CHECK_INTERNET_CONNECTION, timeout=5) as resp:
            result = await resp.text()
    except (TimeoutError, ClientConnectorError):
        result = None
    
    if not result:
        logging.warning('Cannot connect to the internet. Exit from the bot')
        sys.exit(EXIT_CODES['Internet'])
    else:
        logging.debug('Internet connected')
    