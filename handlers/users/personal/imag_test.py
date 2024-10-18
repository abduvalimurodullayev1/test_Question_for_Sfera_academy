from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from keyboards.default.test_savol import admin_crud, menu
from loader import dp, db2, db5, db6  # Assuming you have a loader module where you initialize your Dispatcher
from states.test_state import ImageTestStates, Category2States

# List of admin usernames
admins = ["Abduvali_Murodullayev"]

# Dictionary to store user answers with user ID as key
user_answers = {}


def is_admin(username):
    return username in admins


@dp.message_handler(Text(equals="Rasimli Test Qo\'shish"))
async def test_add_title(message: types.Message):
    if not is_admin(message.from_user.username):
        await message.answer("Siz ushbu buyruqni ishlatishga ruxsat etilmadingiz.")
        return

    await message.answer(text="Categoryani idsini kiriting", reply_markup=ReplyKeyboardRemove())
    await ImageTestStates.category.set()


@dp.message_handler(state=ImageTestStates.category)
async def add_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category_id'] = message.text
    await message.answer("Rasmni kiriting")
    await ImageTestStates.next()


@dp.message_handler(lambda message: not message.photo, state=ImageTestStates.image_test)
async def check_photo(message: types.Message):
    await message.answer("Bu rasm formatida emas")


@dp.message_handler(state=ImageTestStates.image_test, content_types=['photo'])
async def add_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['test_image'] = message.photo[0].file_id
    await message.answer("Test savolni kiriting", reply_markup=ReplyKeyboardRemove())
    await ImageTestStates.next()


@dp.message_handler(state=ImageTestStates.title)
async def add_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['question'] = message.text
    await message.answer("A) variant uchun javobni kiriting")
    await ImageTestStates.next()


@dp.message_handler(state=ImageTestStates.a_variant)
async def add_a_variant(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['a_variant'] = message.text
    await message.answer("B) variant uchun javobni kiriting")
    await ImageTestStates.next()


@dp.message_handler(state=ImageTestStates.b_variant)
async def add_b_variant(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['b_variant'] = message.text
    await message.answer("C) variant uchun javobni kiriting")
    await ImageTestStates.next()


@dp.message_handler(state=ImageTestStates.c_variant)
async def add_c_variant(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['c_variant'] = message.text
    await message.answer("To'g'ri variantni belgilang (0 dan 2 gacha bitta raqamni oling)")
    await ImageTestStates.next()


@dp.message_handler(state=ImageTestStates.correct_answer)
async def add_correct_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['correct_answer'] = message.text
        try:
            correct_option = int(data['correct_answer'])
            if correct_option not in [0, 1, 2]:
                raise ValueError
        except ValueError:
            await message.answer("Iltimos, to'g'ri variantni 0 dan 2 gacha bo'lgan raqamda kiriting")
            return

        db5.add_imagetest(
            category_id=data['category_id'],
            test_image=data['test_image'],
            question=data['question'],
            a_variant=data['a_variant'],
            b_variant=data['b_variant'],
            c_variant=data['c_variant'],
            correct_answer=data['correct_answer']
        )

    await state.finish()
    await message.answer("Ma'lumotlar saqlandi", reply_markup=admin_crud())

    @dp.message_handler(Text(equals="Rasimli Test categoryasini qo'shish"))
    async def test_add_title(message: types.Message):
        await message.answer(text="Categorya kiriting",
                             reply_markup=ReplyKeyboardRemove())
        await Category2States.title.set()

    @dp.message_handler(state=Category2States.title)
    async def add_correct_answer(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['title'] = message.text
        await state.finish()
        await message.answer("Ma'lumotlar saqlandi",
                             reply_markup=admin_crud())
        db6.add_category(title=data['title'])
