from aiogram import types
import logging


from modules.cleaning import messages


async def cmd_setreminder(message: types.Message):
    k = types.InlineKeyboardMarkup(row_width=2)
    k.add(types.InlineKeyboardButton(text='ok', callback_data='None'), types.InlineKeyboardButton(text='not ok', callback_data='None'))
    k.add(types.InlineKeyboardButton(text='^', callback_data='None'), types.InlineKeyboardButton(text=' ', callback_data='None'))
    k.add(types.InlineKeyboardButton(text='8:00', callback_data='None'), types.InlineKeyboardButton(text=' ', callback_data='None'))
    k.add(types.InlineKeyboardButton(text='\/', callback_data='None'), types.InlineKeyboardButton(text=' ', callback_data='None'))
    
    await message.answer(text='.', reply_markup=k, parse_mode='Markdown')

