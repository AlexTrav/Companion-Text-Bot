from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from os import getenv
from dotenv import load_dotenv, find_dotenv


# Подгружаем токен бота из утилиты окружения (.env)
load_dotenv(find_dotenv())


# Создаём экземпляр бота и диспетчера
bot = Bot(token=getenv('BOT_TOKEN_API'))
dp = Dispatcher(bot=bot, storage=MemoryStorage())
