from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove

from keyboards.default.test_savol import admin_crud, menu, ruyhatdan_utish
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if message.from_user.id == 6288993380:
        await message.answer(text=f"Admin xush kelibsiz !",
                             reply_markup=admin_crud())

    else:
        await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!",
                             reply_markup=ruyhatdan_utish())
