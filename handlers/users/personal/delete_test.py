from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from keyboards.default.test_savol import admin_crud
from loader import dp, db2
from states.test_state import DeleteTestStates


@dp.message_handler(Text(equals="Testni uchirish"))
async def delete_test(message: types.Message):
    await message.answer("Testni o'chirish uchun ID raqamini kiriting:",
                         reply_markup=ReplyKeyboardRemove())
    await DeleteTestStates.id.set()


@dp.message_handler(state=DeleteTestStates.id)
async def delete_user(message: types.Message, state: FSMContext):
    try:
        test_id = int(message.text)
        test = db2.get_test(test_id)
        if test:
            db2.delete_test(test_id)
            await message.answer("Test muvaffaqiyatli o'chirildi.",
                                 reply_markup=admin_crud())
        else:
            await message.answer("Berilgan ID raqami bilan test topilmadi.")
    except ValueError:
        await message.answer("Xato: Iltimos, to'g'ri ID raqamini kiriting.")
    finally:
        await state.finish()
