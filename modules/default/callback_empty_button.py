from aiogram import types


async def answer_callback_empty_button_handler(query: types.CallbackQuery):
    await query.answer(text='')