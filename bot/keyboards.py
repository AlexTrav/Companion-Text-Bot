from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
# from aiogram.utils.callback_data import CallbackData
from bot.db.database import db


# Отправить удаление нижней-клавиатуры
def reply_keyboard_remove():
    answer = 'Успешно'
    rrm = ReplyKeyboardRemove()
    return answer, rrm


# Отправить имя модели нейросети
def get_model_name(user_id):
    selected_model_id = db.get_data(table='users', where=1, op1='id', op2=user_id)[0][3]
    model_name = db.get_data(table='models', where=1, op1='id', op2=selected_model_id)[0][1]
    return model_name


# Отправить клавиатуру команды start
def get_start_kb():
    answer = 'Добро пожаловать в Companion Text Bot!'
    start_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='Начать разговор', callback_data='talks')],
        [InlineKeyboardButton(text='Выбрать модель', callback_data='set_model')],
        [InlineKeyboardButton(text='История запросов', callback_data='logs')],
        [InlineKeyboardButton(text='О нас', callback_data='about')]
    ])
    return answer, start_kb


# Отправить клавиатуру режима беседы
def get_talks_kb(user_id):
    selected_model_id = db.get_data(table='users', where=1, op1='id', op2=user_id)[0][3]
    model = db.get_data(table='models', where=1, op1='id', op2=selected_model_id)[0]
    answer = f'Вы перешли в режим беседы.\nВыбранная модель: {model[1]}.\nОписание модели: {model[2]}.\nНачните диалог..'
    talks_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='←'))
    return answer, talks_kb









