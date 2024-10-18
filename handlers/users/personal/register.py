from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import re

from keyboards.default.test_savol import telefon_raqam_yuborish, Qashqadaryo, menu, school, sinf
from loader import dp
from states.test_state import RegisterState
from utils.db_api.test_db import Register, SessionLocal


@dp.message_handler(Text(equals="Ro'yxatdan o'tish"))
async def start_registration_handler(message: types.Message, state: FSMContext):
    await RegisterState.phone_number.set()
    await message.answer("Telefon raqamingizni kiriting:", reply_markup=telefon_raqam_yuborish())


@dp.message_handler(state=RegisterState.phone_number, content_types=types.ContentType.CONTACT)
async def check_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number

    with SessionLocal() as session:
        is_registered = session.query(Register).filter(Register.phone_number == phone_number).first()

    if is_registered:
        await message.answer("Siz allaqachon ro'yxatdan o'tgansiz. Asosiy menyuga o'tishingiz mumkin.",
                             reply_markup=menu())
        await state.finish()
    else:
        async with state.proxy() as data:
            data['phone_number'] = phone_number
        await RegisterState.next()
        await message.answer("Ism, familya va sharifingizni kiritish uchun, iltimos, to'liq ismingizni yozing:")


@dp.message_handler(state=RegisterState.ism_familya)
async def add_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        fullname = message.text.strip()
        if not re.match(r"^[a-zA-Z\s]+$", fullname):
            await message.answer(
                "Iltimos, familiya, ism va sharifingizni faqat harflardan tashkil etilgan bo'lishi kerak.")
            return
        data['ism_familya'] = fullname
        await RegisterState.next()
        await message.answer("Tumaningizni kiriting", reply_markup=Qashqadaryo())


@dp.message_handler(state=RegisterState.region)
async def add_region(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['region'] = message.text.strip()
        await RegisterState.next()
        await message.answer("Maktabingizni kiriting:", reply_markup=school())


@dp.message_handler(state=RegisterState.school)
async def add_school(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['school'] = message.text.strip()
        await RegisterState.next()
        await message.answer("Sinfingizni kiriting:", reply_markup=sinf())


@dp.message_handler(state=RegisterState.class_s)
async def add_class_s(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['class_s'] = message.text.strip()

        new_registration = Register.add_register(
            ism_familya=data['ism_familya'],
            phone_number=data['phone_number'],
            region=data['region'],
            school=data['school'],
            class_s=data['class_s']
        )

        if new_registration:
            await message.answer("Ro'yxatdan o'tdingiz! Endi kategoriyalardan birini tanlang.", reply_markup=menu())
        else:
            await message.answer("Ro'yxatdan o'tishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")

        await state.finish()
