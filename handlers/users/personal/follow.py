import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
import sqlite3
from keyboards.default.test_savol import Test_yechish
from loader import dp  # Adjust import statement based on your project structure
from data.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)

channel = '@abduvaliblogs'


# Connect to the SQLite database


def create_keyboard(subscribed=False):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('Kanalga o`tish', url=f'https://t.me/{channel[1:]}'))
    if not subscribed:
        keyboard.add(types.InlineKeyboardButton('✅ Obuna bo\'lind ', callback_data='subscribed'))
    return keyboard


# Message handler for starting the test
@dp.message_handler(Text(equals="🏆 Olimpiadalarga kirish"))
async def start_command(message: types.Message):
    try:
        chat_member = await bot.get_chat_member(channel, message.from_user.id)
        if chat_member.status in ('creator', 'administrator', 'member'):
            await message.answer("Assalomu alaykum, hush kelibsiz! Testni yechish uchun tayyormisiz?",
                                 reply_markup=Test_yechish())
        else:
            # User is not a member, prompt to subscribe
            keyboard = create_keyboard()
            await message.answer("Kanallarga obuna bo'ling", reply_markup=keyboard)
    except Exception as e:
        await message.answer(f"kanalga obuna bo'lmadingiz")


# Callback query handler for the 'subscribed' button
@dp.callback_query_handler(lambda c: c.data == 'subscribed', state="*")
async def handle_subscription(callback_query: CallbackQuery, state: FSMContext):
    try:
        # Check if the user is a member of the channel
        chat_member = await bot.get_chat_member(channel, callback_query.from_user.id)
        if chat_member.status in ('creator', 'administrator', 'member'):
            # User is already a member, proceed to test performance
            await bot.send_message(callback_query.from_user.id,
                                   "Assalomu alaykum, hush kelibsiz! Testni yechish uchun tayyormisiz?",
                                   reply_markup=Test_yechish())

            # Optionally, remove the inline keyboard after successful subscription
            await bot.edit_message_reply_markup(callback_query.message.chat.id,
                                                callback_query.message.message_id,
                                                reply_markup=None)

            # Optionally, reset the state if needed
            await state.reset_state()
        else:
            # User is not a member, send subscription message and keyboard
            keyboard = create_keyboard()
            await bot.send_message(callback_query.from_user.id, "Kanallarga obuna bo'ling", reply_markup=keyboard)

            # Optionally, update the inline keyboard to reflect unsubscription state
            await bot.edit_message_reply_markup(callback_query.message.chat.id,
                                                callback_query.message.message_id,
                                                reply_markup=keyboard)
    except Exception as e:
        await bot.send_message(callback_query.from_user.id, f"kanalga obuna bo'lmadingiz")

# Close the database connection when the bot stops
