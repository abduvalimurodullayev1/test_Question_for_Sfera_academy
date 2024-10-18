# from aiogram import types
# from aiogram.dispatcher.filters import Text
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
#
# from keyboards.default.test_savol import menu  # Ensure this imports your main menu keyboard
# from loader import dp, bot
# from utils.db_api.test_db import Category, Test_Savol, \
#     TestResult  # Adjust the import according to your project structure
#
# user_answers = {}
# correct_answers = {}
# poll_to_message = {}
#
#
# async def send_test_question(message: types.Message, test, question_number, total_questions):
#     options = [f"A) {test.a_variant}", f"B) {test.b_variant}", f"C) {test.c_variant}"]
#     sent_message = await message.answer_poll(
#         question=f"{question_number}/{total_questions}: {test.question}",
#         options=options,
#         type='quiz',
#         correct_option_id=test.correct_answer,
#         is_anonymous=False
#     )
#
#     correct_answers[sent_message.poll.id] = test.correct_answer
#     poll_to_message[sent_message.poll.id] = sent_message.message_id
#     return sent_message
#
#
# @dp.message_handler(Text(equals="Testni boshlash"))
# async def select_category_handler(message: types.Message):
#     categories = Category.all_categories()
#     if not categories:
#         await message.answer("Hech qanday kategoriyalar topilmadi.")
#         return
#
#     keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
#     for category in categories:
#         keyboard.add(KeyboardButton(category.title))
#
#     await message.answer("Iltimos, kategoriyani tanlang:", reply_markup=keyboard)
#
#
# @dp.message_handler(lambda message: any(category.title == message.text for category in Category.all_categories()))
# async def start_tests_handler(message: types.Message):
#     category = next((cat for cat in Category.all_categories() if cat.title == message.text), None)
#     if not category:
#         await message.answer("Kategoriya topilmadi.")
#         return
#
#     tests = Test_Savol.get_tests_by_category(category.id)
#     if not tests:
#         await message.answer(f"{category.title} uchun testlar topilmadi.")
#         return
#
#     # Store user_id in user_answers dictionary
#     user_id = message.from_user.id
#     user_answers[user_id] = {
#         'user_id': user_id,
#         'correct': 0, 'incorrect': 0, 'total': len(tests), 'current_index': 0, 'tests': tests
#     }
#
#     await message.answer("Eslatma:\nXar 10 soniyada yangilanib turadi", reply_markup=ReplyKeyboardRemove())
#     await send_next_question(user_id, message)
#
#
# async def send_next_question(user_id, message):
#     user_data = user_answers[user_id]
#     current_index = user_data['current_index']
#     tests = user_data['tests']
#
#     if current_index < len(tests):
#         test = tests[current_index]
#         await send_test_question(message, test, current_index + 1, len(tests))
#         user_data['current_index'] += 1
#     else:
#         correct = user_data['correct']
#         incorrect = user_data['incorrect']
#         total = user_data['total']
#
#         # Save results to the database
#         db_result = TestResult(
#             correct=correct,
#             incorrect=incorrect,
#             total=total
#         )
#         db_result.save()
#
#         await message.answer(f"Test yakunlandi!\nTo'g'ri ✅: {correct}\nXato❌: {incorrect}\nJami🎯: {total}")
#         del user_answers[user_id]
#         await message.answer("Asosiy menyuga qaytdingiz", reply_markup=menu())
#
#
# @dp.poll_answer_handler()
# async def handle_poll_answer(quiz_answer: types.PollAnswer):
#     user_id = quiz_answer.user.id
#     poll_id = quiz_answer.poll_id
#
#     if user_id not in user_answers:
#         return
#
#     correct_option_id = correct_answers.get(poll_id)
#     if correct_option_id is not None:
#         if quiz_answer.option_ids[0] == correct_option_id:
#             user_answers[user_id]['correct'] += 1
#         else:
#             user_answers[user_id]['incorrect'] += 1
#
#
#     # Delete the previous poll message
#     message_id = poll_to_message.get(poll_id)
#     if message_id:
#         await bot.delete_message(chat_id=user_id, message_id=message_id)
#         del poll_to_message[poll_id]
#
#     await send_next_question(user_id, types.Message(chat=types.Chat(id=user_id), from_user=types.User(id=user_id)))
#
#
# @dp.message_handler(Text(equals="🔙orqaga"))
# async def back(message: types.Message):
#     await message.answer("Orqaga qaytildi", reply_markup=menu())
#
#
# @dp.message_handler(Text(equals="Test natijalari"))
# async def test_results_handler(message: types.Message):
#     results = TestResult.validate_phone_number()
#     if not results:
#         await message.answer("Hali hech qanday natijalar yo'q.")
#         return
#
#     for result in results:
#         user = await bot.get_chat(result.user_id)
#         await message.answer(f"To'g'ri javoblar: {result.correct}\n"
#                              f"Noto'g'ri javoblar: {result.incorrect}\n"
#                              f"Jami savollar: {result.total}")
