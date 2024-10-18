from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from loader import dp, bot, db2
from utils.db_api.test_db import Category, TestResult, Test_Savol

from keyboards.default.test_savol import menu

user_answers = {}
correct_answers = {}
poll_to_message = {}
photo_to_message = {}  # Dictionary to track photo messages


async def user_start_test(message: types.Message):
    tests = db2.all_Test()
    for test in tests:
        options = [f"A) {test.a_variant}", f"B) {test.b_variant}", f"C) {test.c_variant}"]
        correct_option_id = int(test.correct_answer)
        sent_poll = await message.answer_poll(
            question=test.question,
            options=options,
            type='quiz',
            correct_option_id=correct_option_id,
            is_anonymous=False
        )

        correct_answers[sent_poll.poll.id] = test.correct_answer
        poll_to_message[sent_poll.poll.id] = sent_poll.message_id

    return sent_poll


@dp.message_handler(Text(equals="🇺🇸 🏆Kelajak yoshlari 9-sinf 🏆🇬🇧"))
async def select_category_handler(message: types.Message):
    categories = Category.all_categories()
    if not categories:
        await message.answer("Hech qanday kategoriyalar topilmadi.")
        return

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for category in categories:
        keyboard.add(KeyboardButton(category.title))

    await message.answer("Iltimos, kategoriyani tanlang:", reply_markup=keyboard)


@dp.message_handler(lambda message: any(category.title == message.text for category in Category.all_categories()))
async def start_tests_handler(message: types.Message):
    category = next((cat for cat in Category.all_categories() if cat.title == message.text), None)
    if not category:
        await message.answer("Kategoriya topilmadi.")
        return

    tests = Test_Savol.get_tests_by_category(category.id)
    if not tests:
        await message.answer(f"{category.title} uchun testlar topilmadi.")
        return

    user_id = message.from_user.id
    user_answers[user_id] = {
        'user_id': user_id,
        'correct': 0, 'incorrect': 0, 'total': len(tests), 'current_index': 0, 'tests': tests
    }

    await message.answer("Eslatma:\nXar 10 soniyada yangilanib turadi", reply_markup=ReplyKeyboardRemove())
    await send_next_question(user_id, message)


async def send_next_question(user_id, message):
    user_data = user_answers[user_id]
    current_index = user_data['current_index']
    tests = user_data['tests']

    if current_index < len(tests):
        test = tests[current_index]

        options = [f"A) {test.a_variant}", f"B) {test.b_variant}", f"C) {test.c_variant}"]
        correct_option_id = int(test.correct_answer)
        sent_poll = await message.answer_poll(
            question=test.question,
            options=options,
            type='quiz',
            correct_option_id=correct_option_id,
            is_anonymous=False
        )

        correct_answers[sent_poll.poll.id] = test.correct_answer
        poll_to_message[sent_poll.poll.id] = sent_poll.message_id


        user_data['current_index'] += 1
    else:
        correct = user_data['correct']
        incorrect = user_data['incorrect']
        total = user_data['total']

        db_result = TestResult(
            correct=correct,
            incorrect=incorrect,
            total=total
        )
        db_result.save()

        await message.answer(f"Test yakunlandi!\nTo'g'ri ✅: {correct}\nXato❌: {incorrect}\nJami🎯: {total}")
        del user_answers[user_id]
        await message.answer("Asosiy menyuga qaytdingiz", reply_markup=menu())


@dp.poll_answer_handler()
async def handle_poll_answer(quiz_answer: types.PollAnswer):
    user_id = quiz_answer.user.id
    poll_id = quiz_answer.poll_id

    if user_id not in user_answers:
        return

    correct_option_id = correct_answers.get(poll_id)
    if correct_option_id is not None:
        if quiz_answer.option_ids[0] == correct_option_id:
            user_answers[user_id]['correct'] += 1
        else:
            user_answers[user_id]['incorrect'] += 1

    # Immediately delete the previous poll and photo messages
    message_id = poll_to_message.get(poll_id)
    photo_id = photo_to_message.get(poll_id)
    if message_id:
        try:
            await bot.delete_message(chat_id=user_id, message_id=message_id)
            if photo_id:  # Check if the photo_id is present
                await bot.delete_message(chat_id=user_id, message_id=photo_id)
        except Exception as e:
            print(f"Failed to delete message: {e}")
        finally:
            del poll_to_message[poll_id]
            if poll_id in photo_to_message:
                del photo_to_message[poll_id]

    await send_next_question(user_id, types.Message(chat=types.Chat(id=user_id), from_user=types.User(id=user_id)))


@dp.message_handler(Text(equals="🔙orqaga"))
async def back(message: types.Message):
    await message.answer("Orqaga qaytildi", reply_markup=menu())


@dp.message_handler(Text(equals="Test natijalari"))
async def test_results_handler(message: types.Message):
    results = TestResult.get_all_results()
    if not results:
        await message.answer("Hali hech qanday natijalar yo'q.")
        return

    for result in results:
        await message.answer(f"To'g'ri javoblar: {result.correct}\n"
                             f"Noto'g'ri javoblar: {result.incorrect}\n"
                             f"Jami savollar: {result.total}")
