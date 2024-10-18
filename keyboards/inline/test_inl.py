from aiogram import Bot, types


def create_keyboart():
    btn = types.InlineKeyboardMarkup(row_width=1)
    btn.add(types.InlineKeyboardButton('Channel', url='https://t.me/privatchanelbehruz'))
    btn.add(types.InlineKeyboardButton('✅ Check Subscription', callback_data='checksub'))
