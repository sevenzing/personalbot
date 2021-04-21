from aiogram import types
from bs4 import BeautifulSoup
import requests
import re

from modules.common.constants import URL_TO_SCHEDULE


async def cmd_schedule(message: types.Message):
    '''
    Send link to schedule to the chat
    '''
    link_to_schedule = __extract_url_from_hotel_innopolis()
    await message.answer(link_to_schedule or 'Error. Cannot fetch schedule')

def __extract_url_from_hotel_innopolis(url_to_site='https://hotel.innopolis.university/studentaccommodation/#block884'):
    soup = __get_page_soup(url_to_site)
    links = soup.find_all('a', href=re.compile('.*docs\.google\.com.*'))
    if links:
        return links[1]['href']

    
def __get_page_content(url) -> str:
    """
    Returns page content from url
    """
    session = requests.Session()
    session.headers.update({'User-Agent': 'fuck you'})
    return session.get(url).content.decode('ascii', errors='ignore')

def __get_page_soup(url) -> BeautifulSoup:
    """
    Returns bs4 instance of url
    """
    
    html_doc = __get_page_content(url)
    return BeautifulSoup(html_doc)
