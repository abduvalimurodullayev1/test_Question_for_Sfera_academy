import types

from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp


@dp.message_handler(Text(equals="ℹ️ Ma'lumotlar"))
async def about_me(message: types.Message):
    await message.reply_photo("https://lh3.googleusercontent.com/p/AF1QipMVaqkfRn-_ZUFL-sW36RPcfcGusu2JQidd5sev=s680-w680-h510",
                              caption="But it city academy bot")