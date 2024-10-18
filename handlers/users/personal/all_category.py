from aiogram.dispatcher.filters import Text

from handlers.users.personal.admin_test import is_admin
from loader import *


@dp.message_handler(Text(equals='Categoriyalarni ko\'rish'))
async def all_category(message: types.Message):
    if not is_admin(message.from_user.username):
        await message.answer("Siz ushbu buyruqni ishlatishga ruxsat etilmadingiz.")
        return

    a = db3.all_categories()

    for i in a:
        await message.answer(text=f"Categoriyalar\n"
                                  f"id: {i.id},\n"
                                  f"categoriya nomi {i.title},\n")


@dp.message_handler(Text(equals="Foydalanuvchilarni ko'rish!!"))
async def all_user(message: types.Message):
    if not is_admin(message.from_user.username):
        await message.answer("Siz ushbu buyruqni ishlatishga ruxsat etilmadingiz.")
        return

    b = db.all_register()
    for i in b:
        await message.answer(text=f"Foydalnuvchilar\n "
                                  f"IF: {i.ism_familya}"
                                  f"Telefon raqami: {i.phone_number}"
                                  f"Tumani shahar: {i.region}"
                                  f"Maktab: {i.school}"
                                  f"Sinf: {i.class_s}")


@dp.message_handler(Text("Test natijalrini ko'rish!!"))
async def all_result(message: types.Message):
    if not is_admin(message.from_user.username):
        await message.answer("Siz ushbu buyruqni ishlatishga ruxsat etilmadingiz.")
        return

    user_id = message.from_user.id
    c = db4.get_all_results(register_id=user_id)

    if not c:
        await message.answer("Hech qanday natija topilmadi.")
        return

    for result, ism_familya in c:
        await message.answer(
            text=f"Foydalanuvchilar\n"
                 f"IF: {ism_familya}\n"
                 f"Telefon raqami: {result.phone_number}\n"  # Adjust based on your actual field names
                 f"To'g'ri javoblar: {result.correct}\n"
                 f"Noto'g'ri javoblar: {result.incorrect}\n"
                 f"Jami: {result.total}"
        )
