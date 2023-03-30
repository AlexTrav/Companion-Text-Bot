from aiogram import types

from bot.loader import dp
from bot.states import UserStatesGroup
from bot.keyboards import *


# Обработчик кнопки "Начать разговор"
@dp.callback_query_handler(text='talks', state=UserStatesGroup.start)
async def open_talks(callback: types.CallbackQuery):
    await UserStatesGroup.talks.set()
    ans, kb = get_talks_kb(callback.from_user.id)
    await callback.message.answer(text=ans,
                                  reply_markup=kb)
    await callback.answer()
