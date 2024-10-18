from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.db_api.test_db import Register, Test_Savol, Category, TestResult, Image_test, Category_2

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Register()
db2 = Test_Savol()
db3 = Category()
db4 = TestResult()
db5 = Image_test()
db6 = Category_2()