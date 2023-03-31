from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData
from bot.db.database import db


# Отправить удаление нижней-клавиатуры
def reply_keyboard_remove():
    answer = 'Успешно'
    rrm = ReplyKeyboardRemove()
    return answer, rrm


# Отправить имя модели нейросети
def get_model_name_kb(user_id):
    selected_model_id = db.get_data(table='users', where=1, op1='id', op2=user_id)[0][3]
    model_name = db.get_data(table='models', where=1, op1='id', op2=selected_model_id)[0][1]
    return model_name


# Отправить клавиатуру команды start
def get_start_kb():
    answer = 'Добро пожаловать в Companion Text Bot!'
    start_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='Начать разговор', callback_data='talks')],
        [InlineKeyboardButton(text='Выбрать модель', callback_data='update_model')],
        [InlineKeyboardButton(text='История запросов', callback_data='logs')],
        [InlineKeyboardButton(text='О нас', callback_data='about')]
    ])
    return answer, start_kb


# Отправить клавиатуру режима беседы
def get_talks_kb(user_id):
    selected_model_id = db.get_data(table='users', where=1, op1='id', op2=user_id)[0][3]
    model = db.get_data(table='models', where=1, op1='id', op2=selected_model_id)[0]
    answer = f'Вы перешли в режим беседы\nВыбранная модель: {model[1]}\nОписание модели: {model[2]}\nНачните диалог'
    talks_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='←'))
    return answer, talks_kb


# Отрпавить клавиатуру выбора модели
def get_all_model_kb():
    answer = 'Выберите модель:'
    cb = CallbackData('all_model', 'id', 'action')
    all_model_kb = InlineKeyboardMarkup(row_width=1)
    for model in db.get_data(table='models'):
        all_model_kb.add(InlineKeyboardButton(text=model[1], callback_data=cb.new(id=model[0], action='model')))
    all_model_kb.add(InlineKeyboardButton(text='←', callback_data=cb.new(id=-1, action='back')))
    return answer, all_model_kb


# Отправить клавиатуру модели
def get_model_kb(model_id):
    model = db.get_data(table='models', where=1, op1='id', op2=model_id)[0]
    answer = f'Модель: {model[1]}\nОписание модели: {model[2]}\nПример:\nЗапрос: {model[3]}\nПример ответа: {model[4]}'
    cb = CallbackData('model', 'id', 'action')
    model_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='Выбрать модель', callback_data=cb.new(id=model[0], action='set_model'))],
        [InlineKeyboardButton(text='←', callback_data=cb.new(id=-1, action='back'))]
    ])
    return answer, model_kb


# Отправить клавиатуру логов пользователя
def get_logs_kb(user_id):
    cb = CallbackData('logs', 'id', 'action')
    answer = f'Вот последние запросы сделанные вами:'
    logs_kb = InlineKeyboardMarkup(row_width=1)
    logs = db.get_data(table='logs', where=1, op1='user_id', op2=user_id)
    if len(logs) < 50:
        for log in logs:
            logs_kb.add(InlineKeyboardButton(text=log[3], callback_data=cb.new(id=log[0], action='log')))
    else:
        for log in logs[:50]:
            logs_kb.add(InlineKeyboardButton(text=log[3], callback_data=cb.new(id=log[0], action='log')))
    logs_kb.add(InlineKeyboardButton(text='←', callback_data=cb.new(id=-1, action='back')))
    return answer, logs_kb


# Отрпавить клавиатуру лога
def get_log_kb(log_id):
    cb = CallbackData('log', 'action')
    log = db.get_data(table='logs', where=1, op1='id', op2=log_id)[0]
    model_name = db.get_data(table='models', where=1, op1='id', op2=log[2])[0][1]
    answer = f'Детали запроса:\nЗапрос под номером: {log_id}\nИспользованная модель нейросети: {model_name}\nЗапрос: {log[3]}\nОтвет: {log[4]}'
    log_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='←', callback_data=cb.new(action='back'))]
    ])
    return answer, log_kb
