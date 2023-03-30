from aiogram import types

from bot.loader import dp
from bot.states import UserStatesGroup
from bot.keyboards import *

from bot.db.database import db


# Обработчик кнопки "Начать разговор"
@dp.callback_query_handler(text='talks', state=UserStatesGroup.start)
async def open_talks(callback: types.CallbackQuery):
    await UserStatesGroup.talks.set()
    ans, kb = get_talks_kb(callback.from_user.id)
    await callback.message.answer(text=ans,
                                  reply_markup=kb)
    await callback.answer()


# Обработчик команды "Выбрать модель"
@dp.callback_query_handler(text='update_model', state=UserStatesGroup.start)
async def open_all_model(callback: types.CallbackQuery):
    await UserStatesGroup.update_model.set()
    ans, kb = get_all_model()
    await callback.message.answer(text=ans,
                                  reply_markup=kb)
    await callback.answer()


# Обработчик выбора модели и возвращения в главное меню
@dp.callback_query_handler(CallbackData('all_model', 'id', 'action').filter(), state=UserStatesGroup.update_model)
async def open_model(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await UserStatesGroup.start.set()
        ans, kb = get_start_kb()
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    else:
        ans, kb = get_model(model_id=callback_data['id'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    await callback.answer()


# Обработчик установки модели или  возвращения в меню выбора модели
@dp.callback_query_handler(CallbackData('model', 'id', 'action').filter(), state=UserStatesGroup.update_model)
async def update_model(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        ans, kb = get_all_model()
        await callback.message.answer(text=ans,
                                      reply_markup=kb)
    else:
        db.update_model_user(user_id=callback.from_user.id, model_id=callback_data['id'])
        await UserStatesGroup.start.set()
        ans, kb = get_start_kb()
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        await callback.answer('Модель успешно выбрана!')
    await callback.answer()
