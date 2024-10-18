from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db2, db3


def telefon_raqam_yuborish():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("📱Telefon raqamni yuborish", request_contact=True)
    rkm.add(button1)
    return rkm


def Qashqadaryo():
    rkm = ReplyKeyboardMarkup(row_width=1)
    button2 = (KeyboardButton('Qarshi tumani'))
    button3 = (KeyboardButton('Shakhrisabz tumani'))
    button4 = (KeyboardButton('Kitob tumani'))
    button5 = (KeyboardButton('Qarshi  shahri'))
    button6 = (KeyboardButton('Kasbi shahri'))
    button7 = (KeyboardButton('Shahrisabz shahri'))
    button8 = (KeyboardButton('Muborak tumani'))
    button9 = (KeyboardButton('Dehkanabad tumani'))
    button10 = (KeyboardButton('Guzar tumani'))
    button11 = (KeyboardButton('Kamashi tumani'))
    button12 = (KeyboardButton('Chiroqchi shahri'))
    button13 = (KeyboardButton('Mirishkor tumani'))
    button14 = (KeyboardButton('Yakkabog\' tumani'))
    button15 = (KeyboardButton('Koson tumani'))
    button16 = (KeyboardButton('Nishon tumani'))
    rkm.add(button2, button3, button4, button5, button6, button7, button8, button9, button10, button11, button12,
            button13, button14, button15, button16)
    return rkm


def menu():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton(text="🏆 Olimpiadalarga kirish")
    button2 = KeyboardButton(text="ℹ️ Ma'lumotlar")
    button5 = KeyboardButton(text="📞 Kontaktlar/Manzil")
    button6 = KeyboardButton(text="🏅 Mukofotlar 🎁")
    button7 = KeyboardButton(text="🔝 Reyting 📊")
    button7 = KeyboardButton(text="🌐 Tilni o'zgartirish")
    rkm.add(button1, button2, button5, button6, button7)
    return rkm



def admin_crud():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton('Test qo\'shish')
    button2 = KeyboardButton('Testni o\'chirish')
    button3 = KeyboardButton('Categoriya qo\'shish')
    button4 = KeyboardButton('Categoriyalarni ko\'rish')
    button5 = KeyboardButton("Foydalanuvchilarni ko'rish!!")
    button7 = KeyboardButton("Rasimli Test Qo\'shish")
    button8 = KeyboardButton("Rasimli Test categoryasini qo'shish")
    button9 = KeyboardButton("Rasimli Test categoryalarni kurish")
    button6 = KeyboardButton("Test natijalrini ko'rish!!")
    rkm.add(button1, button2, button3, button4, button5, button7, button8, button9)
    return rkm

def Test_yechish():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton(text="👁 Rasmli testlar 🖼")
    button1 = KeyboardButton(text="🇺🇸 🏆Kelajak yoshlari 9-sinf 🏆🇬🇧")
    button12 = KeyboardButton(text="📘 Zakovat 📚")
    button2 = KeyboardButton(text="🔙ortga")
    rkm.add(button1, button2, button, button12)
    return rkm


def Test_yechish_ru():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton(text="👁 Тесты с картинками 🖼")
    button1 = KeyboardButton(text="🇺🇸 🏆Будущая молодежь 9 класса 🏆🇬🇧")
    button2 = KeyboardButton(text="🔙назад")
    rkm.add(button1, button2)
    return rkm


def Test_yechish_eng():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton(text="👁 Picture tests 🖼")
    button1 = KeyboardButton(text="🇺🇸 🏆Future youth 9th grade 🏆🇬🇧")
    button2 = KeyboardButton(text="🔙back")
    rkm.add(button1, button2)
    return rkm


def ruyhatdan_utish():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton(text="Ro'yxatdan o'tish")
    rkm.add(button1)
    return rkm


def ruyhatdan_utish_eng():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton(text="Registration")
    rkm.add(button1)
    return rkm


def ruyhatdan_utish_ru():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton(text="регистр")
    rkm.add(button1)
    return rkm


def all_category():
    rkm = ReplyKeyboardMarkup(row_width=2)
    categories = db3.all_category()
    for category in categories:
        button = KeyboardButton(text=category.title)
        btn = KeyboardButton(text='🔙ortga')
        rkm.add(button)
    return rkm


