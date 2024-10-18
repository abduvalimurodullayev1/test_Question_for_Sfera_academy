from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from keyboards.default.test_savol import comment, menu
from loader import dp
from states.test_state import CommentState
from utils.db_api.test_db import get_db, Commentary


@dp.message_handler(Text(equals="📞 Kontaktlar/Manzil"))
async def address_contact(message: types.Message):
    await message.reply("Tanlang!!",
                        reply_markup=comment())


@dp.message_handler(Text(equals="fikr💬 qoldirish"))
async def start_comment(message: types.Message):
    await message.reply("Fikringizni qoldiring:")
    await CommentState.waiting_for_comment.set()


@dp.message_handler(state=CommentState.waiting_for_comment)
async def save_comment(message: types.Message, state: FSMContext):
    comment_text = message.text
    if not comment_text:
        await message.reply("Iltimos, fikringizni yozing.")
        return

    with get_db() as db:
        new_comment = Commentary(text=comment_text)
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)

    await message.reply("Fikr saqlandi!")
    await state.finish()


@dp.message_handler(Text(equals="Manzil📍"))
async def send_location(message: types.Message):
    await message.answer_location(latitude=38.8470612, longitude=65.7965881)


@dp.message_handler(Text(equals="🔙ortga"))
async def back(message: types.Message):
    await message.answer("ortga qaytildi", reply_markup=menu())


@dp.message_handler(Text(equals="🏅 Mukofotlar 🎁"))
async def back(message: types.Message):
    await message.answer_photo(photo='https://i.imgflip.com/383duu.png',
                               caption="G'oliblar olgan o'rinlariga qarab, quyidagi yutuqlar bilan mukofotlanadilar. - Lug'at kitoblar - Brend sovg'alar (futbolka, ruchka, bloknot) - Boshqarma rahbarining sertifikati",
                               reply_markup=menu())
