from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from keyboards.default.test_savol import admin_crud, menu
from loader import dp, db2, db5, db3  # Assuming you have a loader module where you initialize your Dispatcher
from states.test_state import TestAddStates, CategoryStates

# List of admin usernames
admins = ["Abduvali_Murodullayev"]

# Dictionary to store user answers with user ID as key
user_answers = {}


def is_admin(username):
    return username in admins


@dp.message_handler(Text(equals="Test qo'shish"))
async def test_add_title(message: types.Message):
    if not is_admin(message.from_user.username):
        await message.answer("Siz ushbu buyruqni ishlatishga ruxsat etilmadingiz.")
        return

    await message.answer(text="Categoryani idsini kiriting", reply_markup=ReplyKeyboardRemove())
    await TestAddStates.category.set()


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
    if not is_admin(message.from_user.username):
        await message.answer("Siz ushbu buyruqni ishlatishga ruxsat etilmadingiz.")
        return

    await message.answer(text="Categorya kiriting",
                         reply_markup=ReplyKeyboardRemove())
    await CategoryStates.title.set()


@dp.message_handler(state=TestAddStates.category)
async def add_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category_id'] = message.text
    await message.answer("Test savolini kiriting")
    await TestAddStates.next()


@dp.message_handler(state=TestAddStates.title)
async def add_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['question'] = message.text
    await message.answer("A) variant uchun javobni kiriting")
    await TestAddStates.next()


@dp.message_handler(state=TestAddStates.a_variant)
async def add_a_variant(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['a_variant'] = message.text
    await message.answer("B) variant uchun javobni kiriting")
    await TestAddStates.next()


@dp.message_handler(state=TestAddStates.b_variant)
async def add_b_variant(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['b_variant'] = message.text
    await message.answer("C) variant uchun javobni kiriting")
    await TestAddStates.next()


@dp.message_handler(state=TestAddStates.c_variant)
async def add_c_variant(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['c_variant'] = message.text
    await message.answer("To'g'ri variantni belgilang (0 dan 2 gacha bitta raqamni oling)")
    await TestAddStates.next()


@dp.message_handler(state=TestAddStates.correct_answer)
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

        db2.add_test(
            category=data['category_id'],
            question=data['question'],
            a_variant=data['a_variant'],
            b_variant=data['b_variant'],
            c_variant=data['c_variant'],
            correct_answer=data['correct_answer']
        )

    await state.finish()
    await message.answer("Ma'lumotlar saqlandi", reply_markup=admin_crud())


@dp.message_handler(Text(equals="Testni boshlash"))
async def user_start_test(message: types.Message):
    # Fetch tests from the database
    tests = db2.all_test()

    # Iterate over each test and create a poll
    for test in tests:
        options = [f"A) {test.a_variant}", f"B) {test.b_variant}", f"C) {test.c_variant}"]
        correct_option_id = int(test.correct_answer)
        await message.answer_poll(
            question=test.question,
            options=options,
            type='quiz',
            correct_option_id=correct_option_id,
            is_anonymous=False
        )


@dp.poll_answer_handler()
async def handle_user_answer(poll_answer: types.PollAnswer):
    user_id = poll_answer.user.id
    poll_id = poll_answer.poll_id
    selected_option = poll_answer.option_ids[0]

    # Get the correct option from the database
    correct_option = db2.get_correct_option(poll_id)

    # Check if the selected option is correct
    if user_id not in user_answers:
        user_answers[user_id] = {"correct": 0, "incorrect": 0}

    if selected_option == correct_option:
        user_answers[user_id]["correct"] += 1
    else:
        user_answers[user_id]["incorrect"] += 1


@dp.message_handler(Text(equals="finish test"))
async def finish_test(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_answers:
        correct_answers = user_answers[user_id]["correct"]
        incorrect_answers = user_answers[user_id]["incorrect"]
        await message.answer(
            f"Test tugadi!\nTo'g'ri javoblar: {correct_answers}\nNoto'g'ri javoblar: {incorrect_answers}")
    else:
        await message.answer("Siz hali testni boshlamadingiz.")


@dp.message_handler(Text(equals="🔙orqaga"))
async def back_to_menu(message: types.Message):
    await message.answer("Orqaga qaytildi", reply_markup=menu())
