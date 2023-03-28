from aiogram import types

from bot.loader import dp, bot

from bot.states import UserStatesGroup
from bot.keyboards import *

from bot.db.database import db


@dp.message_handler(commands=['start'], state='*')
async def start_command(message: types.Message):
    db.checking_user(user_id=message.from_user.id, username=message.from_user.username, flname=message.from_user.first_name + ' ' + message.from_user.last_name)
    await UserStatesGroup.start.set()
    ans, kb = get_start_kb()
    await bot.send_message(chat_id=message.from_user.id,
                           text=ans,
                           reply_markup=kb)
