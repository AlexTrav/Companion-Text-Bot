from aiogram import types

from bot.loader import dp
from bot.keyboards import *
from bot.models import get_answer
from bot.states import UserStatesGroup
from bot.db.database import db


# Обработчик режима диалога и кнопки ←. Принимает запрос, отправляет ответ - Меню диалога с 🤖
@dp.message_handler(content_types=['text'], state=UserStatesGroup.talks)
async def send_answer(message: types.Message) -> None:
    if message.text == '←':
        await UserStatesGroup.start.set()
        ans1, kb1 = get_start_kb()
        ans2, kb2 = reply_keyboard_remove()
        await message.answer(text=ans2,
                             reply_markup=kb2)
        await message.answer(text=ans1,
                             reply_markup=kb1)
    else:
        answer = get_answer(get_model_name_kb(message.from_user.id), message.text).replace('"', "'")
        if answer != '':
            db.insert_log(user_id=message.from_user.id, model_id=db.get_model_id(user_id=message.from_user.id), question=message.text, answer=answer.lstrip())
            await message.answer(answer)
