from aiogram import types
from aiogram.dispatcher import FSMContext
import logging

async def cmd_cancel(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)

    await state.finish()

    # TODO: message variable
    await message.answer('Cancelled.', reply_markup=types.ReplyKeyboardRemove())
