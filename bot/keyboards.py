from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils.callback_data import CallbackData
# from bot.db.database import db


def get_start_keyboard():
    answer = 'Добро пожаловать в Companion Text Bot!'
    start_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='Начать разговор', callback_data='talks')],
        [InlineKeyboardButton(text='Выбрать модель', callback_data='set_model')],
        [InlineKeyboardButton(text='История запросов', callback_data='logs')],
        [InlineKeyboardButton(text='О нас', callback_data='about')]
    ])
    return answer, start_keyboard