def comment():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    com_button = KeyboardButton('fikr💬 qoldirish')
    location = KeyboardButton("Manzil📍")
    orq = KeyboardButton("🔙ortga")
    rkm.add(com_button, orq, location)
    return rkm


def result():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    future_young = KeyboardButton('🇺🇸 🏆Kelajak yoshlari 9-sinf natijalari 🏆🇬🇧')
    image_test = KeyboardButton('👁 Rasmli testlar natijalari🖼')
    zak = KeyboardButton('📘 Zakovat 📚')
    rkm.add(future_young, image_test, zak)


def result_ru():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    future_young = KeyboardButton('🇺🇸 🏆Результаты будущей молодежи за 9 класс 🏆🇬🇧')
    image_test = KeyboardButton('👁Результаты фототеста🖼')
    zak = KeyboardButton('📘 Интеллект 📚')
    rkm.add(future_young, image_test, zak)


def result_eng():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    future_young = KeyboardButton('🇺🇸 🏆Results of future youth for 9th grade 🏆🇬🇧')
    image_test = KeyboardButton('👁Photo test results🖼')
    zak = KeyboardButton('📘 Интеллект 📚')
    rkm.add(future_young, image_test, zak)




def school():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("1-maktab")
    button2 = KeyboardButton("2-maktab")
    button3 = KeyboardButton("3-maktab")
    button4 = KeyboardButton("4-maktab")
    button5 = KeyboardButton("5-maktab")
    button6 = KeyboardButton("6-maktab")
    button7 = KeyboardButton("7-maktab")
    button8 = KeyboardButton("8-maktab")
    button9 = KeyboardButton("9-maktab")
    button10 = KeyboardButton("10-maktab")
    button11 = KeyboardButton("11-maktab")
    button12 = KeyboardButton("12-maktab")
    button13 = KeyboardButton("13-maktab")
    button14 = KeyboardButton("14-maktab")
    button15 = KeyboardButton("15-maktab")
    button16 = KeyboardButton("16-maktab")
    button17 = KeyboardButton("17-maktab")
    button18 = KeyboardButton("18-maktab")
    button19 = KeyboardButton("19-maktab")
    button20 = KeyboardButton("20-maktab")
    button21 = KeyboardButton("21-maktab")
    button22 = KeyboardButton("22-maktab")
    button23 = KeyboardButton("23-maktab")
    button24 = KeyboardButton("24-maktab")
    button25 = KeyboardButton("25-maktab")
    button26 = KeyboardButton("26-maktab")
    button27 = KeyboardButton("27-maktab")
    button28 = KeyboardButton("28-maktab")
    button29 = KeyboardButton("29-maktab")
    button30 = KeyboardButton("30-maktab")
    button31 = KeyboardButton("31-maktab")
    button32 = KeyboardButton("32-maktab")
    button33 = KeyboardButton("33-maktab")
    button34 = KeyboardButton("34-maktab")
    button35 = KeyboardButton("35-maktab")
    button36 = KeyboardButton("36-maktab")
    button37 = KeyboardButton("37-maktab")
    button38 = KeyboardButton("38-maktab")
    button39 = KeyboardButton("39-maktab")
    button40 = KeyboardButton("40-maktab")
    button41 = KeyboardButton("41-maktab")
    button42 = KeyboardButton("42-maktab")
    button43 = KeyboardButton("43-maktab")
    button44 = KeyboardButton("44-maktab")
    button45 = KeyboardButton("45-maktab")
    rkm.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
            button12, button13, button14, button15, button16, button17, button18, button19, button20, button21,
            button22, button23, button24, button25, button26, button27, button28, button29, button30, button31,
            button32, button33, button34, button35, button36, button37, button38, button39, button40, button41,
            button42, button43, button44, button45)
    return rkm


def sinf():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("1-sinf")
    button2 = KeyboardButton("2-sinf")
    button3 = KeyboardButton("3-sinf")
    button4 = KeyboardButton("4-sinf")
    button5 = KeyboardButton("5-sinf")
    button6 = KeyboardButton("6-sinf")
    button7 = KeyboardButton("7-sinf")
    button8 = KeyboardButton("8-sinf")
    button9 = KeyboardButton("9-sinf")
    button10 = KeyboardButton("10-sinf")
    button11 = KeyboardButton("11-sinf")
    rkm.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11)
    return rkm