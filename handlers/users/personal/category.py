from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from keyboards.default.test_savol import all_category, admin_crud, result, Test_yechish
from loader import dp, db3
from states.test_state import CategoryStates


@dp.message_handler(Text(equals="🏆 Olimpiadalarga kirish"))
async def category(message: types.Message):
    await message.answer(text="bosh menyudasiz",
                         reply_markup=Test_yechish())


@dp.message_handler(state=CategoryStates.title)
async def add_correct_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
    await state.finish()
    await message.answer("Ma'lumotlar saqlandi",
                         reply_markup=admin_crud())
    db3.add_category(title=data['title'])


@dp.message_handler(Text(equals="Categoriya qo'shish"))
async def test_add_title(message: types.Message):
    await message.answer(text="Categorya kiriting",
                         reply_markup=ReplyKeyboardRemove())
    await CategoryStates.title.set()


@dp.message_handler(Text(equals="📘 Zakovat 📚"))
async def test_add_title(message: types.Message):
    await message.answer("zakovat 12.05.2025 sanasida start oladi")
