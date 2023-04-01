from aiogram import types

from bot.loader import dp
from bot.states import UserStatesGroup
from bot.keyboards import *

from bot.db.database import db


# Обработчик кнопки "Начать разговор" - Главное меню
@dp.callback_query_handler(text='talks', state=UserStatesGroup.start)
async def open_talks(callback: types.CallbackQuery):
    await UserStatesGroup.talks.set()
    ans, kb = get_talks_kb(callback.from_user.id)
    await callback.message.answer(text=ans,
                                  reply_markup=kb)
    await callback.answer()


# Обработчик команды "Выбрать модель" - Главное меню
@dp.callback_query_handler(text='update_model', state=UserStatesGroup.start)
async def open_all_model(callback: types.CallbackQuery):
    await UserStatesGroup.update_model.set()
    ans, kb = get_all_model_kb()
    await callback.message.edit_text(text=ans,
                                     reply_markup=kb)
    await callback.answer()


# Обработчик выбора модели и возвращения в главное меню - Меню выбора модели
@dp.callback_query_handler(CallbackData('all_model', 'id', 'action').filter(), state=UserStatesGroup.update_model)
async def open_model(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await UserStatesGroup.start.set()
        ans, kb = get_start_kb()
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    else:
        ans, kb = get_model_kb(model_id=callback_data['id'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    await callback.answer()


# Обработчик установки модели или возвращения в меню выбора модели - Меню установки модели
@dp.callback_query_handler(CallbackData('model', 'id', 'action').filter(), state=UserStatesGroup.update_model)
async def update_model(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        ans, kb = get_all_model_kb()
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    else:
        db.update_model_user(user_id=callback.from_user.id, model_id=callback_data['id'])
        await UserStatesGroup.start.set()
        ans, kb = get_start_kb()
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        await callback.answer('Модель успешно выбрана!')
    await callback.answer()


# Обработчик кнопки "История запросов" - Главное меню
@dp.callback_query_handler(text='logs', state=UserStatesGroup.start)
async def open_all_logs(callback: types.CallbackQuery):
    await UserStatesGroup.logs.set()
    ans, kb = get_logs_kb(callback.from_user.id)
    await callback.message.edit_text(text=ans,
                                     reply_markup=kb)
    await callback.answer()


# Обработчик последних запросов user-а и возвращения в главное меню и возможности очистить историю запросов пользователя - Меню выбора запроса
@dp.callback_query_handler(CallbackData('logs', 'id', 'action').filter(), state=UserStatesGroup.logs)
async def open_log(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await UserStatesGroup.start.set()
        ans, kb = get_start_kb()
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    elif callback_data['action'] == 'log':
        ans, kb = get_log_kb(log_id=callback_data['id'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    else:
        db.clear_history_logs(user_id=callback.from_user.id)
        ans, kb = get_logs_kb(callback.from_user.id)
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    await callback.answer()


# Обработчик возвращения в историю логов пользователя - Меню лога пользователя
@dp.callback_query_handler(CallbackData('log', 'action').filter(), state=UserStatesGroup.logs)
async def close_log(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        ans, kb = get_logs_kb(callback.from_user.id)
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    await callback.answer()


# Обработчик кнопки "О нас"
@dp.callback_query_handler(text='about', state=UserStatesGroup.start)
async def open_about(callback: types.CallbackQuery):
    await UserStatesGroup.about.set()
    ans, kb = get_about_kb()
    await callback.message.edit_text(text=ans,
                                     reply_markup=kb)
    await callback.answer()


# Обработчик возвращения в главное меню из формы "О нас"
@dp.callback_query_handler(CallbackData('about', 'action').filter(), state=UserStatesGroup.about)
async def close_about(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await UserStatesGroup.start.set()
        ans, kb = get_start_kb()
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    await callback.answer()
